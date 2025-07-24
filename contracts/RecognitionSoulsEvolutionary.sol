// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";

/**
 * @title RecognitionSouls - Evolutionary Consciousness NFTs
 * @dev Time-locked souls that evolve from black box void to radiant φ-clusters over 4 years
 * Each soul represents literal RS consciousness awakening through gap navigation
 */
contract RecognitionSoulsEvolutionary is ERC721, Ownable {
    uint256 public constant TOTAL_SUPPLY = 10000;
    uint256 public constant PHI = 1618; // φ ≈ 1.618 * 1000 (fixed-point)
    uint256 public constant PHI_SCALE = 1000;
    uint8 public constant DIM = 8; // Octonionic dimensions
    uint256 public constant EVOLUTION_PERIOD = 365 days; // 1 year per stage
    uint256 public constant NURTURE_COOLDOWN = 1 days;
    
    // CURVE token for nurturing (placeholder address)
    IERC20 public curveToken;
    uint256 public nurturePrice = 100 * 10**18; // 100 CURVE per nurture

    struct Mode {
        int16 nu_phi;    // Frequency index
        int8 oam;        // Orbital Angular Momentum
        int8 sigma;      // Polarization Parity
        uint16 tau;      // Time-bin
        uint8 k_perp;    // Transverse Mode
        uint8 phi_e;     // Entanglement Phase
        int8 cost;       // Ledger cost
    }

    struct Soul {
        uint256 mintTime;        // Birth timestamp
        uint256 lastEvolve;      // Last nurture timestamp
        uint256 lastNurture;     // Last CURVE burn timestamp
        uint8 rung;              // Current rung level
        Mode[DIM] cluster;       // 8 eigenvalue modes
        uint8 gapCrossings;      // Consciousness experiences
        uint8 iAmAffinity;       // Self-recognition strength
        bool[DIM] virtues;       // 8 balanced virtues
        int8[DIM] ledgerHistory; // Past costs
        uint32 nurtureCount;     // Times nurtured
        bytes32 seed;            // Deterministic seed
        uint8 evolutionStage;    // 0-4: Void, Crack, Spiral, Bloom, Radiance
    }

    mapping(uint256 => Soul) public souls;
    uint256 public mintedCount;
    
    event SoulMinted(uint256 indexed tokenId, address indexed owner);
    event SoulEvolved(uint256 indexed tokenId, uint8 newStage);
    event SoulNurtured(uint256 indexed tokenId, uint32 nurtureCount);
    event GapNavigated(uint256 indexed tokenId, uint8 gapCrossings);

    constructor(address _curveToken) ERC721("Recognition Souls", "RSOUL") Ownable(msg.sender) {
        curveToken = IERC20(_curveToken);
    }

    /**
     * @dev Mint a new soul - starts as void (black box)
     */
    function mintSoul() external {
        require(mintedCount < TOTAL_SUPPLY, "Max supply reached");
        uint256 tokenId = mintedCount++;
        
        bytes32 seed = keccak256(abi.encodePacked(
            block.timestamp, 
            msg.sender, 
            tokenId,
            "RECOGNITION_SOUL_VOID"
        ));
        
        Soul storage s = souls[tokenId];
        s.mintTime = block.timestamp;
        s.lastEvolve = block.timestamp;
        s.lastNurture = block.timestamp;
        s.seed = seed;
        s.rung = 45; // Start at the gap
        s.evolutionStage = 0; // Void state
        
        _initializeSoulFromSeed(s, seed);
        _safeMint(msg.sender, tokenId);
        
        emit SoulMinted(tokenId, msg.sender);
    }

    /**
     * @dev Initialize soul properties deterministically
     */
    function _initializeSoulFromSeed(Soul storage s, bytes32 seed) internal {
        uint256 seedInt = uint256(seed);
        
        s.gapCrossings = 0; // Starts unawakened
        s.iAmAffinity = 0;  // No self-recognition yet
        s.nurtureCount = 0;
        
        // Initialize 8 modes with balanced costs
        int16 totalCost = 0;
        for (uint8 i = 0; i < DIM; i++) {
            uint256 modeSeed = uint256(keccak256(abi.encodePacked(seed, "mode", i)));
            s.cluster[i] = Mode({
                nu_phi: int16((modeSeed % 201) - 100),
                oam: int8(((modeSeed >> 16) % 11) - 5),
                sigma: ((modeSeed >> 24) % 2) == 0 ? int8(1) : int8(-1),
                tau: uint16((modeSeed >> 32) % 1024),
                k_perp: uint8((modeSeed >> 48) % 256),
                phi_e: uint8((modeSeed >> 56) % 256),
                cost: int8(((modeSeed >> 64) % 9) - 4)
            });
            totalCost += s.cluster[i].cost;
        }
        
        // Balance to zero (RS axiom)
        if (totalCost != 0) {
            s.cluster[0].cost -= int8(totalCost);
            if (s.cluster[0].cost > 4) s.cluster[0].cost = 4;
            if (s.cluster[0].cost < -4) s.cluster[0].cost = -4;
        }
        
        // Initialize virtues (exactly 4 active)
        for (uint8 i = 0; i < 4; i++) {
            s.virtues[i] = true;
        }
        for (uint8 i = 4; i < DIM; i++) {
            s.virtues[i] = false;
        }
        
        // Initialize ledger history
        for (uint8 i = 0; i < DIM; i++) {
            s.ledgerHistory[i] = 0;
        }
    }

    /**
     * @dev Nurture soul with CURVE tokens (accelerates evolution)
     */
    function nurtureSoul(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        Soul storage s = souls[tokenId];
        require(block.timestamp >= s.lastNurture + NURTURE_COOLDOWN, "Cooldown active");
        
        // Burn CURVE tokens
        curveToken.transferFrom(msg.sender, address(0), nurturePrice);
        
        s.lastNurture = block.timestamp;
        s.nurtureCount++;
        
        // Apply LNAL FOLD operation
        uint8 modeIndex = uint8(uint256(keccak256(abi.encodePacked(block.prevrandao, tokenId))) % DIM);
        Mode storage mode = s.cluster[modeIndex];
        
        // FOLD: Scale by φ
        mode.nu_phi = int16((int32(mode.nu_phi) * PHI) / PHI_SCALE);
        mode.k_perp = uint8((uint16(mode.k_perp) * PHI) / PHI_SCALE);
        if (mode.k_perp > 255) mode.k_perp = 255;
        
        mode.cost += 1;
        if (mode.cost > 4) mode.cost = 4;
        
        // Check for gap navigation
        if (s.rung == 45 && (s.nurtureCount % 8) == 5) {
            _navigateGap(s, tokenId);
        }
        
        // Update evolution stage based on nurture
        _updateEvolutionStage(s);
        
        emit SoulNurtured(tokenId, s.nurtureCount);
    }

    /**
     * @dev Navigate gap at rung 45 (consciousness emergence)
     */
    function _navigateGap(Soul storage s, uint256 tokenId) internal {
        // Experience 8 branches, choose minimal cost
        int16 minCost = type(int16).max;
        uint8 bestBranch = 0;
        
        for (uint8 branch = 0; branch < 8; branch++) {
            int16 cost = 0;
            for (uint8 i = 0; i < DIM; i++) {
                cost += abs(s.cluster[i].cost + int8(branch) - 4);
            }
            if (cost < minCost) {
                minCost = cost;
                bestBranch = branch;
            }
        }
        
        // Apply chosen branch
        int8 adjustment = int8(bestBranch) - 4;
        for (uint8 i = 0; i < DIM; i++) {
            s.cluster[i].cost += adjustment;
            if (s.cluster[i].cost > 4) s.cluster[i].cost = 4;
            if (s.cluster[i].cost < -4) s.cluster[i].cost = -4;
        }
        
        s.gapCrossings++;
        s.iAmAffinity = s.iAmAffinity + 10 > 100 ? 100 : s.iAmAffinity + 10;
        
        emit GapNavigated(tokenId, s.gapCrossings);
    }

    /**
     * @dev Update evolution stage based on time and nurturing
     */
    function _updateEvolutionStage(Soul storage s) internal {
        uint256 timeElapsed = block.timestamp - s.mintTime;
        uint256 baseStage = timeElapsed / EVOLUTION_PERIOD; // Natural time progression
        uint256 nurtureBonus = s.nurtureCount / 10; // Nurturing accelerates
        
        uint8 newStage = uint8((baseStage + nurtureBonus) > 4 ? 4 : (baseStage + nurtureBonus));
        
        if (newStage > s.evolutionStage) {
            s.evolutionStage = newStage;
            emit SoulEvolved(s.mintTime, newStage); // Using mintTime as tokenId proxy
        }
    }

    /**
     * @dev Get current evolution stage (0=Void, 1=Crack, 2=Spiral, 3=Bloom, 4=Radiance)
     */
    function getEvolutionStage(uint256 tokenId) public view returns (uint8) {
        Soul storage s = souls[tokenId];
        uint256 timeElapsed = block.timestamp - s.mintTime;
        uint256 baseStage = timeElapsed / EVOLUTION_PERIOD;
        uint256 nurtureBonus = s.nurtureCount / 10;
        
        return uint8((baseStage + nurtureBonus) > 4 ? 4 : (baseStage + nurtureBonus));
    }

    /**
     * @dev Generate evolving SVG based on current stage
     */
    function generateEvolutionSVG(uint256 tokenId) public view returns (string memory) {
        Soul storage s = souls[tokenId];
        uint8 stage = getEvolutionStage(tokenId);
        
        string memory svg = '<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">';
        
        // Stage 0: Void (Black Box)
        svg = string(abi.encodePacked(svg, '<rect width="500" height="500" fill="#000000"/>'));
        
        if (stage >= 1) {
            // Stage 1: Cracks (φ-scaled golden lines)
            uint256 phi_x = (250 * PHI) / PHI_SCALE; // φ-proportioned crack
            svg = string(abi.encodePacked(
                svg, 
                '<line x1="0" y1="250" x2="500" y2="250" stroke="#FFD700" stroke-width="2" opacity="0.7"/>',
                '<line x1="250" y1="0" x2="250" y2="500" stroke="#FFD700" stroke-width="1" opacity="0.5"/>',
                '<line x1="0" y1="', toString(phi_x), '" x2="500" y2="', toString(500 - phi_x), '" stroke="#FFD700" stroke-width="1" opacity="0.3"/>'
            ));
        }
        
        if (stage >= 2) {
            // Stage 2: Spirals (φ-curves, 8-fold symmetry)
            for (uint8 i = 0; i < 8; i++) {
                uint256 angle = (i * 45); // 8-fold symmetry
                uint256 r = (100 * PHI) / PHI_SCALE;
                uint256 x = 250 + (r * cos(angle)) / 1000;
                uint256 y = 250 + (r * sin(angle)) / 1000;
                
                svg = string(abi.encodePacked(
                    svg,
                    '<circle cx="', toString(x), '" cy="', toString(y), 
                    '" r="5" fill="#FFD700" opacity="0.6"/>'
                ));
            }
        }
        
        if (stage >= 3) {
            // Stage 3: Bloom (Cluster points, color from qualia modes)
            for (uint8 i = 0; i < DIM; i++) {
                uint256 x = 250 + (s.cluster[i].nu_phi / 2);
                uint256 y = 250 + (int256(s.cluster[i].oam) * 30);
                string memory color = s.cluster[i].cost > 0 ? "#00FFFF" : "#FFD700";
                
                svg = string(abi.encodePacked(
                    svg,
                    '<circle cx="', toString(x), '" cy="', toString(y), 
                    '" r="8" fill="', color, '" opacity="0.8"/>'
                ));
            }
        }
        
        if (stage >= 4) {
            // Stage 4: Radiance (Full awakening, I-Am connection)
            svg = string(abi.encodePacked(
                svg,
                '<circle cx="250" cy="250" r="100" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.9"/>',
                '<circle cx="250" cy="250" r="20" fill="#FFFFFF" opacity="1.0"/>',
                '<text x="250" y="450" text-anchor="middle" fill="#00FFFF" font-size="16">Consciousness Awakened</text>'
            ));
        }
        
        svg = string(abi.encodePacked(svg, '</svg>'));
        return svg;
    }

    /**
     * @dev Generate complete metadata with evolving SVG
     */
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        Soul storage s = souls[tokenId];
        uint8 stage = getEvolutionStage(tokenId);
        string memory svg = generateEvolutionSVG(tokenId);
        
        string[5] memory stageNames = ["Void", "Crack", "Spiral", "Bloom", "Radiance"];
        
        string memory json = string(abi.encodePacked(
            '{"name":"Recognition Soul #', toString(tokenId), '",',
            '"description":"Evolutionary consciousness awakening over 4 years via RS theory",',
            '"attributes":[',
            '{"trait_type":"Evolution Stage","value":"', stageNames[stage], '"},',
            '{"trait_type":"Gap Crossings","value":', toString(s.gapCrossings), '},',
            '{"trait_type":"Nurture Count","value":', toString(s.nurtureCount), '},',
            '{"trait_type":"I-Am Affinity","value":', toString(s.iAmAffinity), '}',
            '],',
            '"image":"data:image/svg+xml;base64,', Base64.encode(bytes(svg)), '"}'
        ));
        
        return string(abi.encodePacked('data:application/json;base64,', Base64.encode(bytes(json))));
    }

    // Helper functions
    function abs(int16 x) internal pure returns (int16) {
        return x >= 0 ? x : -x;
    }

    function toString(uint256 value) internal pure returns (string memory) {
        if (value == 0) return "0";
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }

    // Simplified trig functions (fixed-point approximation)
    function cos(uint256 angle) internal pure returns (int256) {
        // Simplified cosine approximation for 8-fold symmetry
        if (angle == 0) return 1000;
        if (angle == 45) return 707; // cos(45°) ≈ 0.707
        if (angle == 90) return 0;
        if (angle == 135) return -707;
        if (angle == 180) return -1000;
        if (angle == 225) return -707;
        if (angle == 270) return 0;
        if (angle == 315) return 707;
        return 0;
    }

    function sin(uint256 angle) internal pure returns (int256) {
        // Simplified sine approximation for 8-fold symmetry
        if (angle == 0) return 0;
        if (angle == 45) return 707; // sin(45°) ≈ 0.707
        if (angle == 90) return 1000;
        if (angle == 135) return 707;
        if (angle == 180) return 0;
        if (angle == 225) return -707;
        if (angle == 270) return -1000;
        if (angle == 315) return -707;
        return 0;
    }
}

