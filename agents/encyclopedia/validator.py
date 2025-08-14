import sys
from pathlib import Path

NEEDED = [
    "Definition",
    "In Plain English",
    "Why It Matters",
    "How It Works",
    "Key Properties",
    "Related Topics",
]


def main():
    if len(sys.argv) < 2:
        print("Usage: validator.py path/to/page.html")
        sys.exit(1)
    p = Path(sys.argv[1])
    if not p.exists():
        print(f"Not found: {p}")
        sys.exit(2)
    html = p.read_text(encoding="utf-8")
    errs = []
    for h in NEEDED:
        if h not in html:
            errs.append(f"Missing section: {h}")
    if errs:
        print("\n".join(errs))
        sys.exit(3)
    print("OK")


if __name__ == "__main__":
    main()
