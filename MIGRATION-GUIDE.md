# Template Migration Guide

## Safe Migration Strategy

### Why This Approach Works
- **Prefixed classes** (`template-*`) prevent conflicts
- **Gradual migration** - convert one page at a time
- **Preserves existing functionality** - old CSS stays intact
- **Easy rollback** - just remove the template CSS link

### Step-by-Step Page Conversion

#### 1. Add Template CSS
```html
<!-- After your main.css -->
<link rel="stylesheet" href="/assets/css/site-template.css">
```

#### 2. Update Body Class
```html
<!-- Change from -->
<body class="academic-page">

<!-- To -->
<body class="template-page">
```

#### 3. Convert HTML Structure

**Hero Sections:**
```html
<!-- Old -->
<section class="cosmic-hero">
  <div class="hero-content">

<!-- New -->
<section class="template-hero template-hero-framed">
  <div class="template-hero-content">
```

**Content Sections:**
```html
<!-- Old -->
<section class="content-section">
  <div class="container">

<!-- New -->  
<section class="template-section">
  <div class="template-container">
```

**Titles:**
```html
<!-- Old -->
<h2 class="section-title">

<!-- New -->
<h2 class="template-section-title">
```

**Content Cards:**
```html
<!-- Old -->
<div class="content-block">

<!-- New -->
<div class="template-reading">
```

**Buttons:**
```html
<!-- Old -->
<a href="#" class="btn primary">

<!-- New -->
<a href="#" class="template-btn template-btn-primary">
```

### Test Pages Available

1. **Template Demo**: `/template-test.html`
   - Shows all template components
   - Includes usage instructions

2. **About Page Example**: `/about-template-version.html`
   - Simplified version using template
   - Compare with original `/about.html`

### Conversion Priority

Start with simple pages first:
1. Static content pages (about, ethics, etc.)
2. List/index pages
3. Article pages
4. Interactive pages last

### Handling Special Cases

#### Pages with Heavy Inline Styles
Keep the inline styles but add template classes for structure:
```html
<section class="template-section" style="background: custom-gradient;">
```

#### Interactive Components
Keep original IDs and data attributes:
```html
<div class="template-container" id="interactive-widget" data-config="...">
```

#### Custom Layouts
Mix template utilities with custom CSS:
```html
<div class="template-container custom-grid-layout">
```

### Verification Checklist

After converting a page:
- [ ] Page loads without errors
- [ ] Navigation still works
- [ ] Interactive elements function
- [ ] Mobile view looks good
- [ ] Spacing feels consistent
- [ ] No visual regressions

### Rollback Plan

To revert a single page:
1. Remove template CSS link
2. Change body class back
3. Revert HTML class changes

To revert everything:
```bash
git revert [commit-hash]
```

### Next Steps

1. Test `/template-test.html` locally
2. Compare `/about.html` vs `/about-template-version.html`
3. Pick 2-3 simple pages to convert
4. Test thoroughly
5. Gradually roll out to more pages

### Common Issues

**Too much spacing?**
The template uses 0.75rem sections. Add custom overrides if needed:
```css
.needs-more-space {
  padding-top: 2rem !important;
}
```

**Conflicts with existing styles?**
The `template-` prefix should prevent most conflicts. If issues arise, add more specific selectors.

**JavaScript broken?**
Update your selectors:
```javascript
// Old
document.querySelector('.hero-content')

// New  
document.querySelector('.template-hero-content')
```
