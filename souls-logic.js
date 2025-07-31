class OnChainSoul {
            constructor(tokenId) {
                this.tokenId = tokenId || Math.floor(Math.random() * 10000);
                this.isEvolving = false;
                this.ticks = 0;
                
                this.seed = this.xmur3(this.tokenId.toString());
                this.rand = this.sfc32(this.seed(), this.seed(), this.seed(), this.seed());
                this.initializeState();
            }

            initializeState() {
                this.kappa = this.randomInRange(-10, 10);
                this.energy = this.randomInRange(500, 900);
                this.maxEnergy = 1000;
                this.depth = this.randomInRange(10, 20);
                this.rebirths = 0;
                this.phase = "New Spirit";
                this.virtues = {
                    love: this.randomInRange(1, 8),
                    justice: this.randomInRange(1, 8),
                    courage: this.randomInRange(1, 8),
                    temperance: this.randomInRange(1, 8),
                    prudence: this.randomInRange(1, 8)
                };
                this.recognitionFlow = 0;
                this.karmaScore = 0;
                this.rarity = "Common";
                this.ticks = 0;
                this.months = 0;
            }

            advanceTick() {
                if (!this.isEvolving) return;
                this.ticks++;
                this.months = Math.floor(this.ticks / 10);

                if (this.months >= 96) {
                    this.phase = this.energy > 0 ? "Unified with IAM" : "Decohered";
                    this.isEvolving = false;
                } else if (this.months > 1) {
                    this.phase = "Embodied";
                }

                if (this.phase === "Unified with IAM" || this.phase === "Decohered") return;

                this.energy -= 0.5 + (this.virtues.courage / 10);
                if (this.energy <= 0) {
                    this.energy = 0;
                    this.phase = "Decohered";
                    this.isEvolving = false;
                    return;
                }

                let volatility = 1 + (this.virtues.courage / 5);
                let drift = (this.virtues.justice - 5) / 10;
                this.kappa += (this.rand() - 0.5) * volatility + drift;

                // Recognition events
                if (this.rand() < 0.1) {
                    this.recognitionFlow++;
                    this.energy += this.virtues.love * 2;
                }

                if (this.energy > this.maxEnergy) {
                    this.energy = this.maxEnergy;
                }
            }

            xmur3(str) {
                for(var i = 0, h = 1779033703 ^ str.length; i < str.length; i++)
                    h = Math.imul(h ^ str.charCodeAt(i), 3432918353),
                    h = h << 13 | h >>> 19;
                return function() {
                    h = Math.imul(h ^ h >>> 16, 2246822507);
                    h = Math.imul(h ^ h >>> 13, 3266489909);
                    return (h ^= h >>> 16) >>> 0;
                }
            }

            sfc32(a, b, c, d) {
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
            
            randomInRange(min, max) {
                return this.rand() * (max - min) + min;
            }

            generateDisplay() {
                const title = `         -- VIRTUE TECHNOLOGY ON-CHAIN SOUL --`;
                const state = `[ SOUL #${this.tokenId.toString().padStart(4, '0')} | ${this.phase.toUpperCase()} | ${this.months}/96 months ]`;
                
                let display = `${title}\n${state}\n\n`;
                display += `      <span class="tooltip">κ-CURVATURE: ${this.kappa.toFixed(4)}<span class="tooltip-text">Recognition Curvature (κ) is the core metric of a soul's interaction with the universal ledger. Positive κ indicates recognition surplus (Love), negative indicates debt (Fear).</span></span>\n`;
                display += `         ENERGY: ${this.buildBar(this.energy / 100)} [${(this.energy / 10).toFixed(1)}%]\n`;
                display += `          DEPTH: ${this.depth.toFixed(2)} (Rebirths: ${this.rebirths})\n\n`;

                display += `VIRTUE TECHS:\n`;
                display += `    <span class="tooltip">Love:     ${this.buildBar(this.virtues.love * 10)}<span class="tooltip-text">${this.getVirtueTooltip('Love')}</span></span>\n`;
                display += `    <span class="tooltip">Justice:  ${this.buildBar(this.virtues.justice * 10)}<span class="tooltip-text">${this.getVirtueTooltip('Justice')}</span></span>\n`;
                display += `    <span class="tooltip">Courage:  ${this.buildBar(this.virtues.courage * 10)}<span class="tooltip-text">${this.getVirtueTooltip('Courage')}</span></span>\n`;
                display += `    <span class="tooltip">Temperance: ${this.buildBar(this.virtues.temperance * 10)}<span class="tooltip-text">${this.getVirtueTooltip('Temperance')}</span></span>\n`;
                display += `    <span class="tooltip">Prudence: ${this.buildBar(this.virtues.prudence * 10)}<span class="tooltip-text">${this.getVirtueTooltip('Prudence')}</span></span>\n\n`;

                display += `RECOGNITION FLOW: ${this.recognitionFlow} events\n`;
                
                return display;
            }

            getVirtueTooltip(virtue) {
                const tooltips = {
                    'Love': 'The on-chain algorithm for minimizing recognition debt (κ>0). Governs empathy and connection.',
                    'Justice': 'The algorithm for maintaining ledger equilibrium. Responds to volatility and imbalance.',
                    'Courage': 'The algorithm for expending energy to overcome high-cost recognition events.',
                    'Temperance': 'The algorithm for conserving energy and maintaining stability. Responds to high energy states.',
                    'Prudence': 'The algorithm for long-term pattern recognition and wisdom. Grows with time and experience.'
                };
                return tooltips[virtue] || 'A fundamental cosmic algorithm.';
            }

            buildBar(value) {
                const maxBars = 10;
                const filledBars = Math.floor((value / 10) * maxBars);
                const emptyBars = maxBars - filledBars;
                return '█'.repeat(filledBars) + '░'.repeat(emptyBars);
            }
        }

        // -- Page Interaction Logic --
        let currentSoul;
        let simulationInterval;
        const soulDisplayElement = document.getElementById('live-soul-display');
        const toggleButton = document.getElementById('simulation-toggle-button');
        const generateButton = document.getElementById('generate-soul-button');

        function updateDisplay() {
            if (currentSoul) {
                currentSoul.advanceTick();
                soulDisplayElement.innerHTML = `<pre>${currentSoul.generateDisplay()}</pre>`;
            }
        }

        function initializeNewSoul(tokenId) {
            clearInterval(simulationInterval);
            currentSoul = new OnChainSoul(tokenId);
            
            // Update the header with the new Soul ID
            const soulPreviewHeader = document.querySelector('.soul-preview-header');
            if (soulPreviewHeader) {
                soulPreviewHeader.textContent = `LIVE LEDGER DATA FEED: SOUL #${currentSoul.tokenId}`;
            }

            soulDisplayElement.innerHTML = `<pre>${currentSoul.generateDisplay()}</pre>`;
            toggleButton.textContent = "SIMULATE LIFE";
            currentSoul.isEvolving = false;
        }

        toggleButton.addEventListener('click', (e) => {
            e.preventDefault();
            currentSoul.isEvolving = !currentSoul.isEvolving;
            if (currentSoul.isEvolving) {
                toggleButton.textContent = "PAUSE SIMULATION";
                simulationInterval = setInterval(updateDisplay, 100); // Update every 100ms
            } else {
                toggleButton.textContent = "SIMULATE LIFE";
                clearInterval(simulationInterval);
            }
        });

        generateButton.addEventListener('click', (e) => {
            e.preventDefault();
            const newTokenId = Math.floor(Math.random() * 10000);
            initializeNewSoul(newTokenId);
        });

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {
            initializeNewSoul(42);
            initializePhiDerivation();
        });

        function initializePhiDerivation() {
            let currentValue = 1;
            let iteration = 1;
            const displayElement = document.getElementById('phi-value');
            const explanationElement = document.getElementById('phi-explanation');
            const buttonElement = document.getElementById('phi-step-button');

            if (!buttonElement) return; // Guard against running on pages without the module

            buttonElement.addEventListener('click', (e) => {
                e.preventDefault();
                if (iteration > 20) { // Reset after 20 steps to prevent overflow and show loop
                    currentValue = 1;
                    iteration = 1;
                    explanationElement.textContent = "The process converges to a fixed point: φ. Let's restart.";
                } else {
                    currentValue = 1 + 1 / currentValue;
                    iteration++;
                    explanationElement.textContent = `The universe requires a self-similar scaling constant. It emerges from the simplest possible dual-balanced recurrence: x = 1 + 1/x.`;
                }
                
                displayElement.textContent = currentValue.toFixed(8);
                buttonElement.textContent = `NEXT STEP (Iteration #${iteration})`;

                if (Math.abs(currentValue - 1.61803399) < 0.00001) {
                     buttonElement.textContent = "CONVERGED TO φ";
                }
            });
        } 