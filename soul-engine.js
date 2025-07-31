class UnifiedSoul {
    constructor(tokenId) {
        this.tokenId = tokenId;
        this.nonce = 0;

        // --- Seeding ---
        this._seed = this._xmur3(this.tokenId.toString());
        this.rand = this._sfc32(this._seed(), this._seed(), this._seed(), this._seed());
        
        this.initializeState();
    }

    // --- State Initialization ---
    initializeState() {
        this.ticks = 0;
        this.months = 0;
        this.phase = "New Spirit"; // New Spirit, Embodied, Decohered, Unified with IAM
        this.isEvolving = false;
        
        this.kappa = this._randomInRange(-20, 20); // Recognition balance
        this.energy = this._randomInRange(800, 1000);
        this.maxEnergy = 1000;
        this.depth = this._randomInRange(5, 15);
        this.rebirths = 0;
        
        this.virtues = {
            love: this._randomInRange(1, 8),
            justice: this._randomInRange(1, 8),
            courage: this._randomInRange(1, 8),
            temperance: this._randomInRange(1, 8),
            prudence: this._randomInRange(1, 8)
        };
        
        this.recognitionFlow = 0;
    }

    // --- Core Simulation Tick ---
    advanceTick() {
        if (!this.isEvolving) return;

        this.ticks++;
        this.months = Math.floor(this.ticks / 10); // 10 ticks = 1 month

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
            return;
        }

        // --- Kappa Fluctuation (modified by virtues) ---
        const volatility = 1 + (this.virtues.courage / 4);
        const drift = (this.virtues.justice - 4.5) / 8;
        this.kappa += (this.rand() - 0.5) * volatility + drift;
        
        // --- Recognition Events (modified by virtues) ---
        const prudenceBonus = this.virtues.prudence / 150;
        if (this.rand() < (0.1 + prudenceBonus)) {
            this.recognitionFlow++;
            this.energy += this.virtues.love * 2.5; // Love makes events more energizing
        }

        // --- Prudence Growth ---
        if (this.rand() < 0.05 && this.virtues.prudence < 8) {
            this.virtues.prudence += 0.01;
            if(this.virtues.prudence > 8) this.virtues.prudence = 8;
        }
        
        if (this.energy > this.maxEnergy) this.energy = this.maxEnergy;
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