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
	text = read_text(cfg["theory_path"])
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


def build_prompt(system_prompt: str, template_md: str, task: Dict[str, Any], contexts: List[Dict[str, Any]]) -> List[Dict[str, str]]:
	ctx = "\n\n".join([c["text"] for c in contexts])
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
	# ensure container structure and meta badges
	category = task.get("category", "Physics")
	difficulty = task.get("difficulty", "Foundational")
	tags = ", ".join(task.get("tags", []))
	title = task.get("title", "")
	# If body already contains our container, keep as-is
	if "template-container" in body and "template-reading" in body:
		return body
	# Avoid duplicate H1 if already present
	maybe_h1 = "" if "<h1" in body.lower() else f"<h1>{title}</h1>"
	meta = (
		f"<p class=\"template-hero-badge\">Encyclopedia / {category} / {title}</p>"
		f"<div class=\"meta-badges\">"
		f"<span class=\"category-badge\">{category}</span>"
		f"<span class=\"difficulty-badge\">{difficulty}</span>"
		+ (f"<span class=\"tags\">{tags}</span>" if tags else "")
		+ "</div>"
	)
	wrapped = (
		"<section class=\"template-section encyclopedia-entry\">"
		"<div class=\"template-container\">"
		"<div class=\"template-reading\">"
		+ meta + maybe_h1 + body +
		"</div></div></section>"
	)
	return wrapped


def call_model(cfg: Dict[str, Any], messages: List[Dict[str, str]]) -> str:
	assert OpenAI is not None, "openai library not available"
	client = OpenAI()
	resp = client.chat.completions.create(
		model=cfg.get("model", "gpt-4o-mini"),
		messages=messages,
		max_tokens=cfg.get("max_tokens", 3000),
		temperature=0.3,
	)
	return resp.choices[0].message.content or ""


def minimal_validate(html: str) -> List[str]:
	errs = []
	needed = ["Definition", "In Plain English", "Why It Matters", "How It Works", "Key Properties", "Related Topics"]
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
	<title>{slug}</title>
	<link rel=\"stylesheet\" href=\"/assets/css/main.css\" />
	<link rel=\"stylesheet\" href=\"/assets/css/site-template.css\" />
	<link rel=\"stylesheet\" href=\"/style.css\" />
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
