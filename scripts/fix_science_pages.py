#!/usr/bin/env python3
"""
Fix the Science menu pages to use standard classes from style.css
"""

import re
from pathlib import Path

# Science menu pages
SCIENCE_PAGES = [
    'logical-foundations.html',
    'constants.html',
    'formulas/index.html',
    'measurement.html',
    'predictions.html',
    'future-predictions.html',
    'particle-masses.html',
    'encyclopedia/primes.html'
]

def normalize_classes(html_content):
    """Replace custom classes with standard ones from style.css"""
    
    # Class mappings
    replacements = [
        # Hero sections
        (r'class="constants-hero"', 'class="hero"'),
        (r'class="hero-content"', 'class="container"'),
        (r'class="hero-title"', 'class="hero-title"'),  # Keep this
        (r'class="hero-lead"', 'class="lead"'),
        (r'class="hero-stats"', 'class="mt-3"'),
        (r'class="eyebrow"', 'class="text-muted mb-2"'),
        (r'class="lede"', 'class="lead"'),
        
        # Sections
        (r'class="constants-section"', 'class="section"'),
        (r'class="symphony-section"', 'class="section"'),
        (r'class="constants-cta"', 'class="section text-center"'),
        (r'class="section alt"', 'class="section" style="background: var(--background-alt)"'),
        
        # Content containers
        (r'class="reading"', 'class="content"'),
        (r'class="container reading"', 'class="container"'),
        
        # Components
        (r'class="mystery-box"', 'class="card"'),
        (r'class="constant-explorer"', 'class="card"'),
        (r'class="old-constant-btn"', 'class="btn btn-secondary"'),
        (r'class="cta-btn primary"', 'class="btn btn-primary"'),
        (r'class="cta-btn secondary"', 'class="btn btn-secondary"'),
        (r'class="chip"', 'class="btn btn-secondary" style="font-size: 0.875rem; padding: 0.5rem 1rem; margin: 0.25rem"'),
        
        # Typography
        (r'class="section-title"', 'class="text-center"'),
        (r'class="cta-title"', 'class="mb-3"'),
        (r'class="cta-text"', 'class="lead mb-4"'),
        
        # Remove floating elements for now
        (r'<div class="floating-constants">.*?</div>', ''),
        (r'<div class="math-bg">.*?</div>', ''),
    ]
    
    for pattern_tuple in replacements:
        if len(pattern_tuple) == 3:  # Has flags
            old, new, flags = pattern_tuple
            html_content = re.sub(old, new, html_content, flags=flags)
        else:  # No flags
            old, new = pattern_tuple
            if new:  # Only replace if we have a replacement
                html_content = re.sub(old, new, html_content, flags=re.IGNORECASE)
            else:  # Remove if replacement is empty
                html_content = re.sub(old, new, html_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Clean up multiple spaces/newlines
    html_content = re.sub(r'\n\s*\n\s*\n', '\n\n', html_content)
    
    return html_content

def add_missing_placeholders(html_content):
    """Ensure footer placeholder exists"""
    if 'footer-placeholder' not in html_content and '</body>' in html_content:
        html_content = html_content.replace(
            '</body>',
            '\n  <div id="footer-placeholder"></div>\n</body>'
        )
    return html_content

def process_file(filepath):
    """Process a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = normalize_classes(content)
        content = add_missing_placeholders(content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {filepath}")
            return True
        else:
            print(f"  No changes needed: {filepath}")
        return False
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    root = Path('.')
    fixed_count = 0
    
    print("Fixing Science menu pages...\n")
    
    for page in SCIENCE_PAGES:
        filepath = root / page
        if filepath.exists():
            if process_file(filepath):
                fixed_count += 1
        else:
            print(f"⚠️  Not found: {page}")
    
    print(f"\n✅ Fixed {fixed_count} pages")

if __name__ == "__main__":
    main()
