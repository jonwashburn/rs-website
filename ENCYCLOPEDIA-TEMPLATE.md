# Encyclopedia Template Guide v3.0
## Recognition Physics Encyclopedia - Academic Style

---

## TEMPLATE STRUCTURE

### Page HTML Structure (Generated Automatically)
The agent will wrap your content in this structure:

```html
<section class="template-section encyclopedia-entry">
    <div class="template-container">
        <!-- Hero Box (auto-generated) -->
        <div class="encyclopedia-hero">
            <p class="template-hero-badge">ENCYCLOPEDIA ENTRY</p>
            <h1>[Title with <span class="template-accent-text">accent</span>]</h1>
            <p class="lead-text">[Summary from metadata]</p>
            <div class="meta-badges">
                <span class="category-badge">[Category]</span>
                <span class="difficulty-badge">[Level]</span>
                <span class="tags">[Tags]</span>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="template-reading">
            [Your content goes here]
        </div>
    </div>
</section>
```

### Content Structure (What You Write)

#### 1. Introduction Section
```html
<!-- Lead paragraph introducing the concept -->
<p class="lead-text">
    [A compelling introduction that sets context. Can include <button class="term" data-def="Definition shown on hover">interactive terms</button> that reveal definitions on hover.]
</p>

<!-- Optional reading tip -->
<div class="reading-tip">
    <p><strong>Reading tip:</strong> [Guidance for how to approach this content]</p>
</div>
```

#### 2. Core Definition
```html
<div class="definition-box">
    <h2>Formal Definition</h2>
    <p>[Technical definition with precision]</p>
    <p class="math-note">Mathematical form: <code>[formula]</code></p>
</div>
```

#### 3. Plain Language Explanation
```html
<div class="plain-language">
    <p>
        In plain terms, [accessible explanation using everyday language and analogies].
    </p>
    <p>
        [Continue with additional context, making complex ideas approachable].
    </p>
</div>
```

#### 4. Key Properties/Constants (if applicable)
```html
<h2 class="template-section-title">Key Properties</h2>

<div class="constants-list">
    <div class="constant">
        <div class="constant-header">
            <span class="constant-name">Property Name</span>
            <span class="constant-value">Value</span>
        </div>
        <p class="constant-desc">Brief description of what this means.</p>
        <details>
            <summary>Derivation & Details</summary>
            <div class="details-content">
                <p>Detailed explanation of how this is derived.</p>
                <ul>
                    <li>Point 1 about this property</li>
                    <li>Point 2 about this property</li>
                </ul>
            </div>
        </details>
    </div>
</div>
```

#### 5. How It Works (Mechanism)
```html
<h2 class="template-section-title">How It Works</h2>

<div class="theorems-grid">
    <details class="theorem-detail">
        <summary>Step 1: [Process Name]</summary>
        <div class="theorem-content">
            <p><strong>What happens:</strong> [Description]</p>
            <p><strong>Why it matters:</strong> [Significance]</p>
            <p><strong>Mathematical form:</strong> <code>[formula if applicable]</code></p>
        </div>
    </details>
    
    <details class="theorem-detail">
        <summary>Step 2: [Process Name]</summary>
        <div class="theorem-content">
            <p>[Content following same structure]</p>
        </div>
    </details>
</div>
```

#### 6. Calculations/Predictions (if applicable)
```html
<h2 class="template-section-title">Testable Predictions</h2>

<div class="calc-grid">
    <div class="calc-card">
        <h3>Prediction Name</h3>
        <span class="calc-value">Predicted Value</span>
        <span class="calc-formula">Formula used</span>
        <p>Brief explanation of what this predicts.</p>
        <a href="#" class="derivation-link">See derivation</a>
    </div>
    
    <div class="calc-card">
        <h3>Another Prediction</h3>
        <span class="calc-value">Value</span>
        <span class="calc-formula">Formula</span>
        <p>Explanation.</p>
    </div>
</div>
```

#### 7. Mathematical Details (Collapsible)
```html
<details class="math-section">
    <summary>Mathematical Framework</summary>
    <div class="math-content">
        <div class="formula-section">
            <span class="formula">Main Formula Here</span>
            <div class="description">
                <p>Where:</p>
                <ul>
                    <li><code>x</code> = description of variable</li>
                    <li><code>y</code> = description of variable</li>
                </ul>
            </div>
        </div>
    </div>
</details>
```

#### 8. Common Misconceptions
```html
<h2 class="template-section-title">Common Misconceptions</h2>

<div class="comparison-card">
    <h3>Misconception vs. Reality</h3>
    <div class="comparison-point">
        <strong>Wrong:</strong> [Common misunderstanding]
    </div>
    <div class="comparison-point">
        <strong>Right:</strong> [Correct understanding]
    </div>
</div>
```

