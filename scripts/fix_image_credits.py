#!/usr/bin/env python3
"""Fix image credits to match local SVG images"""
import re
from pathlib import Path

def fix_credits_in_html(content):
    """Update image credits for local SVG images"""
    # Pattern to find figure elements with our local images
    pattern = r'(<figure[^>]*>.*?<img src="/assets/images/encyclopedia/[^"]+\.svg"[^>]*>.*?<figcaption>)(.*?)(</figcaption>)'
    
    def replace_caption(match):
        prefix = match.group(1)
        caption_content = match.group(2)
        suffix = match.group(3)
        
        # Extract just the caption text (before the bullet)
        caption_parts = caption_content.split('•')
        if len(caption_parts) > 0:
            caption_text = caption_parts[0].strip()
            # Replace with new credit
            new_caption = f'{caption_text} • <span class="figure-credit">Recognition Physics Institute</span> • <span class="figure-license">CC BY 4.0</span>'
            return prefix + new_caption + suffix
        return match.group(0)
    
    return re.sub(pattern, replace_caption, content, flags=re.DOTALL)

def main():
    enc_dir = Path("encyclopedia")
    fixed_count = 0
    
    for html_file in enc_dir.glob("*.html"):
        if html_file.name == "index.html":
            continue
        
        try:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            new_content = fix_credits_in_html(content)
            
            if new_content != content:
                html_file.write_text(new_content, encoding="utf-8")
                fixed_count += 1
                print(f"Fixed credits in: {html_file.name}")
                
        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")
    
    print(f"\nFixed credits in {fixed_count} HTML files")

if __name__ == "__main__":
    main()
