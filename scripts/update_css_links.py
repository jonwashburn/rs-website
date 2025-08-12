#!/usr/bin/env python3
"""
Update all HTML files to use the new consolidated style.css
"""

import re
from pathlib import Path

def update_css_links(html_content, filepath):
    """Replace all CSS links with single style.css"""
    
    # Remove all existing CSS links (except fonts and external)
    patterns_to_remove = [
        r'<link[^>]*href="[^"]*(?:main|academic-style|encyclopedia|constants-styles)\.css[^"]*"[^>]*>\n?',
        r'<link[^>]*href="/assets/css/(?:main|academic-style|encyclopedia)\.css[^"]*"[^>]*>\n?'
    ]
    
    for pattern in patterns_to_remove:
        html_content = re.sub(pattern, '', html_content, flags=re.IGNORECASE)
    
    # Add new style.css if not already present
    if 'style.css' not in html_content and '</head>' in html_content:
        # Add after charset meta tag or at beginning of head
        if '<meta charset' in html_content:
            html_content = re.sub(
                r'(<meta charset[^>]*>)',
                r'\1\n  <link rel="stylesheet" href="/assets/css/style.css">',
                html_content,
                count=1
            )
        else:
            html_content = re.sub(
                r'(<head[^>]*>)',
                r'\1\n  <link rel="stylesheet" href="/assets/css/style.css">',
                html_content,
                count=1,
                flags=re.IGNORECASE
            )
    
    return html_content

def process_file(filepath):
    """Process a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = update_css_links(content, filepath)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def should_skip(filepath):
    """Skip certain files."""
    skip_patterns = [
        '_includes/', 'node_modules/', 'tools/', 'scripts/',
        '/._', '._', 'soul-', 'recognition-soul', 'demo', 'nft'
    ]
    return any(pattern in str(filepath) for pattern in skip_patterns)

def main():
    root = Path('.')
    updated_count = 0
    
    html_files = list(root.glob('**/*.html'))
    print(f"Found {len(html_files)} HTML files")
    print("Updating CSS links...\n")
    
    for filepath in sorted(html_files):
        if should_skip(filepath):
            continue
        
        if process_file(filepath):
            updated_count += 1
    
    print(f"\n✅ Updated {updated_count} files")

if __name__ == "__main__":
    main()