#### 9. FAQ Section
```html
<h2 class="template-section-title">Frequently Asked Questions</h2>

<div class="faq-section">
    <details>
        <summary>Question that readers often ask?</summary>
        <p>Clear, concise answer that addresses the question directly.</p>
    </details>
    
    <details>
        <summary>Another common question?</summary>
        <p>Helpful answer with context.</p>
    </details>
</div>
```

#### 10. Related Topics
```html
<h2 class="template-section-title">Related Topics</h2>

<div class="related-grid">
    <a href="/encyclopedia/[slug]" class="related-card">
        <h3>Related Concept Name</h3>
        <p>Brief description of how it relates.</p>
        <span class="relation-type">FOUNDATIONAL</span>
    </a>
    
    <a href="/encyclopedia/[slug]" class="related-card">
        <h3>Another Related Concept</h3>
        <p>Connection explanation.</p>
        <span class="relation-type">EXTENDS</span>
    </a>
</div>
```

#### 11. Academic Context (Optional)
```html
<div class="academic-note">
    <strong>Academic Note:</strong> [Connection to established physics/mathematics, 
    comparisons with standard approaches, or notes for researchers.]
</div>
```

#### 12. Further Reading (Collapsible)
```html
<details class="further-reading">
    <summary>Further Reading</summary>
    <ul>
        <li><a href="/[page]">Internal Resource Title</a></li>
        <li><a href="[external]">External Paper or Resource</a></li>
    </ul>
</details>
```

---

## STYLE GUIDELINES

### Interactive Elements
- Use `<button class="term" data-def="Definition here">term</button>` for hoverable definitions
- These appear with subtle pink outline, reveal definitions on hover
- Keep definitions concise (1-2 sentences max)

### Visual Hierarchy
- **Hero Box**: Framed with border, contains title and metadata
- **Section Titles**: Use `<h2 class="template-section-title">` for major sections
- **Accent Color**: Last word of titles gets `<span class="template-accent-text">` for pink accent
- **Cards**: Use for calculations, properties, comparisons (hover effect included)

### Mathematical Content
- Inline math: `<code>formula</code>`
- Block formulas: Use `.formula-section` with `.formula` class
- Always provide plain language explanation alongside math

### Progressive Disclosure
- Use `<details>` elements for deep dives
- Summary should be compelling question or clear section name
- Expanded content should reward curiosity

### Relationship Types for Related Topics
- **FOUNDATIONAL**: Required prerequisite understanding
- **EXTENDS**: Builds upon this concept
- **PARALLEL**: Similar concept in different domain
- **APPLIES**: Practical application of this concept
- **CONTRASTS**: Opposing or alternative view

---

## CONTENT PRINCIPLES

### Clarity First
- Lead with clearest explanation
- Build complexity gradually
- Always provide plain English alongside technical content

### Academic Rigor
- Precise definitions
- Mathematical formulations where applicable
- Clear derivations
- Testable predictions

### Accessibility
- Multiple explanation levels
- Visual aids where helpful
- Interactive elements for engagement
- Progressive disclosure for different audiences

### Consistency
- Follow the structural order
- Use established CSS classes
- Maintain tone: authoritative but approachable
- Link related concepts generously

---

## QUALITY CHECKLIST

Before publishing, ensure:

- [ ] Hero box properly formatted with title, summary, and badges
- [ ] Both technical definition and plain language explanation present
- [ ] Interactive terms used where helpful
- [ ] Mathematical content (if any) has plain language companion
- [ ] Related topics identified with relationship types
- [ ] Progressive disclosure used for detailed content
- [ ] All sections follow academic page styling
- [ ] Links to related encyclopedia entries included
- [ ] Mobile responsive (cards stack, hero adjusts)

---

## CSS CLASSES REFERENCE

### Structural
- `.template-section.encyclopedia-entry` - Main wrapper
- `.template-container` - Content container
- `.encyclopedia-hero` - Framed hero box
- `.template-reading` - Main content area

### Typography
- `.template-hero-badge` - Small caps label
- `.template-accent-text` - Pink accent color
- `.lead-text` - Larger intro paragraphs
- `.template-section-title` - Section headings

### Components
- `.definition-box` - Formal definition container
- `.plain-language` - Blue background explanation
- `.reading-tip` - Pink-bordered tip box
- `.academic-note` - Yellow gradient note
- `.constant` - Property/constant card
- `.calc-card` - Calculation/prediction card
- `.theorem-detail` - Expandable detail section
- `.comparison-card` - Comparison container
- `.related-card` - Related topic link card

### Interactive
- `.term` - Hoverable term with definition
- `.expansion` - Revealed definition box
- `details` - Collapsible sections
- `.derivation-link` - Link to detailed derivation

---

This template creates encyclopedia pages that match the sophisticated, academic style of the Recognition Physics technical overview page, with consistent design elements, interactive features, and clear information hierarchy.