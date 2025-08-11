// Matrix rain effect
function createMatrixRain() {
    const container = document.getElementById('matrixBg');
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

// Formula switcher
const formulas = [
    'J(x) = ½(x + 1/x)',
    'm = B·E_coh·φ^(r+f)',
    'κ = ∂²S/∂R²',
    'N = 2^D = 8',
    'F = -GMm/r² · w(r)'
];

function showFormula(index) {
    const display = document.getElementById('formula3d');
    display.style.animation = 'none';
    setTimeout(() => {
        display.textContent = formulas[index - 1];
        display.style.animation = 'rotate3d 10s linear infinite';
    }, 100);
}

// Create flowing particles in margins
function createFlowingParticles() {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-container';
    document.body.appendChild(particleContainer);
    
    function createParticle(side) {
        const particle = document.createElement('div');
        particle.className = 'flowing-particle';
        particle.style[side] = '0';
        particle.style.top = Math.random() * window.innerHeight + 'px';
        
        // Random formula symbol
        const symbols = ['φ', 'π', '∫', '∂', '∇', 'Σ', 'κ', '∞'];
        particle.textContent = symbols[Math.floor(Math.random() * symbols.length)];
        
        particleContainer.appendChild(particle);
        
        // Animate particle
        const duration = 3000 + Math.random() * 4000;
        const startX = side === 'left' ? -50 : window.innerWidth + 50;
        const endX = side === 'left' ? window.innerWidth + 50 : -50;
        const amplitude = 50 + Math.random() * 100;
        
        let start = null;
        function animate(timestamp) {
            if (!start) start = timestamp;
            const progress = (timestamp - start) / duration;
            
            if (progress < 1) {
                const x = startX + (endX - startX) * progress;
                const y = parseFloat(particle.style.top) + Math.sin(progress * Math.PI * 4) * 2;
                particle.style.transform = `translate(${x - startX}px, ${Math.sin(progress * Math.PI * 4) * amplitude}px)`;
                particle.style.opacity = Math.sin(progress * Math.PI);
                requestAnimationFrame(animate);
            } else {
                particle.remove();
            }
        }
        requestAnimationFrame(animate);
    }
    
    // Create particles periodically
    setInterval(() => {
        if (Math.random() > 0.5) createParticle('left');
        if (Math.random() > 0.5) createParticle('right');
    }, 500);
}

// Initialize on load
window.addEventListener('load', () => {
    createMatrixRain();
    createFlowingParticles();
});

// Parallax effect on mouse move
document.addEventListener('mousemove', (e) => {
    const x = e.clientX / window.innerWidth - 0.5;
    const y = e.clientY / window.innerHeight - 0.5;
    
    document.querySelectorAll('.formula-card').forEach((card, i) => {
        const speed = (i + 1) * 2;
        card.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
    });
});
