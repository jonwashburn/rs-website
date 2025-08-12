#!/usr/bin/env python3
"""
Fix the remaining pages (Theory of Us, Questions, About) to use standard classes
"""

import re
from pathlib import Path

# Remaining pages to fix
PAGES_TO_FIX = [
    # Theory of Us menu
    'us.html',
    'us/religion.html',
    'us/philosophy.html',
    'us/ancient.html',
    'astrology/index.html',
    'us/health.html',
    'ethics.html',
    'us/community.html',
    'prophecy.html',
    
    # Questions
    'questions/index.html',
    
    # About menu
    'about.html',
    'about/recognition-physics.html',
    'about/jon-washburn.html',
    'about/contact.html',
    
    # Other top-level pages
    'reality.html',
    'downloads.html',
    'index.html'  # Homepage
]

def normalize_page_structure(html_content):
    """Ensure pages have proper structure and classes"""
    
    # Common class replacements
    replacements = [
        # Hero sections
        (r'class="hero-section"', 'class="hero"'),
        (r'class="hero-container"', 'class="container"'),
        (r'class="hero-text"', 'class="lead"'),
        (r'class="hero-heading"', 'class="hero-title"'),
        
        # Content sections
        (r'class="content-section"', 'class="section"'),
        (r'class="section-container"', 'class="container"'),
        (r'class="section-content"', 'class="content"'),
        (r'class="content-wrapper"', 'class="container"'),
        
        # Cards and boxes
        (r'class="feature-card"', 'class="card"'),
        (r'class="info-box"', 'class="card"'),
        (r'class="highlight-box"', 'class="card"'),
        
        # Buttons
        (r'class="primary-btn"', 'class="btn btn-primary"'),
        (r'class="secondary-btn"', 'class="btn btn-secondary"'),
        (r'class="cta-button"', 'class="btn btn-primary"'),
        
        # Typography
        (r'class="page-title"', 'class="hero-title"'),
        (r'class="section-heading"', 'class="text-center"'),
        (r'class="subtitle"', 'class="lead"'),
        (r'class="intro-text"', 'class="lead"'),
        
        # Lists
        (r'class="feature-list"', 'class="list-unstyled"'),
        (r'class="bullet-list"', 'class="list-unstyled"'),
        
        # Grids
        (r'class="feature-grid"', 'class="grid"'),
        (r'class="card-grid"', 'class="grid"'),
        
        # Remove redundant wrappers
        (r'<div class="page-wrapper">', ''),
        (r'</div><!-- \.page-wrapper -->', ''),
        (r'<div class="main-wrapper">', ''),
        (r'</div><!-- \.main-wrapper -->', ''),
    ]
    
    for old, new in replacements:
        html_content = re.sub(old, new, html_content, flags=re.IGNORECASE)
    
    # Ensure main content is wrapped properly
    if '<main' not in html_content and '<body' in html_content:
        # Find where body content starts (after header placeholder)
        header_match = re.search(r'<div id="header-placeholder"></div>\s*', html_content)
        if header_match:
            insert_pos = header_match.end()
            footer_match = re.search(r'\s*<div id="footer-placeholder"></div>', html_content)
            if footer_match:
                content_start = insert_pos
                content_end = footer_match.start()
                content = html_content[content_start:content_end]
                
                # Wrap content in main tag
                new_content = f'\n  <main>\n{content}\n  </main>\n'
                html_content = html_content[:content_start] + new_content + html_content[content_end:]
    
    # Clean up excessive whitespace
    html_content = re.sub(r'\n\s*\n\s*\n', '\n\n', html_content)
    
    return html_content

def add_missing_elements(html_content, filename):
    """Add missing header/footer placeholders and main.js"""
    
    # Ensure header placeholder
    if 'header-placeholder' not in html_content and '<body' in html_content:
        body_match = re.search(r'<body[^>]*>', html_content)
        if body_match:
            insert_pos = body_match.end()
            html_content = html_content[:insert_pos] + '\n  <div id="header-placeholder"></div>\n' + html_content[insert_pos:]
    
    # Ensure footer placeholder
    if 'footer-placeholder' not in html_content and '</body>' in html_content:
        html_content = html_content.replace(
            '</body>',
            '\n  <div id="footer-placeholder"></div>\n</body>'
        )
    
    # Ensure main.js is included
    if 'main.js' not in html_content and '</body>' in html_content:
        html_content = html_content.replace(
            '<div id="footer-placeholder"></div>',
            '<div id="footer-placeholder"></div>\n  <script src="/assets/js/main.js"></script>'
        )
    
    # Add page-specific class to body if missing
    if filename == 'index.html':
        html_content = re.sub(r'<body([^>]*)>', r'<body\1 class="homepage">', html_content)
    elif 'questions' in filename:
        html_content = re.sub(r'<body([^>]*)>', r'<body\1 class="questions-page">', html_content)
    elif 'about' in filename:
        html_content = re.sub(r'<body([^>]*)>', r'<body\1 class="about-page">', html_content)
    elif 'us' in filename or 'ethics' in filename or 'prophecy' in filename:
        html_content = re.sub(r'<body([^>]*)>', r'<body\1 class="theory-page">', html_content)
    
    return html_content

def process_file(filepath):
    """Process a single HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = normalize_page_structure(content)
        content = add_missing_elements(content, filepath.name)
        
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
    
    print("Fixing remaining pages...\n")
    
    for page in PAGES_TO_FIX:
        filepath = root / page
        if filepath.exists():
            if process_file(filepath):
                fixed_count += 1
        else:
            print(f"⚠️  Not found: {page}")
    
    print(f"\n✅ Fixed {fixed_count} pages")

if __name__ == "__main__":
    main()
