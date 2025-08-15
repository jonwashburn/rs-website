#!/usr/bin/env python3
"""
Cache CC images from upload.wikimedia.org locally and rewrite encyclopedia pages
and the image manifest to use local paths. Preserves attribution in captions
and adds source_url into the manifest for provenance.

Enhancements:
- Scan both HTML files and the images manifest for Wikimedia URLs
- On 404 for thumb URLs, fall back to the original file URL
- If still failing, fetch via Special:FilePath with width to obtain a working rendition
- Process any remaining Wikimedia URLs on the fly while rewriting HTML/manifest
- Final verification for any remaining Wikimedia URLs in HTML and manifest
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, urlunparse, quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ENC_DIR = ROOT / "encyclopedia"
ASSETS_DIR = ROOT / "assets" / "images" / "encyclopedia"
MANIFEST_FILE = ROOT / "assets" / "data" / "encyclopedia-images.json"

TARGET_HOST = "upload.wikimedia.org"
USER_AGENT = (
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
	"AppleWebKit/537.36 (KHTML, like Gecko) "
	"Chrome/126.0.0.0 Safari/537.36"
)
TIMEOUT_SECS = 25


def is_wikimedia(url: str) -> bool:
	try:
		parsed = urlparse(url)
		return parsed.netloc.lower().endswith(TARGET_HOST)
	except Exception:
		return False


def extension_from_url(url: str) -> str:
	path = urlparse(url).path
	ext = os.path.splitext(path)[1]
	return ext if ext else ".bin"


def hashed_filename(url: str) -> str:
	# Use sha1 of URL to ensure uniqueness, preserve extension
	sha = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
	return f"{sha}{extension_from_url(url)}"


# --- Wikimedia thumb helpers ---
THUMB_RE = re.compile(r"^/wikipedia/commons/thumb/([0-9a-fA-F])/([0-9a-fA-F]{2})/([^/]+)/(?:\d+px-)?([^/]+)$")


def extract_filename_from_url(url: str) -> Optional[str]:
	try:
		parsed = urlparse(url)
		# Try thumb pattern
		m = THUMB_RE.match(parsed.path)
		if m:
			_group_a, _group_b, file_name, _tail = m.groups()
			return file_name
		# Fallback: last path component
		parts = parsed.path.rstrip('/').split('/')
		if parts:
			return parts[-1]
		return None
	except Exception:
		return None


def thumb_to_original(url: str) -> Optional[str]:
	"""Convert a Wikimedia thumb URL to the original file URL."""
	try:
		parsed = urlparse(url)
		m = THUMB_RE.match(parsed.path)
		if not m:
			return None
		group_a, group_b, file_name, _tail = m.groups()
		orig_path = f"/wikipedia/commons/{group_a}/{group_b}/{file_name}"
		return urlunparse((parsed.scheme, parsed.netloc, orig_path, "", "", ""))
	except Exception:
		return None


def download(url: str, dest: Path) -> bool:
	try:
		dest.parent.mkdir(parents=True, exist_ok=True)
		req = Request(url, headers={"User-Agent": USER_AGENT})
		with urlopen(req, timeout=TIMEOUT_SECS) as resp:
			data = resp.read()
		dest.write_bytes(data)
		return True
	except Exception as e:
		print(f"WARN: failed to download {url}: {e}")
		return False


def download_with_fallbacks(orig_url: str, dest_dir: Path) -> Optional[Path]:
	"""Try downloading url; if it fails, try original-from-thumb; then Special:FilePath."""
	# 1) direct
	filename = hashed_filename(orig_url)
	dest = dest_dir / filename
	if download(orig_url, dest):
		return dest
	# 2) original from thumb
	orig = thumb_to_original(orig_url)
	if orig:
		filename = hashed_filename(orig)
		dest2 = dest_dir / filename
		if download(orig, dest2):
			return dest2
	# 3) Special:FilePath
	fname = extract_filename_from_url(orig_url)
	if fname:
		filepath_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(fname)}?width=1200"
		filename = hashed_filename(filepath_url)
		dest3 = dest_dir / filename
		if download(filepath_url, dest3):
			return dest3
	return None


def find_img_srcs(html: str) -> list:
	# Capture src in double or single quotes
	pattern = re.compile(r"<img[^>]+src=([\"'])([^\"']+)\1", re.IGNORECASE)
	return [m.group(2) for m in pattern.finditer(html)]


def replace_src(html: str, old: str, new: str) -> str:
	return html.replace(old, new)


def process_html_file(html_path: Path, url_to_local: dict, cache_dir: Path) -> bool:
	content = html_path.read_text(encoding="utf-8", errors="ignore")
	srcs = find_img_srcs(content)
	changed = False
	for src in srcs:
		if is_wikimedia(src):
			local_path = url_to_local.get(src)
			if not local_path:
				local_file = download_with_fallbacks(src, cache_dir)
				if not local_file:
					continue
				local_path = f"/assets/images/encyclopedia/_cache/{local_file.name}"
				url_to_local[src] = local_path
			new_content = replace_src(content, src, local_path)
			if new_content != content:
				content = new_content
				changed = True
	if changed:
		html_path.write_text(content, encoding="utf-8")
	return changed


def process_manifest(url_to_local: dict, cache_dir: Path) -> bool:
	if not MANIFEST_FILE.exists():
		return False
	with MANIFEST_FILE.open("r", encoding="utf-8") as f:
		manifest = json.load(f)
	changed = False
	for page_id, page in manifest.items():
		images = page.get("images", [])
		for img in images:
			src = img.get("src", "")
			if is_wikimedia(src):
				local = url_to_local.get(src)
				if not local:
					local_file = download_with_fallbacks(src, cache_dir)
					if not local_file:
						continue
					local = f"/assets/images/encyclopedia/_cache/{local_file.name}"
					url_to_local[src] = local
				img["source_url"] = src
				img["src"] = local
				changed = True
	if changed:
		with MANIFEST_FILE.open("w", encoding="utf-8") as f:
			json.dump(manifest, f, indent=2)
	return changed


def collect_wikimedia_urls() -> set:
	urls: set = set()
	# From HTML
	for html_file in sorted(ENC_DIR.glob("*.html")):
		if html_file.name == "index.html":
			continue
		content = html_file.read_text(encoding="utf-8", errors="ignore")
		for src in find_img_srcs(content):
			if is_wikimedia(src):
				urls.add(src)
	# From manifest
	if MANIFEST_FILE.exists():
		with MANIFEST_FILE.open("r", encoding="utf-8") as f:
			manifest = json.load(f)
		for page_id, page in manifest.items():
			for img in page.get("images", []):
				src = img.get("src", "")
				if is_wikimedia(src):
					urls.add(src)
	return urls


def main():
	url_to_local = {}
	cache_dir = ASSETS_DIR / "_cache"
	cache_dir.mkdir(parents=True, exist_ok=True)

	# Pre-scan and cache
	all_urls = collect_wikimedia_urls()
	if all_urls:
		print(f"Found {len(all_urls)} wikimedia URLs. Downloading locally...")
		for url in sorted(all_urls):
			local_file = download_with_fallbacks(url, cache_dir)
			if not local_file:
				continue
			local_src = f"/assets/images/encyclopedia/_cache/{local_file.name}"
			url_to_local[url] = local_src
			print(f"Cached: {url} -> {local_src}")

	# Rewrite HTML (and cache any missed URLs on the fly)
	updated_files = 0
	for html_file in sorted(ENC_DIR.glob("*.html")):
		if html_file.name == "index.html":
			continue
		if process_html_file(html_file, url_to_local, cache_dir):
			updated_files += 1
	print(f"Rewrote {updated_files} HTML files")

	# Rewrite manifest (and cache any missed URLs on the fly)
	if process_manifest(url_to_local, cache_dir):
		print("Updated manifest with local Wikimedia image paths")

	# Final check: ensure no upload.wikimedia.org remain in HTML
	remaining_html = 0
	for html_file in sorted(ENC_DIR.glob("*.html")):
		text = html_file.read_text(encoding="utf-8", errors="ignore")
		if TARGET_HOST in text:
			remaining_html += 1
	print(f"Remaining HTML files containing '{TARGET_HOST}': {remaining_html}")

	# Final check: ensure no upload.wikimedia.org remain in manifest
	remaining_manifest = 0
	if MANIFEST_FILE.exists():
		with MANIFEST_FILE.open("r", encoding="utf-8") as f:
			manifest = json.load(f)
		for page_id, page in manifest.items():
			for img in page.get("images", []):
				src = img.get("src", "")
				if TARGET_HOST in src:
					remaining_manifest += 1
	print(f"Remaining manifest entries containing '{TARGET_HOST}': {remaining_manifest}")

if __name__ == "__main__":
	sys.exit(main() or 0)
