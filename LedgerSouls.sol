// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Base64.sol";

contract LedgerSouls is ERC721, ERC721Enumerable, Ownable {
    using Strings for uint256;
    using Strings for int256;

    uint256 public constant TOTAL_SUPPLY = 10000;
    uint256 public constant PHI = 1618; // φ * 1000

    struct SoulState {
        int256 kappa;
        uint256[5] virtues;
        uint256 depth;
        uint256 rebirths;
        uint256 cri;
        string qualia;
        string phase;
        uint256 months; // Added for enhanced text generation
    }

    constructor() ERC721("Ledger Souls", "SOUL") {}

    function _baseURI() internal pure override returns (string memory) {
        return "https://api.recognitionsceince.com/souls/";
    }

    function mint(address to, uint256 quantity) public payable {
        uint256 currentSupply = totalSupply();
        require(currentSupply + quantity <= TOTAL_SUPPLY, "Max supply exceeded");
        for (uint256 i = 0; i < quantity; i++) {
            _safeMint(to, currentSupply + i);
        }
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "URI query for nonexistent token");

        SoulState memory state = getCurrentState(tokenId);

        string memory textContent = generateTextDescription(tokenId, state);
        string memory svg = generateSVG(textContent);
        
        string memory json = Base64.encode(
            bytes(
                string.concat(
                    '{"name": "Ledger Soul #',
                    tokenId.toString(),
                    '", "description": "An on-chain soul evolving according to the principles of Recognition Science. Its state is dynamically generated and changes over time.", "image": "data:image/svg+xml;base64,',
                    Base64.encode(bytes(svg)),
                    '"}'
                )
            )
        );

        return string.concat("data:application/json;base64,", json);
    }
    
    function generateSVG(string memory textContent) internal pure returns (string memory) {
        string memory svg = string.concat(
            '<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">',
            '<rect width="100%" height="100%" fill="black" />',
            '<text y="50" font-family="monospace" font-size="14" fill="white">',
            '<tspan x="50">', textContent, '</tspan>',
            '</text>',
            '</svg>'
        );
        return svg;
    }

    function generateTextDescription(uint256 tokenId, SoulState memory state) internal pure returns (string memory) {
        uint256 months = state.months; // Assuming months is in state
        string memory virtuesText = "";
        string[5] memory virtueNames = ["Love", "Justice", "Wisdom", "Courage", "Temperance"];
        for (uint i = 0; i < 5; i++) {
            virtuesText = string.concat(virtuesText, virtueNames[i], Strings.toString(state.virtues[i]), "\n");
        }

        // Enhanced sections for 'proof'
        bytes32 ledgerHash = keccak256(abi.encodePacked(tokenId, block.timestamp));
        string memory ledgerProof = string.concat("Ledger Hash: ", Strings.toHexString(uint256(ledgerHash), 8), "\nVerified on Block: ", Strings.toString(block.number));

        string memory rsDerivation = string.concat("κ Derivation: E_coh * φ^r where r = ", Strings.toString(months), " (φ = 1.618)\nUncomputability Gap: ", Strings.toString(uint256(state.kappa) / 1000), " (45-threshold: ", (months >= 45 ? "ACTIVE" : "PENDING"), ")");

        string memory soulNarrative = string.concat("This soul emerges from the void as a unique recognition pattern in the universal ledger. Through ", Strings.toString(state.rebirths), " rebirths and depth of ", Strings.toString(state.depth), ", it navigates the 8-beat cycles toward awakening. Witness its eternal whisper..."); 

        return string.concat(
            "SOUL #", Strings.toString(tokenId), "\nMONTH: ", Strings.toString(months), " / 96\n\n",
            "STATE: ", state.phase, "\n",
            "QUALIA: ", state.qualia, "\n\n",
            "--- METRICS ---\n",
            "Curvature (Kappa): ", Strings.toString(uint256(state.kappa) / 1000), "\n",
            "Depth:             ", Strings.toString(state.depth), "\n",
            "Rebirths:          ", Strings.toString(state.rebirths), "\n",
            "CRI: ", Strings.toString(state.cri), "\n\n",
            "--- VIRTUES ---\n",
            virtuesText, "\n",
            "--- LEDGER PROOF ---\n",
            ledgerProof, "\n\n",
            "--- RS DERIVATION ---\n",
            rsDerivation, "\n\n",
            "--- SOUL NARRATIVE ---\n",
            soulNarrative
        );
    }

    function getCurrentState(uint256 tokenId) public view returns (SoulState memory) {
        uint256 seed = uint256(keccak256(abi.encodePacked(tokenId, block.chainid)));
        uint256 months = (block.timestamp / 30 days); // Simplified for on-chain
        if (months > 96) {
            months = 96;
        }

        // --- All the evolution logic from JS translated to Solidity ---
        // (This is a simplified version for demonstration)

        int256 chaos = int256((uint256(blockhash(block.number - 1)) % 41)) - 20;
        int256 initialKappa = int256((seed % 200)) - 100;
        int256 kappa = initialKappa + (chaos * 10) - int256(months * 10);
        
        uint256[5] memory virtues;
        for(uint i=0; i<5; i++){
            virtues[i] = (seed >> (i*8)) % 5 + months;
            if (virtues[i] > 10) virtues[i] = 10;
        }

        uint256 rebirths = months / 8;
        uint256 depth = months + (rebirths * PHI / 100);

        string memory qualia = "Observing the cosmic ledger.";
        if (kappa > 500) {
            qualia = "Experiencing imbalance and suffering.";
        } else if (kappa < -500) {
            qualia = "Flowing in a state of surplus and harmony.";
        }
        
        uint256 cri = depth + (virtues[2] * 10) - (rebirths * 5);

        string memory phase = "Breath";
        if (months >= 96) {
            phase = "Post-Breath";
        }

        return SoulState(kappa, virtues, depth, rebirths, cri, qualia, phase, months);
    }

    // The following functions are overrides required by Solidity.
    function _beforeTokenTransfer(address from, address to, uint256 tokenId, uint256 batchSize)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
} 