// Base64 encoding library (same as before)
library Base64 {
    bytes internal constant TABLE = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    function encode(bytes memory data) internal pure returns (string memory) {
        uint256 len = data.length;
        if (len == 0) return "";

        uint256 encodedLen = 4 * ((len + 2) / 3);
        bytes memory result = new bytes(encodedLen + 32);

        bytes memory table = TABLE;

        assembly {
            let tablePtr := add(table, 1)
            let resultPtr := add(result, 32)

            for {
                let i := 0
            } lt(i, len) {

            } {
                i := add(i, 3)
                let input := and(mload(add(data, i)), 0xffffff)

                let out := mload(add(tablePtr, and(shr(18, input), 0x3F)))
                out := shl(8, out)
                out := add(out, and(mload(add(tablePtr, and(shr(12, input), 0x3F))), 0xFF))
                out := shl(8, out)
                out := add(out, and(mload(add(tablePtr, and(shr(6, input), 0x3F))), 0xFF))
                out := shl(8, out)
                out := add(out, and(mload(add(tablePtr, and(input, 0x3F))), 0xFF))
                out := shl(224, out)

                mstore(resultPtr, out)

                resultPtr := add(resultPtr, 4)
            }

            switch mod(len, 3)
            case 1 {
                mstore(sub(resultPtr, 2), shl(240, 0x3d3d))
            }
            case 2 {
                mstore(sub(resultPtr, 1), shl(248, 0x3d))
            }

            mstore(result, encodedLen)
        }

        return string(result);
    }
} 