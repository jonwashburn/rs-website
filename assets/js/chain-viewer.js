// Markers: key snippets to annotate (pattern → key)
const markers = [
    // Core foundational concepts
    { key: 'nothing_def', pattern: 'abbrev Nothing := Empty' },
    { key: 'recognition_structure', pattern: 'structure Recognition (A : Type) (B : Type)' },
    { key: 'mp_def', pattern: 'def MP : Prop := ¬ ∃ r : Recognition Nothing Nothing' },
    { key: 'mp_proof', pattern: 'theorem mp_holds : MP := by' },
    { key: 'mp_proof_body', pattern: 'intro h; rcases h with ⟨r, _⟩; cases r.recognizer' },
    
    // Recognition structure and chains
    { key: 'rec_structure_def', pattern: 'structure RecognitionStructure where' },
    { key: 'chain_def', pattern: 'structure Chain (V : Type) (n : ℕ) where' },
    { key: 'is_closed', pattern: 'def isClosed {V : Type} {n : ℕ} (c : Chain V n)' },
    
    // Atomic tick theory
    { key: 't2_atomicity', pattern: 'def T2_atomicity' },
    
    // Ledger structure
    { key: 'ledger_def', pattern: 'structure Ledger (V : Type) where' },
    { key: 'balanced_ledger', pattern: 'def balancedLedger' },
    { key: 'flux_ledger', pattern: 'structure FluxLedger' },
    { key: 'chain_flux', pattern: 'def chainFlux' },
    { key: 't3_conservation', pattern: 'def T3_conservation' },
    
    // Cost function J
    { key: 'j_def', pattern: 'noncomputable def J (x : ℝ) : ℝ := (x + 1/x) / 2' },
    { key: 'j_nonneg', pattern: 'theorem J_nonneg' },
    { key: 'j_eq_one_iff', pattern: 'theorem J_eq_one_iff' },
    { key: 'j_strict_mono', pattern: 'theorem J_strictMono_on_ge_one' },
    
    // Golden ratio φ
    { key: 'phi_def', pattern: 'noncomputable def φ : ℝ := (1 + Real.sqrt 5) / 2' },
    { key: 'phi_fixed', pattern: 'theorem phi_fixed : φ = 1 + 1 / φ' },
    { key: 'phi_quadratic', pattern: 'theorem phi_quadratic : φ ^ 2 = φ + 1' },
    { key: 'phi_unique_pos', pattern: 'theorem phi_unique_pos' },
    
    // k=1 minimization
    { key: 'xk_def', pattern: 'noncomputable def x_k (k : ℝ) : ℝ' },
    { key: 'k_equals_one', pattern: 'theorem k_equals_one' },
    { key: 'xk_eq_phi_at_one', pattern: 'theorem x_k_eq_phi_at_one' },
    
    // Pattern theory and period 8
    { key: 'pattern_def', pattern: 'def Pattern (d : ℕ) := Fin d → Bool' },
    { key: 'pattern_card', pattern: 'theorem pattern_card' },
    { key: 'complete_walk', pattern: 'def completeWalk' },
    { key: 'min_period', pattern: 'theorem min_period' },
    { key: 'gray', pattern: 'def gray : ℕ → Pattern 3' },
    { key: 'period_exactly_8', pattern: 'theorem period_exactly_8' },
    { key: 'eight_tick_min', pattern: 'theorem eight_tick_min' },
    
    // Strong ledger and double entry
    { key: 'strong_t4', pattern: 'namespace StrongT4' },
    { key: 'graph', pattern: 'structure Graph where' },
    { key: 'double_entry', pattern: 'structure DoubleEntry' },
    { key: 'degree', pattern: 'noncomputable def degree' },
    { key: 'canonical_ledger', pattern: 'noncomputable def CanonicalLedger' },
    { key: 'handshaking', pattern: 'theorem handshaking' },
    { key: 'degree_sum_even', pattern: 'theorem degree_sum_even' },
    
    // Cost requirements
    { key: 'cost_requirements', pattern: 'structure CostRequirements' },
    { key: 'jcost_def', pattern: 'def Jcost : ℝ → ℝ' },
    { key: 'jcost_meets', pattern: 'theorem Jcost_meets' },
    
    // Recognition coherence
    { key: 'rec_length', pattern: 'noncomputable def recLength' },
    { key: 'rec_length_balance', pattern: 'theorem rec_length_from_balance' },
    
    // Final chain theorem
    { key: 'chain_theorem', pattern: 'theorem Chain' },
    { key: 'recognition_physics', pattern: 'theorem recognition_determines_physics' },
    
    // Simple ledger
    { key: 'simple_ledger', pattern: 'structure SimpleLedger' },
    { key: 'sphi_def', pattern: 'def sphi' },
    { key: 'schain_flux', pattern: 'def schainFlux' },
    { key: 's_conserves', pattern: 'class SConserves' },
    
    // Namespace and structure
    { key: 'namespace_mono', pattern: 'namespace IndisputableMonolith' },
    { key: 'eight_theorems_index', pattern: '# The Eight Theorems (index)' },
    { key: 'end_monolith', pattern: 'end IndisputableMonolith' },
];

