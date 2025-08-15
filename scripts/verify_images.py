#!/usr/bin/env python3
"""Verify all images in the manifest are accessible"""
import json
import urllib.request
import urllib.error
from pathlib import Path


def check_url(url: str) -> tuple[bool, str]:
    """Check if a URL is accessible"""
    try:
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return True, f"OK ({response.headers.get('Content-Type', 'unknown')})"
            else:
                return False, f"HTTP {response.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def main():
    manifest_path = Path("assets/data/encyclopedia-images.json")
    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}")
        return
    
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    
    print("Verifying image URLs...\n")
    
    errors = 0
    for page, data in manifest.items():
        print(f"Page: {page}")
        images = data.get("images", [data]) if isinstance(data, dict) else [data]
        
        for i, img in enumerate(images):
            src = img.get("src", "")
            alt = img.get("alt", "")
            
            # Skip local files
            if src.startswith("/"):
                print(f"  [{i+1}] Local file: {src}")
                continue
            
            # Check external URL
            ok, msg = check_url(src)
            if ok:
                print(f"  [{i+1}] ✓ {src[:60]}... - {msg}")
            else:
                print(f"  [{i+1}] ✗ {src[:60]}... - {msg}")
                errors += 1
                
                # Check fallbacks
                if "fallback_src" in img:
                    ok2, msg2 = check_url(img["fallback_src"])
                    print(f"       Fallback: {ok2 and '✓' or '✗'} - {msg2}")
        print()
    
    if errors > 0:
        print(f"\n⚠️  Found {errors} broken image(s)")
    else:
        print("\n✅ All images verified")


if __name__ == "__main__":
    main()
