#!/usr/bin/env python3
"""
Strip inline styles from HTML files while preserving all content.
Removes:
- style="" attributes
- <style> blocks (except in special files)
- Excessive inline CSS
Preserves:
- All text content
- HTML structure
- Links, images, scripts
"""

import re
from pathlib import Path

def should_skip(filepath):
    """Skip certain files that need special handling."""
    skip_patterns = [
        'soul-', 'recognition-soul', 'nft', 'demo',
        '_includes/', 'test-styling', 'tools/', 'scripts/',
        '/._', '._'  # Mac files
    ]
    filename = filepath.name
    return any(pattern in str(filepath) for pattern in skip_patterns) or filename.startswith('._')

def strip_inline_styles(html_content, filepath):
    """Remove inline styles while preserving content."""
    
    # Remove style attributes but keep the elements
    html_content = re.sub(r'\s*style\s*=\s*"[^"]*"', '', html_content)
    html_content = re.sub(r"\s*style\s*=\s*'[^']*'", '', html_content)
    
    # Remove <style> blocks unless it's a special page
    if 'constants' not in str(filepath) and 'academic' not in str(filepath):
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Clean up excessive whitespace
    html_content = re.sub(r'\n\s*\n\s*\n', '\n\n', html_content)
    
    return html_content

def process_file(filepath):
    """Process a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        content = strip_inline_styles(content, filepath)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Cleaned: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    """Strip inline styles from all HTML files."""
    root = Path('.')
    cleaned_count = 0
    skipped_count = 0
    
    # Find all HTML files
    html_files = list(root.glob('**/*.html'))
    
    print(f"Found {len(html_files)} HTML files")
    print("Stripping inline styles...\n")
    
    for filepath in sorted(html_files):
        if should_skip(filepath):
            skipped_count += 1
            continue
        
        if process_file(filepath):
            cleaned_count += 1
    
    print(f"\n✅ Cleaned {cleaned_count} files")
    print(f"⏭️  Skipped {skipped_count} files")
    print(f"📄 Total processed: {len(html_files)}")

if __name__ == "__main__":
    main()
