#!/usr/bin/env python3
"""Download Wikipedia images locally to avoid hotlinking issues"""
import os
import urllib.request
from pathlib import Path

images = [
    {
        "url": "https://upload.wikimedia.org/wikipedia/commons/6/6f/CMB_Timeline300_no_WMAP.jpg",
        "filename": "cmb-timeline.jpg"
    },
    {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Universe_expansion.png/600px-Universe_expansion.png", 
        "filename": "universe-expansion.png"
    },
    {
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Planck_satellite_cmb.jpg/600px-Planck_satellite_cmb.jpg",
        "filename": "planck-cmb.jpg"
    }
]

# Create directory
img_dir = Path("assets/images/encyclopedia")
img_dir.mkdir(parents=True, exist_ok=True)

for img in images:
    dest = img_dir / img["filename"]
    if not dest.exists():
        print(f"Downloading {img['filename']}...")
        try:
            urllib.request.urlretrieve(img["url"], dest)
            print(f"  Downloaded to {dest}")
        except Exception as e:
            print(f"  ERROR: {e}")
    else:
        print(f"Already exists: {dest}")