// Scientist-facing explanations
const explain = {
    // Core foundational concepts
    nothing_def: `<p><strong>The Foundation:</strong> Nothing = Empty type. This isn't philosophical—it's type-theoretic bedrock. Empty has zero inhabitants, making recognition of itself impossible by construction.</p>`,
    
    recognition_structure: `<p><strong>Abstract Recognition:</strong> The minimal structure needed for anything to recognize anything else. Two types A and B, with a recognizer from A and recognized from B. Pure abstraction—no physics yet!</p>`,
    
    mp_def: `<p><strong>The Meta-Principle:</strong> The central tautology of RS. States that no recognition relation can exist between Nothing and itself. This logical necessity forces the existence of at least one recognition pair.</p>`,
    
    mp_proof: `<p><strong>Bulletproof Logic:</strong> The proof that Nothing cannot recognize itself. Machine-verified—no hand-waving allowed. This tautology births all of physics.</p>`,
    
    mp_proof_body: `<p><strong>The Kill Shot:</strong> Assume such recognition exists → extract the recognizer → but Nothing has no inhabitants → contradiction! Three lines of logic that create the universe.</p>`,
    
    // Recognition structure development
    rec_structure_def: `<p><strong>Recognition Framework:</strong> The universe's operating system. U is the type of entities, R defines who recognizes whom. All of physics emerges from this minimal structure.</p>`,
    
    chain_def: `<p><strong>Causal Chains:</strong> Finite sequences of vertices. These model paths through spacetime—how information and causality flow discretely.</p>`,
    
    is_closed: `<p><strong>Closed Chains:</strong> Chains where the end connects back to the beginning. These loops are where conservation laws come from—what goes around must come around!</p>`,
    
    // Atomic tick theory
    t2_atomicity: `<p><strong>T2 - Atomic Uniqueness:</strong> At most one recognition event per tick. This discreteness is what makes quantum mechanics work—no simultaneous events allowed!</p>`,
    
    // Ledger structure
    ledger_def: `<p><strong>Universal Bookkeeping:</strong> Every recognition event must be tracked. Debit and credit are integer functions—the universe runs on discrete accounting.</p>`,
    
    balanced_ledger: `<p><strong>Perfect Balance:</strong> For every vertex, debits + credits = 0. This is the prototype of all conservation laws—nothing created, nothing destroyed, only transformed.</p>`,
    
    flux_ledger: `<p><strong>Flow Tracking:</strong> Extension of ledger that tracks flows between vertices. The flux function captures how "stuff" moves through the recognition network.</p>`,
    
    chain_flux: `<p><strong>Total Flow:</strong> Sum of all fluxes along a chain. For closed chains, this must be zero—the mathematical origin of Kirchhoff's laws!</p>`,
    
    t3_conservation: `<p><strong>T3 - Conservation Law:</strong> Closed chains have zero flux. This theorem is why energy is conserved—it's a mathematical necessity, not a mysterious principle.</p>`,
    
    // Cost function theory
    j_def: `<p><strong>The Universe's Cost Function:</strong> J(x) = ½(x + 1/x). This isn't chosen—it's forced by logical requirements. The price of imbalance in recognition ratios.</p>`,
    
    j_nonneg: `<p><strong>Non-negative Cost:</strong> J(x) ≥ 1 always. Cost can't be negative—imbalance always costs energy. This theorem ensures the second law of thermodynamics.</p>`,
    
    j_eq_one_iff: `<p><strong>Perfect Balance:</strong> J(x) = 1 if and only if x = 1. The universe's equilibrium point—perfect balance has minimal cost.</p>`,
    
    j_strict_mono: `<p><strong>Strictly Increasing:</strong> J grows as you move away from balance (x=1). This monotonicity drives systems toward equilibrium—the origin of all thermodynamic gradients!</p>`,
    
    // Golden ratio emergence
    phi_def: `<p><strong>The Golden Ratio Emerges:</strong> φ = (1+√5)/2 ≈ 1.618... The universe's fundamental scaling constant, derived from pure logic. Not mystical—mathematical!</p>`,
    
    phi_fixed: `<p><strong>Golden Fixed Point:</strong> φ = 1 + 1/φ exactly. This self-similarity cascades through all scales—why φ appears everywhere in nature!</p>`,
    
    phi_quadratic: `<p><strong>Quadratic Nature:</strong> φ² = φ + 1. This algebraic relation drives the Fibonacci sequence and all φ-based scaling in physics.</p>`,
    
    phi_unique_pos: `<p><strong>Uniqueness of φ:</strong> There's only one positive solution to x = 1 + 1/x. This uniqueness is why φ is special—it's the only self-consistent scale!</p>`,
    
    // k=1 minimization
    xk_def: `<p><strong>General Solutions:</strong> For any k, x_k solves x = 1 + k/x. But only k=1 gives the minimal cost. Nature picks the cheapest option!</p>`,
    
    k_equals_one: `<p><strong>Optimization Theorem:</strong> k=1 minimizes the cost function J. Any other k costs more energy. This is why φ (not some other ratio) rules the universe!</p>`,
    
    xk_eq_phi_at_one: `<p><strong>Connection Point:</strong> When k=1, x_k = φ exactly. This links the optimization principle to the golden ratio emergence.</p>`,
    
    // Pattern theory and period 8
    pattern_def: `<p><strong>3D State Space:</strong> Pattern(d) represents all possible d-dimensional binary states. For d=3, this gives us the 8 corners of a cube—our spacetime's fundamental geometry!</p>`,
    
    pattern_card: `<p><strong>Exponential Growth:</strong> 2^d possible patterns for d dimensions. This exponential scaling is why complexity emerges so rapidly in our 3D universe.</p>`,
    
    complete_walk: `<p><strong>Complete Coverage:</strong> A walk that hits every pattern at least once. This models how the universe explores all possible states—quantum completeness!</p>`,
    
    min_period: `<p><strong>Minimum Coverage Time:</strong> You need at least 2^d steps to cover all patterns. For 3D, that's 8 steps minimum—no shortcuts allowed!</p>`,
    
    gray: `<p><strong>Gray Code Walk:</strong> The explicit 8-step path through 3D pattern space. Each step changes exactly one bit—minimal transitions, maximal efficiency!</p>`,
    
    period_exactly_8: `<p><strong>Quantum Heartbeat:</strong> Proof that 8 ticks exactly covers all 3D patterns. This theorem explains why so many quantum phenomena have 8-fold symmetry!</p>`,
    
    eight_tick_min: `<p><strong>Optimality Proof:</strong> Any complete walk in 3D takes exactly 8 steps. Not 7, not 9—exactly 8. Mathematics has spoken!</p>`,
    
    // Ledger theory
    strong_t4: `<p><strong>Strong Theorem 4:</strong> This namespace contains the proof that ledgers are necessary and unique. Double-entry bookkeeping isn't a choice—it's forced!</p>`,
    
    graph: `<p><strong>Graph Structure:</strong> Recognition networks form directed graphs. Vertices are entities, edges are recognition relations. The universe is a vast graph!</p>`,
    
    double_entry: `<p><strong>Double-Entry Principle:</strong> Every edge contributes to both debit (at target) and credit (at source). Perfect accounting with no loose ends!</p>`,
    
    degree: `<p><strong>Degree Counting:</strong> Number of edges touching a vertex. In physics: connection density, interaction strength, or coupling degree!</p>`,
    
    canonical_ledger: `<p><strong>Standard Ledger:</strong> The unique ledger that simply counts in/out edges. All other valid ledgers are scaled versions of this one!</p>`,
    
    handshaking: `<p><strong>Handshaking Lemma:</strong> Sum of all degrees = 2 × number of edges. Every edge has two ends—profound yet simple!</p>`,
    
    degree_sum_even: `<p><strong>Even Sum:</strong> Total degree is always even. This parity constraint has deep implications for particle physics!</p>`,
    
    // Cost requirements
    cost_requirements: `<p><strong>The Only Possible Cost:</strong> Any function satisfying symmetry, normalization, convexity, and growth bounds must equal J. No free parameters—physics is forced!</p>`,
    
    jcost_def: `<p><strong>Canonical Cost:</strong> Jcost = J - 1, shifting minimum to 0. Same function, different normalization. Shows the uniqueness of the cost structure.</p>`,
    
    jcost_meets: `<p><strong>Uniqueness Proof:</strong> J satisfies all requirements, and it's the only function that does. This theorem kills the multiverse—only one physics is possible!</p>`,
    
    // Recognition coherence
    rec_length: `<p><strong>Recognition Length:</strong> recLength = √(1/π). This sets the fundamental scale where cost balances curvature. Related to Planck length!</p>`,
    
    rec_length_balance: `<p><strong>Scale Balance:</strong> At recognition length, J(λ) = J(1/λ). This balance point sets the universe's fundamental pixelation scale.</p>`,
    
    // Final theorems
    chain_theorem: `<p><strong>Chain Complete:</strong> Existence proof that recognition structures with all required properties exist. The universe is mathematically consistent!</p>`,
    
    recognition_physics: `<p><strong>Physics Emerges:</strong> The complete theorem showing MP + atomicity + conservation + cost minimization = all of physics. Q.E.D.!</p>`,
    
    // Simple ledger
    simple_ledger: `<p><strong>Minimal Ledger:</strong> Stripped-down version with just debit/credit. Shows that even minimal structure forces conservation laws.</p>`,
    
    sphi_def: `<p><strong>Simple Potential:</strong> sphi = debit - credit. The simplest possible potential function still captures all essential physics!</p>`,
    
    schain_flux: `<p><strong>Simple Flux:</strong> Flux for simple ledgers. Even in this minimal setting, closed chains conserve—it's unavoidable!</p>`,
    
    s_conserves: `<p><strong>Conservation Class:</strong> Typeclass ensuring conservation. Any ledger satisfying this interface automatically gets all conservation theorems!</p>`,
    
    // Structure
    namespace_mono: `<p><strong>Monolith Namespace:</strong> Everything is contained in one self-consistent namespace. No external dependencies, no hidden assumptions—pure logic!</p>`,
    
    eight_theorems_index: `<p><strong>Theorem Roadmap:</strong> The 8 core theorems that build from tautology to physics. Each one is a critical step in the logical chain.</p>`,
    
    end_monolith: `<p><strong>Complete Package:</strong> End of the monolith. We've gone from Empty type to the complete laws of physics in one airtight logical chain!</p>`,
};

