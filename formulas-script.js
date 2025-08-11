// Matrix rain effect
function createMatrixRain() {
    const container = document.getElementById('matrixBg');
    if (!container) return;
    
    const columns = Math.floor(window.innerWidth / 20);
    
    for (let i = 0; i < columns; i++) {
        const column = document.createElement('div');
        column.className = 'matrix-column';
        column.style.left = i * 20 + 'px';
        column.style.animationDuration = (Math.random() * 10 + 5) + 's';
        column.style.animationDelay = Math.random() * 5 + 's';
        
        // Random formula symbols
        const symbols = 'φπΣ∫∂∇κμνλαβγδεζηθ0123456789+-=()[]{}';
        let text = '';
        for (let j = 0; j < 50; j++) {
            text += symbols[Math.floor(Math.random() * symbols.length)] + '<br>';
        }
        column.innerHTML = text;
        container.appendChild(column);
    }
}

// Parallax effect for hero background
function handleParallax() {
    const heroBg = document.querySelector('.hero-bg-container');
    if (!heroBg) return;
    
    const scrolled = window.pageYOffset;
    const heroHeight = window.innerHeight;
    
    // Fade out the Matrix background as user scrolls
    const opacity = Math.max(0, 1 - (scrolled / heroHeight) * 2);
    heroBg.style.opacity = opacity;
    
    // Add slight parallax movement
    heroBg.style.transform = `translateY(${scrolled * 0.5}px)`;
}

// Source Code Button Interaction
function initSourceCodeButton() {
    const btn = document.getElementById('sourceCodeBtn');
    if (!btn) return;
    
    btn.addEventListener('click', function() {
        // Add glitch effect
        this.classList.add('glitch');
        
        // Create terminal-like popup
        createTerminalPopup();
        
        // Remove glitch effect after animation
        setTimeout(() => {
            this.classList.remove('glitch');
        }, 300);
    });
}

// Create Terminal Popup
function createTerminalPopup() {
    // Remove existing popup if any
    const existing = document.getElementById('terminalPopup');
    if (existing) existing.remove();
    
    // Create popup container
    const popup = document.createElement('div');
    popup.id = 'terminalPopup';
    popup.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 90%;
        max-width: 800px;
        height: 80vh;
        background: rgba(0, 0, 0, 0.95);
        border: 2px solid #10b981;
        border-radius: 10px;
        z-index: 10000;
        overflow: hidden;
        animation: terminalOpen 0.3s ease-out;
    `;
    
    // Create terminal header
    const header = document.createElement('div');
    header.style.cssText = `
        background: #10b981;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    `;
    header.innerHTML = `
        <div style="display: flex; gap: 8px;">
            <div style="width: 12px; height: 12px; border-radius: 50%; background: rgba(0,0,0,0.3);"></div>
            <div style="width: 12px; height: 12px; border-radius: 50%; background: rgba(0,0,0,0.3);"></div>
            <div style="width: 12px; height: 12px; border-radius: 50%; background: rgba(0,0,0,0.3);"></div>
        </div>
        <span style="color: #000; font-family: 'JetBrains Mono', monospace; font-weight: 600;">RECOGNITION PHYSICS SOURCE</span>
        <button id="closeTerminal" style="background: none; border: none; color: #000; font-size: 20px; cursor: pointer;">✕</button>
    `;
    
    // Create terminal body
    const body = document.createElement('div');
    body.style.cssText = `
        padding: 20px;
        color: #10b981;
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        line-height: 1.6;
        overflow-y: auto;
        height: calc(100% - 50px);
    `;
    
    // Terminal content with typing effect
    const commands = [
        '$ accessing recognition_physics.core...',
        '> Loading universal ledger framework...',
        '> Initializing cost function J(x) = ½(x + 1/x)',
        '> Golden ratio φ detected at minimum',
        '> Mass ladder initialized with 89 rungs',
        '> Sector factors B ∈ {1,2,3,4,6,8,9,12}',
        '> Coherence energy E_coh = 0.090 eV',
        '',
        '$ cat meta_principle.lean',
        'theorem meta_principle : ¬(Nothing → Nothing) := by',
        '  intro h',
        '  cases h.recognizer',
        '  -- Q.E.D.',
        '',
        '$ python calculate_electron_mass.py',
        '> Calculating: m = B·E_coh·φ^(r+f)',
        '> B = 1, r = 32, f = 0.0',
        '> Result: 0.51099895 MeV',
        '> Measured: 0.51099895 MeV',
        '> Error: 0.000000%',
        '',
        '$ git clone https://github.com/jonwashburn/audit.git',
        '> Cloning Recognition Science audit repository...',
        '> Machine-verified proofs: ✓',
        '> Zero free parameters: ✓',
        '> Cross-domain validation: ✓',
        '',
        '$ echo "Reality is computation. These are its instructions."'
    ];
    
    popup.appendChild(header);
    popup.appendChild(body);
    document.body.appendChild(popup);
    
    // Close button functionality
    document.getElementById('closeTerminal').addEventListener('click', () => {
        popup.style.animation = 'terminalClose 0.3s ease-out';
        setTimeout(() => popup.remove(), 300);
    });
    
    // Click outside to close
    popup.addEventListener('click', (e) => {
        if (e.target === popup) {
            popup.style.animation = 'terminalClose 0.3s ease-out';
            setTimeout(() => popup.remove(), 300);
        }
    });
    
    // Type out commands
    let index = 0;
    function typeCommand() {
        if (index < commands.length) {
            const line = document.createElement('div');
            line.textContent = commands[index];
            line.style.opacity = '0';
            line.style.animation = 'fadeIn 0.2s forwards';
            line.style.animationDelay = '0.05s';
            body.appendChild(line);
            body.scrollTop = body.scrollHeight;
            index++;
            setTimeout(typeCommand, 150);
        } else {
            // Add blinking cursor at the end
            const cursor = document.createElement('span');
            cursor.textContent = '█';
            cursor.style.animation = 'blink 1s infinite';
            body.appendChild(cursor);
        }
    }
    
    setTimeout(typeCommand, 300);
}

// Add necessary CSS animations
function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes terminalOpen {
            from {
                opacity: 0;
                transform: translate(-50%, -50%) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }
        }
        
        @keyframes terminalClose {
            from {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }
            to {
                opacity: 0;
                transform: translate(-50%, -50%) scale(0.9);
            }
        }
        
        @keyframes fadeIn {
            to {
                opacity: 1;
            }
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}

// Initialize on load
window.addEventListener('load', () => {
    createMatrixRain();
    initSourceCodeButton();
    addAnimationStyles();
});

// Handle scroll events for parallax
window.addEventListener('scroll', handleParallax);

// Initial parallax state
handleParallax();