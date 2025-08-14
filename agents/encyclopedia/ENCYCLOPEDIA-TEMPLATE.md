# Encyclopedia Template Guide v2.0
## For Recognition Physics Encyclopedia Pages

---

## TEMPLATE STRUCTURE

### 1. File Header (HTML)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[TITLE] - Recognition Physics Encyclopedia</title>
    <meta name="description" content="[SUMMARY - 160 chars max]">
    <link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
```

### 2. Metadata Block (Required)
```yaml
---
title: [Item Name]
category: [Physics|Mathematics|Consciousness|Computation|Cosmology]
difficulty: [Foundational|Intermediate|Advanced|Expert]
readingTime: [X min]
tags: [tag1, tag2, tag3, tag4]  # 3-6 tags
relatedConcepts: [concept1, concept2, concept3]  # for auto-linking
prerequisites: [prereq1, prereq2]  # optional
lastUpdated: YYYY-MM-DD
---
```

### 3. Page Structure (Canonical Order)

```html
<section class="template-section encyclopedia-entry">
    <div class="template-container">
        <div class="template-reading">
            <!-- Breadcrumb -->
            <p class="template-hero-badge">Encyclopedia / [Category] / [Title]</p>
            
            <!-- Title -->
            <h1>[Title]</h1>
            
            <!-- One-line essence -->
            <p class="essence">[Single sentence capturing the core idea]</p>
            
            <!-- Metadata badges -->
            <div class="meta-badges">
                <span class="category-badge">[Category]</span>
                <span class="difficulty-badge">[Difficulty]</span>
                <span class="reading-time">[X] min read</span>
            </div>
            
            <!-- Visual anchor (if applicable) -->
            <figure class="concept-visual">
                <img src="/assets/images/encyclopedia/[slug].svg" alt="[Description]">
                <figcaption>[Caption explaining the visual]</figcaption>
            </figure>
            
            <!-- Core Definition -->
            <div class="definition-box">
                <h2>Definition</h2>
                <p>[Technical definition in 1-2 sentences]</p>
                <p class="math-note">(Expressed mathematically: [formula if applicable])</p>
            </div>
            
            <!-- Plain English -->
            <h2>In Plain English</h2>
            <p>[Accessible explanation using analogy or everyday language]</p>
            <p>[Continue with 2-3 paragraphs max]</p>
            
            <!-- Why It Matters -->
            <div class="why-matters-callout">
                <h2>Why It Matters</h2>
                <ul>
                    <li><strong>[Impact 1]:</strong> [Explanation]</li>
                    <li><strong>[Impact 2]:</strong> [Explanation]</li>
                    <li><strong>[Impact 3]:</strong> [Explanation]</li>
                </ul>
            </div>
            
            <!-- How It Works -->
            <h2>How It Works</h2>
            <div class="mechanism-steps">
                <div class="step">
                    <h3>1. [Step/Component Name]</h3>
                    <p>[Description]</p>
                </div>
                <div class="step">
                    <h3>2. [Step/Component Name]</h3>
                    <p>[Description]</p>
                </div>
                <div class="step">
                    <h3>3. [Step/Component Name]</h3>
                    <p>[Description]</p>
                </div>
            </div>
            
            <!-- Key Properties -->
            <h2>Key Properties</h2>
            <div class="properties-grid">
                <div class="property-card">
                    <h3>[Property Name]</h3>
                    <p>[Description]</p>
                    <p class="math-note">(Value: [if applicable])</p>
                </div>
                <div class="property-card">
                    <h3>[Property Name]</h3>
                    <p>[Description]</p>
                </div>
                <div class="property-card">
                    <h3>[Property Name]</h3>
                    <p>[Description]</p>
                </div>
            </div>
            
            <!-- Mathematical Foundation (if applicable) -->
            <details class="math-section">
                <summary><h2>Mathematical Foundation</h2></summary>
                <div class="math-content">
                    <p>[Mathematical description]</p>
                    <p class="math-note">[Key equations]</p>
                    <p>[Derivation or relationships]</p>
                </div>
            </details>
            
            <!-- Connections -->
            <h2>Connections & Interactions</h2>
            <ul class="connections-list">
                <li><strong>With [Concept]:</strong> [How they relate]</li>
                <li><strong>Enables [Process]:</strong> [What it makes possible]</li>
                <li><strong>Constrains [Phenomenon]:</strong> [Limitations it imposes]</li>
            </ul>
            
            <!-- Predictions & Tests -->
            <div class="testable-box">
                <h2>Testable Predictions</h2>
                <ul>
                    <li class="prediction">[Specific, falsifiable prediction]</li>
                    <li class="prediction">[Another prediction with measurable outcome]</li>
                    <li class="test-method">Test via: [Experimental approach]</li>
                </ul>
            </div>
            
            <!-- Common Misconceptions -->
            <h2>Common Misconceptions</h2>
            <div class="misconception">
                <p class="wrong">❌ <strong>Wrong:</strong> [Common misunderstanding]</p>
                <p class="right">✓ <strong>Right:</strong> [Correct understanding]</p>
            </div>
            
            <!-- FAQs -->
            <h2>Frequently Asked Questions</h2>
            <div class="faq-section">
                <details class="faq-item">
                    <summary>[Question 1]</summary>
                    <p>[Answer]</p>
                </details>
                <details class="faq-item">
                    <summary>[Question 2]</summary>
                    <p>[Answer]</p>
                </details>
                <details class="faq-item">
                    <summary>[Question 3]</summary>
                    <p>[Answer]</p>
                </details>
            </div>
            
            <!-- Related Topics -->
            <h2>Related Topics</h2>
            <div class="related-grid">
                <a href="/encyclopedia/[slug1]" class="related-card">
                    <h3>[Topic Name]</h3>
                    <p>[One-line description]</p>
                    <span class="relation-type">Prerequisite</span>
                </a>
                <a href="/encyclopedia/[slug2]" class="related-card">
                    <h3>[Topic Name]</h3>
                    <p>[One-line description]</p>
                    <span class="relation-type">Extension</span>
                </a>
                <a href="/encyclopedia/[slug3]" class="related-card">
                    <h3>[Topic Name]</h3>
                    <p>[One-line description]</p>
                    <span class="relation-type">Application</span>
                </a>
            </div>
            
            <!-- Further Reading (optional) -->
            <details class="further-reading">
                <summary><h2>Further Reading</h2></summary>
                <ul>
                    <li><a href="[url]">[Internal page or section]</a> - [Description]</li>
                    <li><a href="[url]">[Paper or proof]</a> - [What it covers]</li>
                </ul>
            </details>
        </div>
    </div>
