#!/usr/bin/env python3
"""Remove duplicate images that appear after headings"""
import re

with open('encyclopedia/big-bang.html', 'r') as f:
    html = f.read()

# Pattern to find duplicate consecutive figure elements
pattern = r'(<figure class="concept-visual">.*?</figure>)(<figure class="concept-visual">.*?</figure>)'

def replacer(match):
    # Keep only the first figure (which has the onerror handler)
    return match.group(1)

# Remove duplicates
html = re.sub(pattern, replacer, html, flags=re.DOTALL)

with open('encyclopedia/big-bang.html', 'w') as f:
    f.write(html)

print("Removed duplicate figures")
