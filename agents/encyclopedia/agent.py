import os
import json
import argparse
import hashlib
import yaml
import re
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

try:
	from openai import OpenAI
except Exception:  # pragma: no cover
	OpenAI = None  # type: ignore

INDEX_FILE = ".index/theory_index.json"


def load_config(cfg_path: str) -> Dict[str, Any]:
	with open(cfg_path, "r", encoding="utf-8") as f:
		return yaml.safe_load(f)


def read_text(path: str) -> str:
	with open(path, "r", encoding="utf-8") as f:
		return f.read()


def strip_latex(src: str) -> str:
	"""Minimal LaTeX→text cleaning to improve retrieval while keeping content."""
	import re
	s = src
	# remove comments
	s = re.sub(r"%.*", "", s)
	# drop \begin{...}/\end{...} markers
	s = re.sub(r"\\begin\{.*?\}|\\end\{.*?\}", " ", s)
	# remove common preamble commands
	s = re.sub(r"\\(documentclass|usepackage|title|author|date|maketitle)[^\n]*", " ", s)
	# braces
	s = re.sub(r"[{}]", "", s)
	# collapse whitespace
	s = re.sub(r"\s+", " ", s)
	return s.strip()


def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
	words = text.split()
	chunks = []
	start = 0
	while start < len(words):
		end = min(len(words), start + chunk_size)
		chunks.append(" ".join(words[start:end]))
		if end == len(words):
			break
		start = max(end - overlap, start + 1)
	return chunks


def embed_texts(client: Any, model: str, texts: List[str]) -> List[List[float]]:
	resp = client.embeddings.create(model=model, input=texts)
	# openai>=1.0 returns objects with `.embedding` attribute
	return [d.embedding for d in resp.data]


def ensure_index(cfg: Dict[str, Any], force: bool = False) -> Dict[str, Any]:
	index_path = Path(cfg["index_dir"]) / "theory_index.json"
	index_path.parent.mkdir(parents=True, exist_ok=True)

	if index_path.exists() and not force:
		with open(index_path, "r", encoding="utf-8") as f:
			return json.load(f)

	assert OpenAI is not None, "openai library not available"
	client = OpenAI()
	# Load one or multiple theory paths
	paths = cfg.get("theory_paths") or [cfg.get("theory_path")]
	texts: List[str] = []
	for p in paths:
		if not p:
			continue
		raw = read_text(p)
		if p.lower().endswith((".tex", ".ltx")):
			raw = strip_latex(raw)
		texts.append(raw)
	text = "\n\n".join(texts)
	chunks = chunk_text(text, cfg.get("chunk_size", 1400), cfg.get("chunk_overlap", 200))
	embs = embed_texts(client, cfg["embedding_model"], chunks)
	index = {"model": cfg["embedding_model"], "chunks": chunks, "embeddings": embs}
	with open(index_path, "w", encoding="utf-8") as f:
		json.dump(index, f)
	return index


def retrieve(cfg: Dict[str, Any], query: str, k: int) -> List[Dict[str, Any]]:
	index_path = Path(cfg["index_dir"]) / "theory_index.json"
	with open(index_path, "r", encoding="utf-8") as f:
		index = json.load(f)
	assert OpenAI is not None, "openai library not available"
	client = OpenAI()
	q_emb = embed_texts(client, index["model"], [query])[0]
	M = np.array(index["embeddings"], dtype=float)
	sim = cosine_similarity([q_emb], M)[0]
	order = np.argsort(-sim)[:k]
	return [{"text": index["chunks"][i], "score": float(sim[i])} for i in order]


def slugify(title: str) -> str:
	return title.lower().replace(" ", "-").replace("/", "-")


# Stable anchors for encyclopedia categories (used by breadcrumbs)
CATEGORY_ANCHORS: Dict[str, str] = {
	"Recognition Physics Fundamentals": "fundamentals",
	"Fundamental Constants": "constants",
	"Quantum & Particle Physics": "quantum",
	"Spacetime & Gravity": "spacetime-gravity",
	"Thermodynamics & Statistical": "thermo-stat",
	"Cosmology & Astrophysics": "cosmology",
	"Chemistry & Materials": "chemistry-materials",
	"Biology & Consciousness": "biology-consciousness",
	"Mathematics & Computation": "math-computation",
	"Advanced Physics & Technology": "advanced-tech",
}


