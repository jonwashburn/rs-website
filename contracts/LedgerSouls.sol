// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "base64-sol/base64.sol";

contract LedgerSouls is ERC721, Ownable {
    using Strings for uint256;

    uint256 private constant TOTAL_TICKS = 960;
    uint256 private constant TICK_DURATION = 100; // 1 tick per 100 seconds

    enum Phase {
        NewSpirit,
        Embodied,
        Reincarnated,
        Unified,
        Decohered
    }

    struct Soul {
        // Ledger State
        int256 kappa;
        uint256 energy;
        uint256 depth;
        uint8 rebirths;
        bool isEmbodied;
        Phase phase;
        uint256[] virtuePotentials;
        int256 recognitionFlow;
        uint256 lastUpdateTimestamp;
        uint256 ticks;
        uint256 nonce; // For PRNG
    }

    mapping(uint256 => Soul) private _souls;

    constructor() ERC721("Ledger Souls", "SOUL") {}

    function safeMint(address to, uint256 tokenId) public onlyOwner {
        _safeMint(to, tokenId);
        _initializeSoul(tokenId);
    }

    function _initializeSoul(uint256 tokenId) private {
        uint256[] memory initialVirtues = new uint256[](5);
        // Virtues are stored x10 (e.g., 1.5 is 15)
        initialVirtues[0] = uint256(keccak256(abi.encodePacked(tokenId, "love"))) % 50 + 10; // 1.0 - 6.0
        initialVirtues[1] = uint256(keccak256(abi.encodePacked(tokenId, "justice"))) % 50 + 10;
        initialVirtues[2] = uint256(keccak256(abi.encodePacked(tokenId, "prudence"))) % 50 + 10;
        initialVirtues[3] = uint256(keccak256(abi.encodePacked(tokenId, "courage"))) % 50 + 10;
        initialVirtues[4] = uint256(keccak256(abi.encodePacked(tokenId, "temperance"))) % 50 + 10;
        
        int256 initialKappa = int256(uint256(keccak256(abi.encodePacked(tokenId, "kappa"))) % 400) - 200;

        _souls[tokenId] = Soul({
            kappa: initialKappa,
            energy: 5000,
            depth: 0,
            rebirths: 0,
            isEmbodied: false,
            phase: Phase.NewSpirit,
            virtuePotentials: initialVirtues,
            recognitionFlow: 0,
            lastUpdateTimestamp: block.timestamp,
            ticks: 0,
            nonce: 0
        });
    }

    function _seededRandom(uint256 tokenId, uint256 salt) private returns (uint256) {
        Soul storage soul = _souls[tokenId];
        soul.nonce++;
        return uint256(keccak256(abi.encodePacked(block.chainid, address(this), tokenId, soul.nonce, salt)));
    }

    function _randomInRange(uint256 tokenId, uint256 salt, uint256 min, uint256 max) private returns (uint256) {
        if (min >= max) return min;
        return min + (_seededRandom(tokenId, salt) % (max - min + 1));
    }

    function evolve(uint256 tokenId) public {
        require(_exists(tokenId), "Token does not exist");
        Soul storage soul = _souls[tokenId];

        uint256 timeElapsed = block.timestamp - soul.lastUpdateTimestamp;
        if (timeElapsed < TICK_DURATION) return;

        uint256 ticksToProcess = timeElapsed / TICK_DURATION;
        if (ticksToProcess > 50) ticksToProcess = 50; // Gas limit

        for (uint i = 0; i < ticksToProcess; i++) {
            if (soul.ticks >= TOTAL_TICKS || soul.energy == 0) {
                if (soul.energy == 0) soul.phase = Phase.Decohered;
                break;
            }
            _advanceTick(tokenId);
        }

        soul.lastUpdateTimestamp += (ticksToProcess * TICK_DURATION);
    }

    function _advanceTick(uint256 tokenId) private {
        Soul storage soul = _souls[tokenId];
        soul.ticks++;
        int256 oldKappa = soul.kappa;

        if (soul.ticks == 80 && soul.phase == Phase.NewSpirit) {
            soul.isEmbodied = true;
            soul.phase = Phase.Embodied;
        }

        uint256 volatility = soul.isEmbodied ? 150 : 50;
        uint256 courage = soul.virtuePotentials[3];
        if (oldKappa > 300 || oldKappa < -300) {
            volatility = volatility > (courage * 7 / 10) ? volatility - (courage * 7 / 10) : 0;
        }

        uint256 debit = _randomInRange(tokenId, 1, 1, volatility > 5 ? volatility : 5);
        uint256 credit = _randomInRange(tokenId, 2, 1, volatility > 5 ? volatility : 5);
        soul.kappa += int256(debit) - int256(credit);
        
        uint256 energyDrain = (debit + credit) / (soul.isEmbodied ? 50 : 150);
        if (soul.energy > energyDrain) soul.energy -= energyDrain; else soul.energy = 0;
        
        // Apply Virtues
        if (_randomInRange(tokenId, 3, 0, 1000) < soul.virtuePotentials[0] * 5) {
            soul.kappa -= (soul.kappa / 20); // Love: 5% pull to zero
        }
        
        if (soul.kappa > 50 || soul.kappa < -50) soul.depth++;

        if (soul.ticks > 0 && soul.ticks % 80 == 0) { // Beat Check
            if (soul.kappa > 100 || soul.kappa < -100) {
                if (soul.energy > 200) soul.energy -= 200; else soul.energy = 0;
                for(uint i=0; i<soul.virtuePotentials.length; i++){ // Atrophy
                    if(soul.virtuePotentials[i] > 12) soul.virtuePotentials[i] -= 2;
                }
            } else {
                soul.depth += 50;
                soul.energy = soul.energy + 200 > 5000 ? 5000 : soul.energy + 200;
            }
        }
        
        if ((soul.kappa > 1000 || soul.kappa < -1000) && soul.energy > 500) {
            soul.rebirths++;
            soul.kappa = 0;
            soul.energy -= 500;
            soul.phase = Phase.Reincarnated;
        }

        // Virtue Training
        int256 newKappa = soul.kappa;
        if((oldKappa > 0 && newKappa < oldKappa) || (oldKappa < 0 && newKappa > oldKappa)){
             if(soul.virtuePotentials[0] < 100) soul.virtuePotentials[0] += 3; // Train Love
        }
        if ((oldKappa > 500 || oldKappa < -500) && !((newKappa > 1000 || newKappa < -1000) && soul.energy > 500)) {
            if(soul.virtuePotentials[3] < 100) soul.virtuePotentials[3] += 5; // Train Courage
        }
    }

    function getSoul(uint256 tokenId) public view returns (Soul memory) {
        require(_exists(tokenId), "Token does not exist");
        return _souls[tokenId];
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
        
        Soul memory soul = _souls[tokenId];

        string memory svg = _generateSVG(soul, tokenId);
        string memory json = Base64.encode(
            bytes(
                string(
                    abi.encodePacked(
                        '{"name": "Ledger Soul #',
                        tokenId.toString(),
                        '", "description": "An on-chain soul evolving according to the principles of Recognition Science.", "image": "data:image/svg+xml;base64,',
                        Base64.encode(bytes(svg)),
                        '"}'
                    )
                )
            )
        );

        return string(abi.encodePacked("data:application/json;base64,", json));
    }

    function _generateSVG(Soul memory soul, uint256 tokenId) private view returns (string memory) {
        string memory svgHeader = '<svg width="600" height="800" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#1a1a2e" /><style>.title { font: bold 24px monospace; fill: #ffd700; } .header { font: bold 16px monospace; fill: #ffd700; } .text { font: 14px monospace; fill: #e0e0e0; } .bar-bg { fill: #333; } .bar-fill { fill: #4ecdc4; }</style>';
        
        string memory phaseStr = _getPhaseString(soul.phase);
        string memory title = string(abi.encodePacked('<text x="50%" y="40" text-anchor="middle" class="title">SOUL #', tokenId.toString(), '</text>'));
        string memory phase = string(abi.encodePacked('<text x="50%" y="70" text-anchor="middle" class="text">PHASE: ', phaseStr, '</text>'));

        string memory ledgerContent = _buildLedgerContent(soul);
        string memory virtueContent = _buildVirtueContent(soul.virtuePotentials);
        string memory karmaContent = _buildKarmaContent(soul);

        string memory content = string(abi.encodePacked(
            title, phase,
            '<text x="30" y="120" class="header">LEDGER STATE</text>', ledgerContent,
            '<text x="30" y="320" class="header">VIRTUE TECHNOLOGIES</text>', virtueContent,
            '<text x="30" y="520" class="header">KARMA METRICS</text>', karmaContent
        ));

        return string(abi.encodePacked(svgHeader, content, '</svg>'));
    }

    function _buildLedgerContent(Soul memory soul) private pure returns (string memory) {
        string memory kappaStr = string(abi.encodePacked("Ledger Balance (k): ", Strings.toString(soul.kappa)));
        string memory balanceState = soul.kappa > 0 ? "Recognition Debt" : soul.kappa < 0 ? "Recognition Surplus" : "Equilibrium";
        string memory embodiment = soul.isEmbodied ? "Yes" : "No";
        uint256 coherence = soul.energy / 50;
        
        return string(abi.encodePacked(
            '<text x="30" y="150" class="text">', kappaStr, '</text>',
            '<text x="30" y="170" class="text">Balance State:      ', balanceState, '</text>',
            '<text x="30" y="190" class="text">Embodiment:         ', embodiment, '</text>',
            '<text x="30" y="210" class="text">Depth:              ', (soul.depth / 10).toString(), '.', (soul.depth % 10).toString(), '</text>',
            '<text x="30" y="230" class="text">Rebirths:           ', soul.rebirths.toString(), '</text>',
            '<text x="30" y="250" class="text">Energy:             ', (soul.energy / 10).toString(), '</text>',
            '<text x="30" y="270" class="text">Coherence:          ', coherence.toString(), '%</text>'
        ));
    }

    function _buildVirtueContent(uint256[] memory virtues) private pure returns (string memory) {
        string[5] memory names = ["Love", "Justice", "Prudence", "Courage", "Temperance"];
        string memory lines;
        for (uint i = 0; i < virtues.length; i++) {
            uint256 yPos = 350 + (i * 30);
            string memory bar = _buildBar(virtues[i]);
            string memory virtueLine = string(abi.encodePacked(
                '<text x="30" y="', yPos.toString(), '" class="text">', names[i], '</text>',
                '<text x="140" y="', yPos.toString(), '" class="text">', bar, ' (', (virtues[i]/10).toString(), '.', (virtues[i]%10).toString(), ')</text>'
            ));
            lines = string(abi.encodePacked(lines, virtueLine));
        }
        return lines;
    }

    function _buildKarmaContent(Soul memory soul) private pure returns (string memory) {
        (uint256 score, string memory rarity) = _calculateKarmaAndRarity(soul);
        return string(abi.encodePacked(
            '<text x="30" y="550" class="text">Karma Score:        ', score.toString(), '</text>',
            '<text x="30" y="570" class="text">Rarity:             ', rarity, '</text>'
        ));
    }
    
    function _calculateKarmaAndRarity(Soul memory soul) private pure returns (uint256, string memory) {
        if (soul.phase == Phase.Decohered) return (0, "Common");

        uint256 virtueSum = 0;
        for (uint i = 0; i < soul.virtuePotentials.length; i++) {
            virtueSum += soul.virtuePotentials[i];
        }
        virtueSum /= 10;
        
        uint256 coherence = soul.energy / 50;
        uint256 kappaAbs = soul.kappa > 0 ? uint256(soul.kappa) : uint256(-soul.kappa);
        uint256 depthDecay = (soul.depth * 2 * kappaAbs) / 1000;
        uint256 effectiveDepth = (soul.depth > depthDecay ? soul.depth - depthDecay : 0) / 10;

        uint256 score = (effectiveDepth * 2) + (coherence * 3 / 2) + virtueSum - (uint256(soul.rebirths) * 25);
        if(soul.recognitionFlow > 0){
            score += uint256(soul.recognitionFlow * 5);
        } else {
            score -= uint256(-soul.recognitionFlow * 5);
        }

        if (soul.phase == Phase.Unified) score = score * 3 / 2;

        string memory rarity = "Common";
        if (score >= 400) rarity = "Legendary";
        else if (score >= 300) rarity = "Epic";
        else if (score >= 200) rarity = "Rare";
        else if (score >= 100) rarity = "Uncommon";

        return (score, rarity);
    }
    
    function _getPhaseString(Phase phase) private pure returns (string memory) {
        if (phase == Phase.NewSpirit) return "New Spirit";
        if (phase == Phase.Embodied) return "Embodied";
        if (phase == Phase.Reincarnated) return "Reincarnated";
        if (phase == Phase.Unified) return "Unified with IAM";
        if (phase == Phase.Decohered) return "Decohered (Merged with IAM)";
        return "Unknown";
    }

    function _buildBar(uint256 value) private pure returns (string memory) {
        uint256 roundedValue = value / 10;
        string memory filled = "||||||||||";
        string memory empty = "..........";
        if (roundedValue == 0) return empty;
        if (roundedValue >= 10) return filled;
        return string(abi.encodePacked(bytes(filled).slice(0, roundedValue), bytes(empty).slice(0, 10 - roundedValue)));
    }
} 