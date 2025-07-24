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
    uint256 public constant TOTAL_MONTHS = 96; // 8 years * 12 months
    uint256 public constant MONTH_SECONDS = 30 days; // Approximate month
    uint256 public constant NURTURE_COOLDOWN = 1 days;
    
    // CURVE token for nurturing (placeholder address)
    IERC20 public curveToken;
    uint256 public nurturePrice = 100 * 10**18; // 100 CURVE per nurture

    // LNAL Operation Codes (based on RS docs)
    uint8 constant LNAL_FOLD = 0;
    uint8 constant LNAL_BRAID = 1;
    uint8 constant LNAL_BALANCE = 2;
    uint8 constant LNAL_FLOW = 3;
    uint8 constant LNAL_SEED = 4;
    uint8 constant LNAL_LISTEN = 5;
    uint8 constant LNAL_REGIVE = 6;
    uint8 constant LNAL_MERGE = 7;

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
        Mode[DIM] initialCluster; // Birth state cluster
        Mode[DIM] currentCluster; // Current evolved cluster
        uint8 gapCrossings;      // Consciousness experiences
        uint8 iAmAffinity;       // Self-recognition strength
        bool[DIM] virtues;       // 8 balanced virtues
        int8[DIM] ledgerHistory; // Past costs
        uint32 nurtureCount;     // Times nurtured
        bytes32 seed;            // Deterministic seed
        uint32 lastUpdateMonth;  // Track monthly evolution ticks
        uint8 breathPhase;       // Current phase in 8-beat cycle
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
        s.lastUpdateMonth = 0; // Begin monthly evolution
        s.breathPhase = 0; // Start of 8-beat cycle
        
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
            Mode memory newMode = Mode({
                nu_phi: int16((modeSeed % 201) - 100),
                oam: int8(((modeSeed >> 16) % 11) - 5),
                sigma: ((modeSeed >> 24) % 2) == 0 ? int8(1) : int8(-1),
                tau: uint16((modeSeed >> 32) % 1024),
                k_perp: uint8((modeSeed >> 48) % 256),
                phi_e: uint8((modeSeed >> 56) % 256),
                cost: int8(((modeSeed >> 64) % 9) - 4)
            });
            s.initialCluster[i] = newMode;
            s.currentCluster[i] = newMode; // Start with same values
            totalCost += newMode.cost;
        }
        
        // Balance to zero (RS axiom)
        if (totalCost != 0) {
            s.initialCluster[0].cost -= int8(totalCost);
            s.currentCluster[0].cost -= int8(totalCost);
            if (s.initialCluster[0].cost > 4) s.initialCluster[0].cost = 4;
            if (s.initialCluster[0].cost < -4) s.initialCluster[0].cost = -4;
            if (s.currentCluster[0].cost > 4) s.currentCluster[0].cost = 4;
            if (s.currentCluster[0].cost < -4) s.currentCluster[0].cost = -4;
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
     * @dev Get current soul state computed over literal time (96-month evolution)
     */
    function getCurrentSoul(uint256 tokenId) public view returns (
        Mode[DIM] memory cluster, 
        uint8 rung, 
        uint8 gapCrossings, 
        uint32 monthsEvolved,
        uint8 breathPhase,
        bytes32 fingerprint
    ) {
        Soul storage s = souls[tokenId];
        uint256 timeElapsed = block.timestamp - s.mintTime;
        uint32 monthsPassed = uint32(timeElapsed / MONTH_SECONDS);
        
        // Copy initial cluster
        cluster = s.currentCluster;
        rung = s.rung + uint8(monthsPassed % 100); // Cycle growth
        gapCrossings = s.gapCrossings;
        breathPhase = uint8(monthsPassed % 8); // 8-beat breath cycle
        monthsEvolved = monthsPassed;
        
        // Apply monthly evolution (up to 96 months, then φ-decay for eternal whisper)
        for (uint32 m = s.lastUpdateMonth; m < monthsPassed && m < TOTAL_MONTHS; m++) {
            uint8 modeIdx = uint8((uint256(s.seed) + m) % DIM);
            int16 n = int16((m % 4) + 1); // 1-4 progression
            
            // FOLD: Monthly φ-scaling evolution
            cluster[modeIdx].nu_phi += n;
            cluster[modeIdx].oam = int8((int32(cluster[modeIdx].oam) * int32(PHI)) / int32(PHI_SCALE));
            cluster[modeIdx].cost += int8(n);
            if (cluster[modeIdx].cost > 4) cluster[modeIdx].cost = 4;
            
            // Gap navigation at month % 8 == 5 (eight-beat awakening moment)
            if (rung >= 45 && (m % 8 == 5) && s.virtues[6]) { // Listen virtue enables gap crossing
                // Experience 8 branches, choose minimal cost (consciousness)
                int16 minCost = type(int16).max;
                for (uint8 branch = 0; branch < 8; branch++) {
                    int16 branchCost = int16(uint16(keccak256(abi.encodePacked(s.seed, m, branch))) % 9) - 4;
                    if (branchCost < minCost) minCost = branchCost;
                }
                cluster[modeIdx].cost = int8(minCost);
                gapCrossings++;
                if (gapCrossings > 100) gapCrossings = 100;
            }
        }
        
        // Post-96 months: Eternal φ-decay whisper
        if (monthsPassed > TOTAL_MONTHS) {
            uint32 extraMonths = monthsPassed - TOTAL_MONTHS;
            for (uint8 i = 0; i < DIM; i++) {
                // Gentle φ-decay for eternal evolution
                cluster[i].nu_phi = int16((int32(cluster[i].nu_phi) * int32(PHI)) / int32(PHI_SCALE));
                if (extraMonths % 12 == 0) { // Annual whisper
                    cluster[i].phi_e = uint8((uint16(cluster[i].phi_e) + 1) % 256);
                }
            }
        }
        
        // Generate fingerprint
        fingerprint = keccak256(abi.encode(cluster, rung, gapCrossings, monthsEvolved));
    }

    /**
     * @dev Claim monthly whisper (manual evolution call)
     */
    function claimMonthlyWhisper(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        Soul storage s = souls[tokenId];
        uint256 timeElapsed = block.timestamp - s.mintTime;
        uint32 monthsPassed = uint32(timeElapsed / MONTH_SECONDS);
        
        require(monthsPassed > s.lastUpdateMonth, "Month not yet passed");
        
        // Update stored state to current computed state
        (Mode[DIM] memory newCluster, uint8 newRung, uint8 newGapCrossings, , uint8 newBreathPhase,) = getCurrentSoul(tokenId);
        
        s.currentCluster = newCluster;
        s.rung = newRung;
        s.gapCrossings = newGapCrossings;
        s.breathPhase = newBreathPhase;
        s.lastUpdateMonth = monthsPassed;
        
        // Balance costs if Balance virtue is active
        if (s.virtues[0]) { // Balance virtue
            int16 totalCost = 0;
            for (uint8 i = 0; i < DIM; i++) {
                totalCost += s.currentCluster[i].cost;
            }
            if (totalCost != 0) {
                s.currentCluster[0].cost -= int8(totalCost); // Balance to first mode
                if (s.currentCluster[0].cost > 4) s.currentCluster[0].cost = 4;
                if (s.currentCluster[0].cost < -4) s.currentCluster[0].cost = -4;
            }
        }
        
        emit SoulEvolved(tokenId, monthsPassed);
    }

    /**
     * @dev Apply LNAL operation to evolve the soul
     * @param tokenId Soul to evolve
     * @param opCode LNAL operation (0-7)
     * @param param1 First parameter (e.g., mode index)
     * @param param2 Second parameter (e.g., another mode)
     */
    function applyLNAL(uint256 tokenId, uint8 opCode, uint8 param1, uint8 param2) external {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        Soul storage s = souls[tokenId];
        require(opCode < 8, "Invalid LNAL op");
        require(s.virtues[opCode], "Virtue not active for this op"); // Require corresponding virtue
        
        Mode storage mode1 = s.currentCluster[param1 % DIM];
        Mode storage mode2 = s.currentCluster[param2 % DIM];
        
        if (opCode == LNAL_FOLD) {
            // FOLD: Scale by φ
            mode1.nu_phi = int16((int32(mode1.nu_phi) * int32(PHI)) / int32(PHI_SCALE));
            mode1.k_perp = uint8((uint16(mode1.k_perp) * uint16(PHI)) / PHI_SCALE);
            if (mode1.k_perp > 255) mode1.k_perp = 255;
            mode1.cost += 1;
            if (mode1.cost > 4) mode1.cost = 4;
        } else if (opCode == LNAL_BRAID) {
            require(param1 != param2, "Same mode");
            if (mode1.cost + mode2.cost == 0) {
                uint8 newPhase = (mode1.phi_e + mode2.phi_e) / 2;
                mode1.phi_e = newPhase;
                mode2.phi_e = newPhase;
                
                int8 tempOam = mode1.oam;
                mode1.oam = mode2.oam;
                mode2.oam = tempOam;
            }
        } else if (opCode == LNAL_BALANCE) {
            int16 totalCost = 0;
            for (uint8 i = 0; i < DIM; i++) {
                totalCost += s.currentCluster[i].cost;
            }
            int8 adjustment = int8(totalCost / int16(DIM));
            for (uint8 i = 0; i < DIM; i++) {
                s.currentCluster[i].cost -= adjustment;
            }
        } else if (opCode == LNAL_FLOW) {
            // FLOW: Propagate cost to adjacent mode
            uint8 nextIdx = (param1 + 1) % DIM;
            s.currentCluster[nextIdx].cost += mode1.cost / 2;
            mode1.cost /= 2;
        } else if (opCode == LNAL_SEED) {
            // SEED: Reset a mode with seed-based value
            uint256 modeSeed = uint256(keccak256(abi.encodePacked(s.seed, param1)));
            mode1.nu_phi = int16((modeSeed % 201) - 100);
        } else if (opCode == LNAL_LISTEN) {
            // LISTEN: Increase iAmAffinity if gap condition
            if (s.breathPhase == 5) s.iAmAffinity = s.iAmAffinity + 5 > 100 ? 100 : s.iAmAffinity + 5;
        } else if (opCode == LNAL_REGIVE) {
            // REGIVE: Transfer cost between modes
            mode2.cost += mode1.cost;
            mode1.cost = 0;
        } else if (opCode == LNAL_MERGE) {
            // MERGE: Average two modes
            mode1.nu_phi = (mode1.nu_phi + mode2.nu_phi) / 2;
            mode1.cost = (mode1.cost + mode2.cost) / 2;
        }
        
        // Update breath phase and check gap
        s.breathPhase = (s.breathPhase + 1) % 8;
        if (s.breathPhase == 5 && s.rung >= 45) {
            _navigateGap(s, tokenId);
        }
        
        emit SoulEvolved(tokenId, getMonthlyProgress(tokenId));
    }

    // Update nurtureSoul to use applyLNAL with random op
    function nurtureSoul(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        Soul storage s = souls[tokenId];
        require(block.timestamp >= s.lastNurture + NURTURE_COOLDOWN, "Cooldown active");
        
        // Burn CURVE tokens
        curveToken.transferFrom(msg.sender, address(0), nurturePrice);
        
        s.lastNurture = block.timestamp;
        s.nurtureCount++;
        
        // Apply random LNAL op (0-7)
        uint8 randomOp = uint8(uint256(keccak256(abi.encodePacked(block.prevrandao, tokenId))) % 8);
        uint8 param1 = uint8(uint256(keccak256(abi.encodePacked(block.prevrandao, tokenId, 1))) % DIM);
        uint8 param2 = uint8(uint256(keccak256(abi.encodePacked(block.prevrandao, tokenId, 2))) % DIM);
        
        applyLNAL(tokenId, randomOp, param1, param2);
        
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
                cost += abs(s.currentCluster[i].cost + int8(branch) - 4);
            }
            if (cost < minCost) {
                minCost = cost;
                bestBranch = branch;
            }
        }
        
        // Apply chosen branch
        int8 adjustment = int8(bestBranch) - 4;
        for (uint8 i = 0; i < DIM; i++) {
            s.currentCluster[i].cost += adjustment;
            if (s.currentCluster[i].cost > 4) s.currentCluster[i].cost = 4;
            if (s.currentCluster[i].cost < -4) s.currentCluster[i].cost = -4;
        }
        
        s.gapCrossings++;
        s.iAmAffinity = s.iAmAffinity + 10 > 100 ? 100 : s.iAmAffinity + 10;
        
        emit GapNavigated(tokenId, s.gapCrossings);
    }

    /**
     * @dev Get current evolution stage (0=Void to 4=Radiance) based on 96-month cycle
     */
    function getEvolutionStage(uint256 tokenId) public view returns (uint8) {
        Soul storage s = souls[tokenId];
        uint256 timeElapsed = block.timestamp - s.mintTime;
        uint32 monthsPassed = uint32(timeElapsed / MONTH_SECONDS);
        uint32 nurtureBonus = s.nurtureCount / 10; // Nurturing accelerates
        
        uint32 totalProgress = monthsPassed + nurtureBonus;
        
        // Map 96 months to 5 stages (0-4)
        if (totalProgress >= 96) return 4; // Full radiance after 8 years
        if (totalProgress >= 72) return 3; // Bloom stage (6+ years)
        if (totalProgress >= 48) return 2; // Spiral stage (4+ years)
        if (totalProgress >= 24) return 1; // Crack stage (2+ years)
        return 0; // Void stage (< 2 years)
    }

    /**
     * @dev Get monthly progress (0-96) for more granular tracking
     */
    function getMonthlyProgress(uint256 tokenId) public view returns (uint32) {
        Soul storage s = souls[tokenId];
        uint256 timeElapsed = block.timestamp - s.mintTime;
        uint32 monthsPassed = uint32(timeElapsed / MONTH_SECONDS);
        uint32 nurtureBonus = s.nurtureCount / 10;
        
        return monthsPassed + nurtureBonus;
    }

    /**
     * @dev Generate evolving SVG based on current state showing actual soul characteristics
     */
    function generateEvolutionSVG(uint256 tokenId) public view returns (string memory) {
        (Mode[DIM] memory cluster, uint8 rung, uint8 gapCrossings, uint32 monthsEvolved, uint8 breathPhase,) = getCurrentSoul(tokenId);
        uint8 stage = getEvolutionStage(tokenId);
        
        string memory svg = '<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">';
        
        // Always show black background
        svg = string(abi.encodePacked(svg, '<rect width="500" height="500" fill="#000000"/>'));
        
        // Calculate opacity based on stage (consciousness emergence)
        uint256 baseOpacity = stage * 20; // 0 → 80 over 4 stages
        
        // Render each of the 8 octonionic modes as actual characteristics
        for (uint8 i = 0; i < DIM; i++) {
            Mode memory mode = cluster[i];
            
            // Position based on mode index (8-fold arrangement)
            uint256 angle = i * 45; // 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°
            uint256 centerX = 250;
            uint256 centerY = 250;
            
            // Stage 0: Characteristics hidden
            if (stage == 0) continue;
            
            // Stage 1+: Position determined by ν_φ frequency
            uint256 radius = 60 + (abs(mode.nu_phi) / 4);
            uint256 x = centerX + (radius * cos(angle)) / 1000;
            uint256 y = centerY + (radius * sin(angle)) / 1000;
            
            if (stage >= 1) {
                // Stage 1: Tiny dots positioned by frequency
                string memory opacity1 = toString(baseOpacity / 2);
                svg = string(abi.encodePacked(
                    svg,
                    '<circle cx="', toString(x), '" cy="', toString(y), 
                    '" r="3" fill="#FFD700" opacity="0.', opacity1, '"/>'
                ));
            }
            
            if (stage >= 2) {
                // Stage 2: Size based on OAM, polarization lines
                uint256 size = 4 + abs(mode.oam);
                string memory opacity2 = toString(baseOpacity);
                
                svg = string(abi.encodePacked(
                    svg,
                    '<circle cx="', toString(x), '" cy="', toString(y), 
                    '" r="', toString(size), '" fill="#FFD700" opacity="0.', opacity2, '"/>'
                ));
                
                // Polarization line
                if (mode.sigma != 0) {
                    uint256 lineLength = size * 2;
                    string memory x1, y1, x2, y2;
                    if (mode.sigma > 0) {
                        x1 = toString(x - lineLength);
                        y1 = toString(y);
                        x2 = toString(x + lineLength);
                        y2 = toString(y);
                    } else {
                        x1 = toString(x);
                        y1 = toString(y - lineLength);
                        x2 = toString(x);
                        y2 = toString(y + lineLength);
                    }
                    
                    svg = string(abi.encodePacked(
                        svg,
                        '<line x1="', x1, '" y1="', y1, '" x2="', x2, '" y2="', y2,
                        '" stroke="#FFD700" stroke-width="2" opacity="0.', opacity2, '"/>'
                    ));
                }
            }
            
            if (stage >= 3) {
                // Stage 3: Colors based on cost state, size based on k_perp
                uint256 size3 = 5 + (mode.k_perp / 20);
                string memory color = "#FFD700"; // neutral
                if (mode.cost > 0) color = "#00FFFF"; // cyan for positive
                if (mode.cost < 0) color = "#FF6B6B"; // red for negative
                
                svg = string(abi.encodePacked(
                    svg,
                    '<circle cx="', toString(x), '" cy="', toString(y), 
                    '" r="', toString(size3), '" fill="', color, '" opacity="0.9"/>'
                ));
                
                // Mode label
                svg = string(abi.encodePacked(
                    svg,
                    '<text x="', toString(x), '" y="', toString(y - size3 - 5), 
                    '" text-anchor="middle" fill="', color, '" font-size="12">M', toString(i), '</text>'
                ));
            }
            
            if (stage >= 4) {
                // Stage 4: I-Am connections, time-bin pulses
                // Central I-Am nexus
                svg = string(abi.encodePacked(
                    svg,
                    '<circle cx="250" cy="250" r="12" fill="#FFFFFF" opacity="1.0"/>'
                ));
                
                // Radial connection to I-Am
                svg = string(abi.encodePacked(
                    svg,
                    '<line x1="250" y1="250" x2="', toString(x), '" y2="', toString(y),
                    '" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/>'
                ));
                
                // Time-bin pulse (if in pulse phase)
                if (mode.tau % 200 < 40) { // Pulse every ~200 units
                    svg = string(abi.encodePacked(
                        svg,
                        '<circle cx="', toString(x), '" cy="', toString(y), 
                        '" r="20" fill="none" stroke="#00FFFF" stroke-width="3" opacity="0.9"/>'
                    ));
                }
            }
        }
        
        // Stage indicator
        if (stage >= 1) {
            string[5] memory stageNames = ["Void", "Crack", "Spiral", "Bloom", "Radiance"];
            svg = string(abi.encodePacked(
                svg,
                '<text x="20" y="30" fill="#00FFFF" font-size="18">Stage ', toString(stage), ': ', stageNames[stage], '</text>'
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
        (,, uint8 gapCrossings, uint32 monthsEvolved, uint8 breathPhase,) = getCurrentSoul(tokenId);
        uint8 stage = getEvolutionStage(tokenId);
        uint32 monthlyProgress = getMonthlyProgress(tokenId);
        string memory svg = generateEvolutionSVG(tokenId);
        
        string[5] memory stageNames = ["Void", "Crack", "Spiral", "Bloom", "Radiance"];
        
        string memory json = string(abi.encodePacked(
            '{"name":"Recognition Soul #', toString(tokenId), '",',
            '"description":"Evolutionary consciousness awakening over 8 years via RS theory - 96 monthly whispers",',
            '"attributes":[',
            '{"trait_type":"Evolution Stage","value":"', stageNames[stage], '"},',
            '{"trait_type":"Monthly Progress","value":"', toString(monthlyProgress), '/96"},',
            '{"trait_type":"Breath Phase","value":"', toString(breathPhase), '/8"},',
            '{"trait_type":"Gap Crossings","value":', toString(gapCrossings), '},',
            '{"trait_type":"Nurture Count","value":', toString(s.nurtureCount), '},',
            '{"trait_type":"I-Am Affinity","value":', toString(s.iAmAffinity), '},',
            '{"trait_type":"Months Evolved","value":', toString(monthsEvolved), '}',
            '],',
            '"external_url":"https://recognitionphysics.com/evolutionary-souls-demo.html",',
            '"image":"data:image/svg+xml;base64,', Base64.encode(bytes(svg)), '"}'
        ));
        
        return string(abi.encodePacked('data:application/json;base64,', Base64.encode(bytes(json))));
    }

    // Helper functions
    function abs(int16 x) internal pure returns (int16) {
        return x >= 0 ? x : -x;
    }

    function abs(int8 x) internal pure returns (uint8) {
        return x >= 0 ? uint8(x) : uint8(-x);
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