# 🎨 How to Make Site-Wide Style Changes

## YES! The Template is Fully Modular

Any change to `/assets/css/site-template.css` will instantly update all 288 pages!

## Quick Examples

### Want to change the primary blue color?
```css
/* In site-template.css, change this ONE line: */
--color-primary: #002855;  /* Current dark blue */
--color-primary: #1a365d;  /* Try a different blue */
```
**Result**: Every button, link, and accent changes across the entire site!

### Want bigger/smaller fonts?
```css
/* Adjust the type scale: */
--text-body: 0.95rem;   /* Current */
--text-body: 1rem;      /* Slightly bigger */
--text-body: 0.875rem;  /* Slightly smaller */
```
**Result**: All body text updates everywhere!

### Want more/less spacing?
```css
/* Change section spacing: */
--space-section: 0.75rem;  /* Current tight spacing */
--space-section: 1.5rem;   /* More breathing room */
```
**Result**: All sections get new spacing!

### Want a different warm background?
```css
/* Change the warm gradient: */
--color-bg-warm: linear-gradient(135deg, #fffbf0 0%, #fff7e6 100%);  /* Current */
--color-bg-warm: linear-gradient(135deg, #f0f4ff 0%, #e6ecff 100%);  /* Blue tint */
```
**Result**: All warm background sections change!

## Testing Changes

1. Edit `/assets/css/site-template.css`
2. Save the file
3. Refresh any page - changes appear immediately!
4. Commit when happy

## Adding New Global Styles

Just add to site-template.css:
```css
/* New global component */
.template-alert {
  background: var(--color-bg-warm);
  border: 2px solid var(--color-primary);
  padding: 1rem;
  border-radius: 8px;
}
```

Then use anywhere:
```html
<div class="template-alert">
  This alert appears consistently everywhere!
</div>
```

## Page-Specific Overrides

For unique page needs, create a page-specific CSS:
```html
<!-- In the page's <head> -->
<link rel="stylesheet" href="/assets/css/site-template.css">
<link rel="stylesheet" href="/assets/css/page-specific.css">
```

## Common Customizations

### 1. Header spacing too tight?
```css
.template-hero { padding: 2rem 0; }  /* Instead of 0.75rem */
```

### 2. Want rounded corners everywhere?
```css
--border-radius: 16px;  /* Add as variable */
.template-reading { border-radius: var(--border-radius); }
```

### 3. Different mobile sizes?
```css
@media (max-width: 768px) {
  --text-body: 1rem;  /* Bigger on mobile */
}
```

## The Power of Modularity

Change once in `site-template.css` → Updates 288 pages instantly!

No more hunting through individual files. No more inconsistencies. Just pure, modular design bliss. 🎉