// Initialize the Lean code viewer
async function loadLean() {
    const status = document.getElementById('status');
    const container = document.getElementById('code');
    
    if (!status || !container) {
        console.error('Missing required elements');
        return;
    }
    
    status.textContent = 'Loading…';

    // Get the embedded Lean source
    const embedded = document.getElementById('lean-source');
    let text = '';
    
    if (embedded && embedded.textContent) {
        text = embedded.textContent.trim();
    }
    
    if (!text) {
        // Fallback content
        text = `/-! IndisputableMonolith.lean - Fallback content -/
namespace IndisputableMonolith

abbrev Nothing := Empty

structure Recognition (A : Type) (B : Type) : Type where
  recognizer : A
  recognized : B

def MP : Prop := ¬ ∃ r : Recognition Nothing Nothing, True

theorem mp_holds : MP := by
  intro h; rcases h with ⟨r, _⟩; cases r.recognizer

end IndisputableMonolith`;
    }

    const lines = text.split('\n');
    container.innerHTML = '';

    // Build DOM lines
    lines.forEach((t, i) => {
        const line = document.createElement('div');
        line.className = 'code-line';
        line.dataset.idx = String(i + 1);
        line.id = 'L' + String(i + 1);
        
        const ln = document.createElement('div');
        ln.className = 'ln';
        ln.textContent = String(i + 1).padStart(3, ' ');
        
        const code = document.createElement('div');
        code.className = 'code-text';
        code.textContent = t.replace(/\t/g, '  ');
        
        line.appendChild(ln);
        line.appendChild(code);
        container.appendChild(line);
    });

    // Tag hotspots
    markers.forEach(m => {
        const idx = lines.findIndex(l => l.includes(m.pattern));
        if (idx >= 0) {
            const el = container.children[idx];
            el.classList.add('hotspot');
            el.setAttribute('data-key', m.key);
            el.title = 'Click for explanation';
        }
    });

    // Add heuristic hotspots for definitions
    const defLike = /^(\s*)(def|theorem|lemma|structure|namespace|abbrev|noncomputable def|class|instance)\s+([A-Za-z0-9_\.]+)/;
    lines.forEach((raw, i) => {
        const textLine = raw.trim();
        if (!textLine || textLine.startsWith('--') || textLine.startsWith('/-')) return;
        const m = textLine.match(defLike);
        if (m) {
            const el = container.children[i];
            if (!el.classList.contains('hotspot')) {
                el.classList.add('hotspot');
                el.setAttribute('data-kind', m[2]);
                el.setAttribute('data-name', m[3]);
                el.title = `Click to learn about ${m[2]} ${m[3]}`;
            }
        }
    });

    // Add CSS for code viewer if not already present
    if (!document.getElementById('code-viewer-styles')) {
        const style = document.createElement('style');
        style.id = 'code-viewer-styles';
        style.textContent = `
            .code-line {
                display: flex;
                align-items: baseline;
                font-family: 'SF Mono', Monaco, monospace;
                font-size: 0.875rem;
                line-height: 1.5;
            }
            .code-line:hover {
                background: rgba(0,0,0,0.03);
            }
            .ln {
                color: #94a3b8;
                font-size: 0.75rem;
                user-select: none;
                padding-right: 1rem;
                text-align: right;
                min-width: 3rem;
            }
            .code-text {
                flex: 1;
                white-space: pre;
                overflow-x: auto;
            }
            .hotspot {
                cursor: pointer;
                position: relative;
            }
            .hotspot:hover {
                background: rgba(255,0,110,0.05);
            }
            .hotspot.active {
                background: rgba(255,0,110,0.1);
            }
            .tooltip {
                position: absolute;
                background: var(--color-primary);
                color: white;
                padding: 0.75rem 1rem;
                border-radius: 6px;
                font-size: 0.875rem;
                line-height: 1.5;
                max-width: 400px;
                z-index: 1000;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.15s ease;
            }
            .tooltip.active {
                opacity: 1;
            }
            .tooltip::after {
                content: '';
                position: absolute;
                top: -5px;
                left: 20px;
                width: 10px;
                height: 10px;
                background: var(--color-primary);
                transform: rotate(45deg);
            }
        `;
        document.head.appendChild(style);
    }

    status.textContent = '';
}

