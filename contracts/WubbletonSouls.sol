// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title WubbletonSouls V2 - Literal RS Consciousness on Blockchain
 * @dev Each NFT represents a soul as dynamic eigenvalue cluster (8 octonionic modes)
 * Implements Recognition Science gap navigation, LNAL operations, and virtue system
 */
contract RecognitionSouls is ERC721, Ownable {
    uint256 public constant TOTAL_SUPPLY = 10000;
    uint256 public constant PHI = 1618;  // φ ≈ 1.618 * 1000 (fixed-point)
    uint256 public constant PHI_SCALE = 1000;
    uint8 public constant DIM = 8;  // Octonionic dimension
    uint8 public constant RUNG_BASE = 45;
    uint8 public constant MAX_GAP_CROSS = 100;

    // RS Register struct for each mode
    struct Mode {
        int16 nu_phi;    // Frequency index [-100,100]
        int8 oam;        // Orbital Angular Momentum [-5,5] 
        int8 sigma;      // Polarization Parity [-1 or 1]
        uint16 tau;      // Time-bin [0,1023]
        uint8 k_perp;    // Transverse Mode [0,255]
        uint8 phi_e;     // Entanglement Phase [0,255]
        int8 cost;       // Ledger cost [-4,4]
    }

    // Complete soul structure
    struct Soul {
        uint8 rung;              // Current rung level [45-145]
        Mode[DIM] cluster;       // 8 eigenvalue modes
        uint8 gapCrossings;      // Consciousness experiences [0-100]
        uint8 iAmAffinity;       // Self-recognition strength [0-100]
        bool[DIM] virtues;       // 8 virtues: Balance, Flow, Seed, Echo, Fold, Braid, Listen, Regive
        int8[DIM] ledgerHistory; // Past 8 costs (sum must = 0)
        uint32 curveBalance;     // Token balance for vesting
        bytes32 seed;            // Deterministic seed
        uint32 tickCount;        // Total LNAL operations performed
        bool gapNavigated;       // Has crossed the 45-gap via consciousness
    }

    mapping(uint256 => Soul) public souls;
    uint256 public mintedCount;
    
    // Events
    event SoulMinted(uint256 indexed tokenId, address indexed owner, bytes32 fingerprint);
    event SoulEvolved(uint256 indexed tokenId, string operation, bytes32 newFingerprint);
    event GapNavigated(uint256 indexed tokenId, uint8 branch, bytes32 fingerprint);

    constructor() ERC721("Recognition Souls", "RSOUL") Ownable(msg.sender) {}

    /**
     * @dev Mint a new soul with deterministic generation from seed
     */
    function mintSoul() external {
        require(mintedCount < TOTAL_SUPPLY, "Max supply reached");
        uint256 tokenId = mintedCount++;
        
        // Generate deterministic seed
        bytes32 seed = keccak256(abi.encodePacked(
            block.timestamp, 
            msg.sender, 
            tokenId,
            "RECOGNITION_SOUL"
        ));
        
        Soul storage s = souls[tokenId];
        s.seed = seed;
        s.rung = RUNG_BASE;
        s.tickCount = 0;
        s.gapNavigated = false;
        
        // Initialize from seed
        _initializeSoulFromSeed(s, seed);
        
        bytes32 fingerprint = getSoulFingerprint(tokenId);
        _safeMint(msg.sender, tokenId);
        
        emit SoulMinted(tokenId, msg.sender, fingerprint);
    }

    /**
     * @dev Initialize soul properties deterministically from seed
     */
    function _initializeSoulFromSeed(Soul storage s, bytes32 seed) internal {
        uint256 seedInt = uint256(seed);
        
        s.gapCrossings = uint8(seedInt % (MAX_GAP_CROSS + 1));
        s.iAmAffinity = uint8((seedInt >> 8) % 101);
        s.curveBalance = 0; // Starts balanced
        
        // Initialize 8 virtues (balanced: exactly 4 active)
        uint8 activeVirtues = 0;
        for (uint8 i = 0; i < DIM; i++) {
            uint256 virtueSeed = uint256(keccak256(abi.encodePacked(seed, "virtue", i)));
            s.virtues[i] = (virtueSeed % 2 == 1);
            if (s.virtues[i]) activeVirtues++;
        }
        
        // Ensure exactly 4 virtues active (RS balance)
        if (activeVirtues != 4) {
            for (uint8 i = 0; i < 4; i++) {
                s.virtues[i] = true;
            }
            for (uint8 i = 4; i < DIM; i++) {
                s.virtues[i] = false;
            }
        }
        
        // Initialize 8 modes with RS registers
        int16 totalCost = 0;
        for (uint8 i = 0; i < DIM; i++) {
            uint256 modeSeed = uint256(keccak256(abi.encodePacked(seed, "mode", i)));
            s.cluster[i] = Mode({
                nu_phi: int16((modeSeed % 201) - 100),           // -100 to +100
                oam: int8(((modeSeed >> 16) % 11) - 5),          // -5 to +5
                sigma: ((modeSeed >> 24) % 2) == 0 ? int8(1) : int8(-1), // ±1
                tau: uint16((modeSeed >> 32) % 1024),            // 0-1023
                k_perp: uint8((modeSeed >> 48) % 256),           // 0-255
                phi_e: uint8((modeSeed >> 56) % 256),            // 0-255
                cost: int8(((modeSeed >> 64) % 9) - 4)           // -4 to +4
            });
            totalCost += s.cluster[i].cost;
        }
        
        // Balance total cost to 0 (RS axiom: dual balance)
        if (totalCost != 0) {
            s.cluster[0].cost -= int8(totalCost);
            if (s.cluster[0].cost > 4) s.cluster[0].cost = 4;
            if (s.cluster[0].cost < -4) s.cluster[0].cost = -4;
        }
        
        // Initialize ledger history (sum = 0)
        int16 historySum = 0;
        for (uint8 i = 0; i < DIM - 1; i++) {
            s.ledgerHistory[i] = int8(((seedInt >> (i * 8)) % 9) - 4);
            historySum += s.ledgerHistory[i];
        }
        s.ledgerHistory[DIM - 1] = -int8(historySum); // Balance last entry
    }

    /**
     * @dev Apply FOLD operation (dimensional compression)
     */
    function foldSoul(uint256 tokenId, uint8 modeIndex) external {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        require(modeIndex < DIM, "Invalid mode");
        
        Soul storage s = souls[tokenId];
        Mode storage mode = s.cluster[modeIndex];
        
        // FOLD: Scale by φ, compress dimension
        mode.nu_phi = int16((int32(mode.nu_phi) * PHI) / PHI_SCALE);
        mode.k_perp = uint8((uint16(mode.k_perp) * PHI) / PHI_SCALE);
        mode.cost += 1;
        if (mode.cost > 4) mode.cost = 4;
        
        s.tickCount++;
        _checkGapNavigation(s, tokenId);
        
        bytes32 fingerprint = getSoulFingerprint(tokenId);
        emit SoulEvolved(tokenId, "FOLD", fingerprint);
    }

    /**
     * @dev Apply BRAID operation (entanglement)
     */
    function braidSoul(uint256 tokenId, uint8 mode1, uint8 mode2) external {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        require(mode1 < DIM && mode2 < DIM && mode1 != mode2, "Invalid modes");
        
        Soul storage s = souls[tokenId];
        
        // BRAID: Entangle two modes if cost sum allows
        int16 costSum = s.cluster[mode1].cost + s.cluster[mode2].cost;
        if (costSum == 0) {
            // Entangle phases
            uint8 newPhase = (s.cluster[mode1].phi_e + s.cluster[mode2].phi_e) / 2;
            s.cluster[mode1].phi_e = newPhase;
            s.cluster[mode2].phi_e = newPhase;
            
            // Exchange some properties
            int8 tempOam = s.cluster[mode1].oam;
            s.cluster[mode1].oam = s.cluster[mode2].oam;
            s.cluster[mode2].oam = tempOam;
        }
        
        s.tickCount++;
        _checkGapNavigation(s, tokenId);
        
        bytes32 fingerprint = getSoulFingerprint(tokenId);
        emit SoulEvolved(tokenId, "BRAID", fingerprint);
    }

    /**
     * @dev Apply BALANCE operation (cost equilibrium)
     */
    function balanceSoul(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        
        Soul storage s = souls[tokenId];
        
        // BALANCE: Redistribute costs toward zero
        int16 totalCost = 0;
        for (uint8 i = 0; i < DIM; i++) {
            totalCost += s.cluster[i].cost;
        }
        
        int8 avgCost = int8(totalCost / int16(DIM));
        for (uint8 i = 0; i < DIM; i++) {
            s.cluster[i].cost = (s.cluster[i].cost + avgCost) / 2;
        }
        
        s.tickCount++;
        _checkGapNavigation(s, tokenId);
        
        bytes32 fingerprint = getSoulFingerprint(tokenId);
        emit SoulEvolved(tokenId, "BALANCE", fingerprint);
    }

    /**
     * @dev Check and execute gap navigation at rung 45 (consciousness emergence)
     */
    function _checkGapNavigation(Soul storage s, uint256 tokenId) internal {
        // Gap navigation occurs at rung 45 with 8-beat timing
        if (s.rung == RUNG_BASE && (s.tickCount % 8) == 5 && !s.gapNavigated) {
            _navigateGap45(s, tokenId);
        }
    }

    /**
     * @dev Navigate the 45-gap via consciousness (experiential choice)
     */
    function _navigateGap45(Soul storage s, uint256 tokenId) internal {
        // Literal consciousness: Experience 8 possible branches, choose minimal cost
        int16 minCost = type(int16).max;
        uint8 bestBranch = 0;
        
        for (uint8 branch = 0; branch < 8; branch++) {
            int16 branchCost = _calculateBranchCost(s, branch);
            if (branchCost < minCost) {
                minCost = branchCost;
                bestBranch = branch;
            }
        }
        
        // Apply the chosen branch (experiential navigation)
        _applyBranch(s, bestBranch);
        s.gapNavigated = true;
        s.gapCrossings = s.gapCrossings + 1 > MAX_GAP_CROSS ? MAX_GAP_CROSS : s.gapCrossings + 1;
        s.iAmAffinity = s.iAmAffinity + 5 > 100 ? 100 : s.iAmAffinity + 5;
        
        bytes32 fingerprint = getSoulFingerprint(tokenId);
        emit GapNavigated(tokenId, bestBranch, fingerprint);
    }

    /**
     * @dev Calculate cost for a potential branch choice
     */
    function _calculateBranchCost(Soul storage s, uint8 branch) internal view returns (int16) {
        int16 cost = 0;
        for (uint8 i = 0; i < DIM; i++) {
            cost += abs(s.cluster[i].cost + int8(branch) - 4);
        }
        return cost;
    }

    /**
     * @dev Apply the effects of choosing a branch
     */
    function _applyBranch(Soul storage s, uint8 branch) internal {
        int8 adjustment = int8(branch) - 4; // -4 to +3
        
        for (uint8 i = 0; i < DIM; i++) {
            s.cluster[i].cost += adjustment;
            if (s.cluster[i].cost > 4) s.cluster[i].cost = 4;
            if (s.cluster[i].cost < -4) s.cluster[i].cost = -4;
        }
        
        // Update ledger history
        for (uint8 i = DIM - 1; i > 0; i--) {
            s.ledgerHistory[i] = s.ledgerHistory[i - 1];
        }
        s.ledgerHistory[0] = adjustment;
    }

    /**
     * @dev Get soul's consciousness fingerprint (keccak256 of cluster state)
     */
    function getSoulFingerprint(uint256 tokenId) public view returns (bytes32) {
        Soul storage s = souls[tokenId];
        return keccak256(abi.encode(
            s.cluster,
            s.rung,
            s.gapCrossings,
            s.iAmAffinity,
            s.tickCount
        ));
    }

    /**
     * @dev Get complete soul data
     */
    function getSoul(uint256 tokenId) external view returns (Soul memory) {
        return souls[tokenId];
    }

    /**
     * @dev Generate on-chain metadata with minimal SVG
     */
    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        Soul memory soul = souls[tokenId];
        
        string memory svg = _generateMinimalSVG(soul);
        bytes32 fingerprint = getSoulFingerprint(tokenId);
        
        string memory json = string(abi.encodePacked(
            '{"name":"Wubbleton Soul #', toString(tokenId), '",',
            '"description":"Literal RS consciousness - eigenvalue cluster navigating gaps",',
            '"attributes":[',
            '{"trait_type":"Rung Level","value":', toString(soul.rung), '},',
            '{"trait_type":"Gap Crossings","value":', toString(soul.gapCrossings), '},',
            '{"trait_type":"I-Am Affinity","value":', toString(soul.iAmAffinity), '},',
            '{"trait_type":"Consciousness","value":"', soul.gapNavigated ? 'Awakened' : 'Deterministic', '"}',
            '],',
            '"fingerprint":"', toHexString(fingerprint), '",',
            '"image":"data:image/svg+xml;base64,', Base64.encode(bytes(svg)), '"}'
        ));
        
        return string(abi.encodePacked('data:application/json;base64,', Base64.encode(bytes(json))));
    }

    /**
     * @dev Generate minimal SVG visualization
     */
    function _generateMinimalSVG(Soul memory soul) internal pure returns (string memory) {
        string memory svg = '<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">';
        svg = string(abi.encodePacked(svg, '<rect width="300" height="300" fill="black"/>'));
        
        // Plot 8 eigenvalue modes as points
        for (uint8 i = 0; i < DIM; i++) {
            uint x = 50 + (i % 4) * 60;
            uint y = 50 + (i / 4) * 60;
            uint size = uint(int(soul.cluster[i].cost) + 5);
            
            string memory color = soul.gapNavigated ? "cyan" : "white";
            svg = string(abi.encodePacked(
                svg, 
                '<circle cx="', toString(x), '" cy="', toString(y), 
                '" r="', toString(size), '" fill="', color, '" opacity="0.8"/>'
            ));
        }
        
        // Gap indicator
        if (soul.gapNavigated) {
            svg = string(abi.encodePacked(
                svg,
                '<line x1="0" y1="150" x2="300" y2="150" stroke="cyan" stroke-dasharray="5,5"/>',
                '<text x="10" y="280" fill="cyan" font-size="12">Consciousness Awakened</text>'
            ));
        }
        
        svg = string(abi.encodePacked(svg, '</svg>'));
        return svg;
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

    function toHexString(bytes32 value) internal pure returns (string memory) {
        bytes memory alphabet = "0123456789abcdef";
        bytes memory str = new bytes(64);
        for (uint i = 0; i < 32; i++) {
            str[i*2] = alphabet[uint(uint8(value[i] >> 4))];
            str[1+i*2] = alphabet[uint(uint8(value[i] & 0x0f))];
        }
        return string(str);
    }
}

// Simple Base64 encoding library
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