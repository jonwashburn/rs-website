#!/usr/bin/env python3
"""Generate a JSON file listing all existing encyclopedia pages"""
import json
import os
from pathlib import Path

def generate_page_list():
    encyclopedia_dir = Path("encyclopedia")
    pages = []
    
    # Get all HTML files in encyclopedia directory
    for html_file in encyclopedia_dir.glob("*.html"):
        # Skip index.html
        if html_file.name == "index.html":
            continue
            
        slug = html_file.stem
        pages.append(slug)
    
    # Sort alphabetically
    pages.sort()
    
    # Write to JSON file
    output_file = "assets/data/existing-pages.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(pages, f, indent=2)
    
    print(f"Generated list of {len(pages)} existing encyclopedia pages")
    print(f"Saved to: {output_file}")
    
    return len(pages)

if __name__ == "__main__":
    generate_page_list()