def load_crosslinks() -> Dict[str, Any]:
	"""Load cross-link map with aliases if available."""
	try:
		p = Path(__file__).parent / "crosslinks.json"
		if p.exists():
			with open(p, "r", encoding="utf-8") as f:
				return json.load(f)
	except Exception:
		pass
	return {}


def load_rs_facts() -> Dict[str, Any]:
	try:
		p = Path(__file__).parent / "rs_facts.json"
		if p.exists():
			with open(p, "r", encoding="utf-8") as f:
				return json.load(f)
	except Exception:
		pass
	return {}


def load_policy_for(category: str) -> Dict[str, Any]:
	try:
		p = Path(__file__).parent / "policies" / "cosmology.json"
		if category.startswith("Cosmology") and p.exists():
			with open(p, "r", encoding="utf-8") as f:
				return json.load(f)
	except Exception:
		pass
	return {}



def build_prompt(system_prompt: str, template_md: str, task: Dict[str, Any], contexts: List[Dict[str, Any]]) -> List[Dict[str, str]]:
	ctx = "\n\n".join([c["text"] for c in contexts])
	xlinks = load_crosslinks()
	rsfacts = load_rs_facts()
	policy = load_policy_for(task.get("category", ""))
	user = f"""
Generate a complete encyclopedia HTML page following the house classes and section order.
Title: {task.get('title')}
Category: {task.get('category','Physics')}
Difficulty: {task.get('difficulty','Foundational')}
Tags: {', '.join(task.get('tags', []))}
Summary: {task.get('summary','')}

Use only the following theory context and your prior RS style rules:
---
{ctx}
---

Cross-linking rules (strict):
- Use the cross-link map below. On first natural mention of any key or alias, wrap that phrase in an <a> to the mapped URL. Do not over-link; one link per concept per section is enough.
- If a concept is not in the map, link to /encyclopedia/{{slugified-title}} when it obviously corresponds to an existing page.
- Maintain clean HTML; no markdown. Example: <a href="/encyclopedia/the-ledger.html">the ledger</a>.

Cross-link map (aliases allowed):
{json.dumps(xlinks)[:4000]}

Canonical RS facts (cite precisely where relevant):
{json.dumps(rsfacts)[:2000]}

Category policy (must satisfy):
{json.dumps(policy)[:2000]}

Output only the body content for the encyclopedia section, without markdown code fences.
""".strip()
	return [
		{"role": "system", "content": system_prompt},
		{"role": "user", "content": user},
	]