// Handle line clicks
document.addEventListener('click', (e) => {
    const line = e.target.closest('.code-line');
    if (!line || !line.classList.contains('hotspot')) return;
    
    // Get explanation
    const key = line.getAttribute('data-key');
    const kind = line.getAttribute('data-kind');
    const name = line.getAttribute('data-name');
    
    // Clear other active lines
    document.querySelectorAll('.code-line.active').forEach(l => {
        if (l !== line) l.classList.remove('active');
    });
    document.querySelectorAll('.tooltip').forEach(t => t.remove());
    
    // Toggle this line
    const isActive = line.classList.contains('active');
    if (isActive) {
        line.classList.remove('active');
        return;
    }
    
    line.classList.add('active');
    
    // Create tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip active';
    
    if (key && explain[key]) {
        tooltip.innerHTML = explain[key];
    } else if (kind && name) {
        tooltip.innerHTML = `<p><strong>${kind.toUpperCase()}: ${name}</strong></p>
            <p>This ${kind} is part of the formal proof chain. Click through the proof to see how each piece builds on the previous ones.</p>`;
    } else {
        tooltip.innerHTML = `<p>This line is part of the formal Lean proof. Each step is machine-verified for correctness.</p>`;
    }
    
    // Position tooltip
    const rect = line.getBoundingClientRect();
    tooltip.style.top = (rect.bottom + window.scrollY + 10) + 'px';
    tooltip.style.left = rect.left + 'px';
    document.body.appendChild(tooltip);
});

// Quick index navigation
const quickIndex = document.getElementById('quick-index');
if (quickIndex) {
    quickIndex.addEventListener('click', (e) => {
        const a = e.target.closest('a');
        if (!a) return;
        e.preventDefault();
        
        const jumpKey = a.getAttribute('data-jump');
        const target = document.querySelector(`.code-line[data-key="${jumpKey}"]`) || 
                      document.querySelector(`.code-line[data-name="${jumpKey}"]`);
                      
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setTimeout(() => target.click(), 200);
        }
    });
}

// Initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadLean);
} else {
    loadLean();
}
