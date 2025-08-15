# Recognition Physics – Encyclopedia Agent

A lightweight background agent to generate Encyclopedia pages from tasks, aligned to the theory.

Core sources:
- `rs-website/ENCYCLOPEDIA-TEMPLATE.md` (authoring template)
- `rs-website/Empirical Measurement of Reality.txt` (primary theory document)

## Quick start

1) Create a virtual environment and install dependencies
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r rs-website/agents/encyclopedia/requirements.txt
```

2) Set your API key
```bash
export OPENAI_API_KEY=YOUR_KEY
```

3) Build the knowledge index from the theory document (first run)
```bash
python rs-website/agents/encyclopedia/agent.py --reindex
```

4) Run on sample tasks
```bash
python rs-website/agents/encyclopedia/agent.py \
  --tasks rs-website/agents/encyclopedia/tasks.sample.json \
  --out rs-website/encyclopedia
```

Pages will be written to `rs-website/encyclopedia/{slug}.html`.

## How it works
- Chunks `Empirical Measurement of Reality.txt`, builds embeddings (text-embedding-3-small), stores under `.index/theory_index.json`
- Loads `system_prompt.md` and the template
- Retrieves top theory chunks per task and prompts a model to produce a full HTML page following house style
- Validates minimal quality gates (required sections, related topics)

## Task format
Provide a JSON file with a list of page specs:
```json
[
  {
    "title": "Light",
    "category": "Physics",
    "difficulty": "Intermediate",
    "tags": ["recognition", "propagation", "invariance"],
    "summary": "The universe's messaging system—one voxel per tick.",
    "overwrite": false
  }
]
```

## CLI
```bash
python rs-website/agents/encyclopedia/agent.py \
  --tasks PATH/TO/tasks.json \
  --out rs-website/encyclopedia \
  --max-items 20 \
  --model gpt-4o-mini \
  --dry-run
```

Flags:
- `--reindex` rebuild the theory index
- `--tasks` path to tasks JSON
- `--out` output directory for generated pages
- `--max-items` limit processed items
- `--model` override default model
- `--dry-run` print results without writing files

## Validator
Run a post-check on any generated file:
```bash
python rs-website/agents/encyclopedia/validator.py rs-website/encyclopedia/light.html | cat
```
Checks for:
- Required sections and badges
- Minimum structure
- Related topics present

## Notes
- The index lives under `rs-website/agents/encyclopedia/.index/` (ignored by git)
- Existing files are skipped unless `overwrite: true`
- Adjust style via `system_prompt.md` and `ENCYCLOPEDIA-TEMPLATE.md`

## Image Guidelines
To avoid broken images in generated pages:
1. **Always verify image URLs exist** before adding to manifest:
   ```bash
   python rs-website/scripts/verify_images.py
   ```
2. **Prefer stable sources**:
   - NASA/ESA official sites (usually public domain)
   - Wikimedia Commons (check the actual filename exists)
   - Local files in `/assets/images/encyclopedia/`
3. **Test with curl** before adding:
   ```bash
   curl -I "https://example.com/image.jpg"  # Should return 200 OK
   ```
4. **Use the manifest** (`assets/data/encyclopedia-images.json`) for post-processing images rather than embedding in agent tasks