def sanitize_and_wrap(html_body: str, task: Dict[str, Any]) -> str:
	# strip markdown code fences if present
	body = re.sub(r"```[a-zA-Z]*", "", html_body)
	body = body.replace("```", "")
	body = body.strip()
	
	# Extract metadata
	category = task.get("category", "Physics")
	difficulty = task.get("difficulty", "Foundational")
	tags = ", ".join(task.get("tags", []))
	title = task.get("title", "")
	summary = task.get("summary", "")
	
	# If body already contains our container, keep as-is
	if "template-container" in body and "template-reading" in body:
		return body
	
	# Extract the h1 from body if it exists, otherwise create it
	h1_match = re.search(r'<h1>(.*?)</h1>', body)
	if h1_match:
		h1_content = h1_match.group(1)
		body = body.replace(h1_match.group(0), '')  # Remove h1 from body
	else:
		h1_content = title
	
	# Try to make last word pink if it's a compound title
	words = h1_content.split()
	if len(words) > 1:
		h1_formatted = ' '.join(words[:-1]) + f' <span class="template-accent-text">{words[-1]}</span>'
	else:
		h1_formatted = h1_content
	
	# Build breadcrumbs (Home / Encyclopedia / Category)
	cat = task.get("category", "")
	cat_anchor = CATEGORY_ANCHORS.get(cat, cat.lower().replace(" ", "-").replace("/", "-"))
	breadcrumbs = (
		'<nav class="enc-breadcrumbs">'
		'<a href="/index.html">Home</a>'
		'<span class="sep">/</span>'
		'<a href="/encyclopedia/index.html">Encyclopedia</a>'
		+ (f'<span class="sep">/</span><a href="/encyclopedia/index.html#cat-{cat_anchor}">{cat}</a>' if cat else '')
		+ '</nav>'
	)

	# Build hero box with framed design (matching academic.html)
	hero_box = (
		f'<div class="encyclopedia-hero">'
		f'<p class="template-hero-badge">ENCYCLOPEDIA ENTRY</p>'
		f'<h1>{h1_formatted}</h1>'
		+ (f'<p class="lead-text">{summary}</p>' if summary else '')
		+ f'<div class="meta-badges">'
		f'<span class="category-badge">{category}</span>'
		f'<span class="difficulty-badge">{difficulty}</span>'
		+ (f'<span class="tags">{tags}</span>' if tags else '')
		+ '</div>'
		f'</div>'
	)

	# Optional hero image/figure support via task metadata
	# Supported fields:
	# - task["hero_image"]: {src, alt, caption, credit}
	# - task["images"]: [ {src, alt, caption, credit, placement: "hero"|"inline"} ]
	hero_fig_html = ""
	try:
		images = task.get("images", []) or []
		# Prefer explicit hero_image, otherwise first with placement hero/banner
		hero_image = task.get("hero_image") or next(
			(img for img in images if str(img.get("placement", "")).lower() in ("hero", "banner")),
			None,
		)
		if hero_image is not None:
			# Default src falls back to slug.svg under assets
			default_src = f"/assets/images/encyclopedia/{slugify(title)}.svg"
			src = hero_image.get("src") or default_src
			alt = hero_image.get("alt") or title
			caption = hero_image.get("caption", "")
			credit = hero_image.get("credit", "")
			credit_html = f'<span class="figure-credit">{credit}</span>' if credit else ""
			cap_html = (
				f"<figcaption>{caption}{(' • ' + credit_html) if caption and credit_html else credit_html}</figcaption>"
				if (caption or credit)
				else ""
			)
			hero_fig_html = (
				'<figure class="concept-visual">'
				f'<img src="{src}" alt="{alt}" loading="lazy" decoding="async" />'
				f"{cap_html}"
				"</figure>"
			)
	except Exception:
		# Do not fail page generation if image metadata is malformed
		hero_fig_html = ""
	
	wrapped = (
		'<section class="template-section encyclopedia-entry">'
		'<div class="template-container">'
		+ breadcrumbs + hero_box + hero_fig_html +
		'<div class="template-reading">'
		+ body +
		'</div></div></section>'
	)
	return wrapped


def call_model(cfg: Dict[str, Any], messages: List[Dict[str, str]]) -> str:
	assert OpenAI is not None, "openai library not available"
	client = OpenAI()
	primary = cfg.get("model", "gpt-4o-mini")
	fallback = cfg.get("fallback_model", "gpt-4o-mini")
	allow_fallback = cfg.get("allow_fallback", True)
	# Prefer Responses API for GPT-5 with reasoning/verbosity if available
	use_responses = primary.startswith("gpt-5")
	try:
		if use_responses and hasattr(client, "responses"):
			resp = client.responses.create(
				model=primary,
				input=[{"role":"system","content":messages[0]["content"]},{"role":"user","content":messages[1]["content"]}],
				reasoning={"effort": cfg.get("reasoning_effort", "medium")},
				text={"verbosity": cfg.get("verbosity", "medium")}
			)
			content = getattr(resp, "output_text", None) or (resp.output[0].content[0].text if getattr(resp, "output", None) else "")
		else:
			resp = client.chat.completions.create(
				model=primary,
				messages=messages,
				max_tokens=cfg.get("max_tokens", 3000),
				temperature=0.3,
			)
			content = resp.choices[0].message.content or ""
		reason = None
	except Exception as e:
		if not allow_fallback:
			raise e
		# Fallback on model-not-found or any transport error (if allowed)
		resp = client.chat.completions.create(
			model=fallback,
			messages=messages,
			max_tokens=cfg.get("max_tokens", 3000),
			temperature=0.3,
		)
		reason = f"fallback_used:{type(e).__name__}"
	# Attach a small tag in the content if fallback was used (non-rendering HTML comment)
	if content and 'reason' in locals() and reason:
		content = f"<!-- {reason} -->\n" + content
	return content


def minimal_validate(html: str) -> List[str]:
	errs = []
	needed = [
		"Essence",
		"Definition",
		"In Plain English",
		"Why It Matters",
		"How It Works",
		"Key Properties",
		"Connections",
		"Testable Predictions",
		"Related Topics",
	]
	for h in needed:
		if h not in html:
			errs.append(f"Missing section: {h}")
	if "template-section" not in html:
		errs.append("Missing template wrapper")
	return errs


