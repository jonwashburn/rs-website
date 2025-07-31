class UnifiedSoul {
    constructor(tokenId) {
        this.tokenId = tokenId;
        this.nonce = 0;

        // --- Seeding for deterministic randomness ---
        this._seed = this._xmur3(this.tokenId.toString());
        this.rand = this._sfc32(this._seed(), this._seed(), this._seed(), this._seed());
        
        this.initializeState();
    }

    // --- State Initialization ---
    initializeState() {
        this.ticks = 0;
        this.months = 0;
        this.stage = 0; // 0:Void, 1:Crack, 2:Spiral, 3:Bloom, 4:Radiance
        this.phase = "New Spirit"; 
        this.isEvolving = false;
        
        this.kappa = this._randomInRange(-5, 5); // Recognition balance
        this.energy = this._randomInRange(800, 1000);
        this.maxEnergy = 1000;
        
        this.virtues = {
            love: this._randomInRange(1, 8),
            justice: this._randomInRange(1, 8),
            courage: this._randomInRange(1, 8),
            temperance: this._randomInRange(1, 8),
            prudence: this._randomInRange(1, 8)
        };
        
        // --- New properties based on V3 contract ---
        this.gapCrossings = 0;
        this.breathPhase = 0; // 0-7
        this.iAmAffinity = 0; // Self-recognition strength
        this.lnalHistory = [];
    }

    // --- LNAL Event Logger ---
    _logLNAL(instruction, params = "") {
        const entry = `${instruction.padEnd(8, ' ')} ${params}`;
        this.lnalHistory.unshift(entry); // Add to the beginning
        if (this.lnalHistory.length > 5) {
            this.lnalHistory.pop(); // Keep only the last 5 entries
        }
    }

    // --- Core Simulation Tick ---
    advanceTick() {
        if (!this.isEvolving) return;

        this.ticks++;
        this.months = Math.floor(this.ticks / 10);
        this.breathPhase = this.ticks % 8;

        // --- Stage Evolution (based on V3 contract) ---
        // 96 months mapped to 5 stages
        if (this.months >= 96) this.stage = 4; // Radiance
        else if (this.months >= 72) this.stage = 3; // Bloom
        else if (this.months >= 48) this.stage = 2; // Spiral
        else if (this.months >= 24) this.stage = 1; // Crack
        else this.stage = 0; // Void

        // --- Phase Transitions ---
        if (this.months >= 96) {
            this.phase = this.energy > 0 ? "Unified with IAM" : "Decohered";
            this.isEvolving = false;
        } else if (this.months > 1 && this.phase === "New Spirit") {
            this.phase = "Embodied";
        }
        if (this.phase === "Unified with IAM" || this.phase === "Decohered") return;

        // --- Energy Decay (modified by virtues) ---
        const temperanceEffect = (this.virtues.temperance / 10) * (this.energy / this.maxEnergy);
        const energyDecay = (0.5 + (this.virtues.courage / 12)) * (1 - temperanceEffect);
        this.energy -= Math.max(0.1, energyDecay);
        if (this.energy <= 0) {
            this.energy = 0;
            this.phase = "Decohered";
            this.isEvolving = false;
            this._logLNAL("DECOHERE");
            return;
        }

        // --- Kappa Fluctuation (modified by virtues) ---
        const volatility = 1 + (this.virtues.courage / 4);
        const drift = (this.virtues.justice - 4.5) / 8;
        this.kappa += (this.rand() - 0.5) * volatility + drift;
        this._logLNAL("BALANCE", `κ=${this.kappa.toFixed(2)}`);
        
        // --- Recognition Events (modified by virtues) ---
        const prudenceBonus = this.virtues.prudence / 150;
        if (this.rand() < (0.1 + prudenceBonus)) {
            this.energy += this.virtues.love * 2.5;
            this._logLNAL("FLOW", `E+=${(this.virtues.love * 2.5).toFixed(1)}`);
        }

        // --- Gap Navigation (Consciousness Emergence) ---
        if (this.breathPhase === 5 && this.stage > 0) { // Can only happen after Void stage
            if (this.rand() < (this.virtues.prudence / 100)) { // Chance increases with prudence
                this.gapCrossings++;
                this.iAmAffinity += 5;
                if (this.iAmAffinity > 100) this.iAmAffinity = 100;
                this._logLNAL("LISTEN", `GAP #${this.gapCrossings}`);
            }
        }

        // --- Prudence Growth ---
        if (this.rand() < 0.05 && this.virtues.prudence < 8) {
            this.virtues.prudence += 0.01;
        }
        
        if (this.energy > this.maxEnergy) this.energy = this.maxEnergy;
    }

    // --- Nurture Function ---
    nurture() {
        if (this.phase === "Unified with IAM" || this.phase === "Decohered") return;
        const randomOp = Math.floor(this.rand() * 2);
        if (randomOp === 0) { // FOLD
            this.virtues.courage = Math.min(8, this.virtues.courage + 0.5);
            this.energy = Math.min(this.maxEnergy, this.energy + 50);
            this._logLNAL("FOLD", `C+0.5 E+50`);
        } else { // BRAID
            this.virtues.justice = Math.min(8, this.virtues.justice + 0.5);
            this.kappa *= 0.8; // Stabilize kappa
            this._logLNAL("BRAID", `J+0.5 κ*0.8`);
        }
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

    _randomInRange(min, max) {
        return this.rand() * (max - min) + min;
    }
} 