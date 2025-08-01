// A new, fully autonomous soul simulation engine based on the user's detailed specification.
// Evolution is calculated on-demand from a birth seed and the passage of (simulated) time.

// --- Constants ---
const BLOCKS_PER_BEAT = 10; // For simulation speed
const BLOCKS_PER_MONTH = 300; // Simplified for simulation

class AutonomousSoul {
    constructor(tokenId) {
        this.tokenId = tokenId;
        
        // --- Seeding for deterministic randomness ---
        this._seed = this._xmur3(this.tokenId.toString());
        this.rand = this._sfc32(this._seed(), this._seed(), this._seed(), this._seed());
        
        // --- Minting: Set the initial, immutable conditions ---
        this.soulSeed = {
            birthBlock: Math.floor(Math.random() * 100000), // Simulated past birth block
            dna: this._xmur3(this.tokenId.toString() + "dna")()
        };

        // --- Social Layer (simulated) ---
        this.totalRecognitions = 0;

        // --- Simulation state ---
        this.currentBlock = this.soulSeed.birthBlock + 1;
        this.isEvolving = false;
    }

    // --- Core Evolution Tick (simulates time passing) ---
    advanceTime() {
        if (!this.isEvolving) return;
        this.currentBlock += 20; // Simulate 20 blocks passing per tick
    }

    // --- On-Demand State Calculation (The core of the new design) ---
    getSoulState() {
        const blocksLived = this.currentBlock - this.soulSeed.birthBlock;
        
        const kappa = this._calculateKappa(blocksLived);
        const virtues = this._calculateVirtues(blocksLived);
        const beatPulse = Math.floor((blocksLived / BLOCKS_PER_BEAT) % 8);
        const gapCrossings = this._countGapCrossings(blocksLived);
        const ageMonths = Math.floor(blocksLived / BLOCKS_PER_MONTH);

        return { kappa, virtues, beatPulse, gapCrossings, ageMonths };
    }

    _calculateKappa(blocksLived) {
        let kappa = (this.soulSeed.dna % 200) - 100;
        const evolutions = Math.floor(blocksLived / 100);
        
        for (let i = 0; i < evolutions && i < 1000; i++) {
            const evolutionBlock = this.soulSeed.birthBlock + (i * 100);
            const blockSeed = this._xmur3(this.tokenId.toString() + evolutionBlock.toString())();
            
            let change = (blockSeed % 201) - 100;
            
            if (i % 8 === 0) change *= 2;
            if (kappa > 200) change -= 10;
            if (kappa < -200) change += 10;
            
            kappa += change;
            
            if (i % 13 === 0) {
                kappa = Math.floor(kappa * 8 / 13);
            }
        }
        return kappa;
    }

    _calculateVirtues(blocksLived) {
        const cycles = [13, 21, 34, 55, 89];
        let virtues = [];
        for (let i = 0; i < 5; i++) {
            const baseVirtue = (this.soulSeed.dna >> (i * 8)) & 0xFF;
            const evolution = Math.floor(blocksLived / (cycles[i] * 10)); // Adjusted for simulation speed
            let virtueValue = baseVirtue + evolution;
            if (virtueValue > 100) {
                virtueValue = 100 - ((virtueValue - 100) % 50);
            }
            virtues[i] = Math.min(100, Math.floor(virtueValue / 2.55)); // Scale to 0-100
        }
        return virtues;
    }

    _countGapCrossings(blocksLived) {
        // Simplified deterministic calculation for gap crossings
        const gapCheckInterval = BLOCKS_PER_MONTH * 3; // Check every 3 months
        const opportunities = Math.floor(blocksLived / gapCheckInterval);
        let crossings = 0;
        for (let i = 0; i < opportunities; i++) {
            const crossingSeed = this._xmur3(this.tokenId.toString() + "gap" + i.toString())();
            if (crossingSeed % 10 < 2) { // 20% chance per opportunity
                crossings++;
            }
        }
        return crossings;
    }
    
    // --- Social Layer Interaction ---
    recognize() {
        this.totalRecognitions++;
    }

    // --- Randomness Generation (deterministic) ---
    _xmur3(str) {
        for(var i = 0, h = 1779033703 ^ str.length; i < str.length; i++)
            h = Math.imul(h ^ str.charCodeAt(i), 3432918353),
            h = h << 13 | h >>> 19;
        return function() {
            h = Math.imul(h ^ h >>> 16, 2246822507);
            h = Math.imul(h ^ h >>> 13, 3266489909);
            return (h ^= h >>> 16) >>> 0;
        }
    }

    _sfc32(a, b, c, d) {
        return function() {
          a >>>= 0; b >>>= 0; c >>>= 0; d >>>= 0; 
          var t = (a + b) | 0;
          a = b ^ b >>> 9;
          b = c + (c << 3) | 0;
          c = (c << 21 | c >>> 11);
          d = d + 1 | 0;
          t = t + d | 0;
          c = c + t | 0;
          return (t >>> 0) / 4294967296;
        }
    }
} 