def write_page(out_dir: Path, slug: str, html_body: str) -> None:
	out_dir.mkdir(parents=True, exist_ok=True)
	path = out_dir / f"{slug}.html"
	page = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
	<meta charset=\"UTF-8\" />
	<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
	<meta http-equiv=\"Content-Security-Policy\" content=\"script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://polyfill.io; style-src 'self' 'unsafe-inline';\">
	<title>{slug}</title>
	<link rel=\"stylesheet\" href=\"/assets/css/main.css\" />
	<link rel=\"stylesheet\" href=\"/assets/css/site-template.css\" />
	<link rel=\"stylesheet\" href=\"/assets/css/encyclopedia.css\" />
	<link rel=\"stylesheet\" href=\"/style.css\" />
	
	<!-- MathJax Configuration -->
	<script>
	window.MathJax = {{
		tex: {{
			inlineMath: [['\\\\(', '\\\\)']],
			displayMath: [['\\\\[', '\\\\]']],
			processEscapes: true
		}},
		options: {{
			skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
		}},
		startup: {{
			ready: () => {{
				MathJax.startup.defaultReady();
				// Process math-note elements after MathJax is ready
				document.querySelectorAll('math-note').forEach(function(note) {{
					const content = note.textContent.trim();
					if (!content.startsWith('\\\\(') && !content.startsWith('\\\\[')) {{
						note.innerHTML = '\\\\(' + content + '\\\\)';
					}}
				}});
				// Re-typeset the page
				MathJax.typesetPromise();
			}}
		}}
	}};
	</script>
	<script src=\"https://polyfill.io/v3/polyfill.min.js?features=es6\"></script>
	<script src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js\"></script>
</head>
<body class=\"template-page\">
	<div id=\"header-placeholder\"></div>
{html_body}
	<div id=\"footer-placeholder\"></div>
	<script src=\"/assets/js/main.js\"></script>
</body>
</html>
"""
	with open(path, "w", encoding="utf-8") as f:
		f.write(page)


def main():
	ap = argparse.ArgumentParser()
	ap.add_argument("--reindex", action="store_true")
	ap.add_argument("--tasks", type=str, default="")
	ap.add_argument("--out", type=str, default="rs-website/encyclopedia")
	ap.add_argument("--max-items", type=int, default=0)
	ap.add_argument("--model", type=str, default="")
	ap.add_argument("--dry-run", action="store_true")
	args = ap.parse_args()

	# Load config from the agent folder
	agent_dir = Path(__file__).parent
	cfg = load_config(str(agent_dir / "config.yaml"))
	if args.model:
		cfg["model"] = args.model

	if args.reindex:
		ensure_index(cfg, force=True)
		print("Index rebuilt.")
		return

	if not args.tasks:
		print("--tasks required")
		return

	with open(args.tasks, "r", encoding="utf-8") as f:
		items = json.load(f)
	if args.max_items:
		items = items[: args.max_items]

	# Make sure index exists
	ensure_index(cfg, force=False)

	sys_prompt = read_text(str(agent_dir / "system_prompt.md"))
	template_md = read_text(cfg.get("template_path", "ENCYCLOPEDIA-TEMPLATE.md"))
	out_dir = Path(args.out)

	for task in items:
		slug = slugify(task["title"]) if "slug" not in task else task["slug"]
		out_path = out_dir / f"{slug}.html"
		if out_path.exists() and not task.get("overwrite", False):
			print(f"Skip existing: {slug}")
			continue
			
		q = f"Recognition Physics Encyclopedia page: {task['title']} in category {task.get('category','Physics')}"
		ctx = retrieve(cfg, q, cfg.get("retrieve_k", 8))
		messages = build_prompt(sys_prompt, template_md, task, ctx)
		raw = call_model(cfg, messages)
		html_body = sanitize_and_wrap(raw, task)
		errs = minimal_validate(html_body)
		if errs:
			print(f"Validation warnings for {slug}: {errs}")
		if args.dry_run:
			print(f"--- {slug} ---\n{html_body[:500]}...\n")
			continue
		write_page(out_dir, slug, html_body)
		print(f"Wrote: {out_path}")


if __name__ == "__main__":
	main()