</section>
```

---

## CONTENT GUIDELINES

### Voice & Tone
- **Authoritative but accessible** - Write as if explaining to a smart colleague
- **Present tense** for facts, past tense for discoveries
- **Active voice** preferred
- **No hedging** - State facts confidently (we've proven them)
- **No hype** - Let the implications speak for themselves

### Plain English Rules
1. **Lead with intuition**, follow with precision
2. **One idea per paragraph**
3. **Concrete analogies** over abstract descriptions
4. **Short sentences** (aim for 15-20 words average)
5. **Define jargon** on first use, then use freely

### Mathematical Content
- **Never lead with math** - Always provide context first
- **Math as evidence**, not explanation
- Use the format: `(Expressed mathematically: [formula])`
- Keep derivations in collapsible sections
- Link to full proofs when available

### Linking Strategy
1. **First mention** of any RS concept gets linked
2. **Prerequisites** listed explicitly in metadata
3. **Related topics** show relationship type (prerequisite, extension, application)
4. **No orphan pages** - Every page links to/from at least 3 others
5. **Avoid circular prerequisites**

### Visual Guidelines
- **One primary visual** per page (concept diagram preferred)
- **SVG format** for diagrams
- **Alt text** must fully describe the concept shown
- **Captions** explain what to notice
- **Consistent color scheme**: 
  - Pink (#ff006e) for emphasis
  - Blue (#0066cc) for primary concepts
  - Gray (#64748b) for supporting elements

---

## QUALITY CHECKLIST

### Required Elements
- [ ] One-line essence at top
- [ ] Definition in 1-2 sentences
- [ ] Plain English explanation with analogy
- [ ] 3+ key properties
- [ ] 2+ testable predictions
- [ ] 3-5 FAQs
- [ ] 3+ related topics with relationship types
- [ ] Mathematical note (if applicable)

### Content Quality
- [ ] No undefined jargon
- [ ] No circular explanations
- [ ] At least one concrete example
- [ ] Clear causal mechanism ("how it works")
- [ ] Falsifiable predictions marked explicitly
- [ ] Common misconceptions addressed

### Technical Accuracy
- [ ] Consistent with RS framework
- [ ] Parameter-free claims
- [ ] Units specified where applicable
- [ ] Links to supporting proofs/papers
- [ ] No contradictions with other entries

### Accessibility
- [ ] Reading time accurate (150-200 words/min)
- [ ] Difficulty level appropriate
- [ ] Prerequisites listed
- [ ] Progressive disclosure (details in collapsible sections)
- [ ] Mobile-friendly layout

---

## CATEGORIES & DIFFICULTY LEVELS

### Categories
- **Physics**: Fundamental physical concepts (light, mass, forces)
- **Mathematics**: Mathematical structures and methods
- **Consciousness**: Awareness, recognition, agency
- **Computation**: Information processing, algorithms
- **Cosmology**: Large-scale structure and evolution

### Difficulty Levels
- **Foundational**: Core concepts everyone needs (ledger, recognition)
- **Intermediate**: Built on foundations (8-beat cycle, voxel grid)
- **Advanced**: Requires multiple prerequisites (LNAL, ledger curvature)
- **Expert**: Deep technical content (proof details, advanced predictions)

---

## AUTOMATION NOTES FOR AGENTS

### File Naming
- Slug format: `lowercase-with-hyphens`
- File path: `/encyclopedia/[slug].html`
- Image path: `/assets/images/encyclopedia/[slug].svg`

### Metadata Extraction
```python
# Extract from front matter
title: str
category: Literal["Physics", "Mathematics", "Consciousness", "Computation", "Cosmology"]
difficulty: Literal["Foundational", "Intermediate", "Advanced", "Expert"]
readingTime: int  # in minutes
tags: List[str]  # 3-6 tags
relatedConcepts: List[str]  # for auto-linking
prerequisites: Optional[List[str]]
```

### Auto-generated Elements
1. **Breadcrumb**: `Encyclopedia / {category} / {title}`
2. **Meta description**: First 160 chars of essence + definition
3. **Reading time**: Word count / 175
4. **Relationship types**: Infer from prerequisite graph

### Validation Rules
1. All internal links must resolve
2. No duplicate titles
3. Prerequisites must be lower or equal difficulty
4. At least 500 words, max 2500 words
5. Math expressions must be valid LaTeX

### Cross-referencing
- Build bidirectional link graph
- Auto-suggest related topics based on shared tags
- Flag orphan pages
- Detect circular prerequisites

---

## EXAMPLE ENTRIES TO STUDY

### Foundational
- The Ledger
- Recognition Events
- Positive Cost

### Intermediate  
- Light (current version to improve)
- 8-Beat Cycle
- Voxel Grid

### Advanced
- LNAL Machine Code
- Ledger Curvature
- Golden Ratio Scaling

### Expert
- Prime Grid Lossless
- Axiomatic Bridging
- Parameter-Free Predictions

---

## CSS CLASSES REFERENCE

```css
.encyclopedia-entry { /* Main container */ }
.essence { /* One-liner at top */ }
.meta-badges { /* Category, difficulty, time */ }
.definition-box { /* Highlighted definition */ }
.math-note { /* Inline math expressions */ }
.why-matters-callout { /* Impact section */ }
.mechanism-steps { /* How it works */ }
.properties-grid { /* Key properties cards */ }
.testable-box { /* Predictions section */ }
.misconception { /* Wrong vs right */ }
.faq-section { /* Collapsible Q&As */ }
.related-grid { /* Related topics cards */ }
.relation-type { /* Badge on related cards */ }
```

---

## VERSION HISTORY
- v2.0 (2024-12): Complete template with automation support
- v1.0 (2024-11): Initial template based on Light page

---

## NOTES FOR BACKGROUND AGENT

When creating encyclopedia entries:

1. **Start with prerequisites** - Build foundational concepts first
2. **Maintain consistency** - Use established terminology exactly
3. **Cross-link aggressively** - No isolated pages
4. **Validate predictions** - Must be specific and testable
5. **Progressive enhancement** - Can start simple, add sections later
6. **Track coverage** - Maintain list of planned vs completed entries
7. **Quality over quantity** - Better to have 50 excellent entries than 200 mediocre ones

Key principle: Each entry should teach one concept thoroughly while connecting it to the larger framework.
