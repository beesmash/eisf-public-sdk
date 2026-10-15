#!/usr/bin/env python3
"""Read-only, metadata-only index of OpenAI October 2026 math release.

Do not treat source claims or available Lean files as independently proven.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

FAMILY_RE = re.compile(r"(?m)^\*\*(\d{3})\.\s*(.+?)\*\*")
PDF_RE = re.compile(r"\[([^\]]+)\]\((preprints/[^)]+\.pdf)\)")
WITHDRAWN = (
    "algebraicity-of-weil-classes-on-split-abelian-eightfolds",
    "algebraicity-of-kuga-satake-correspondences-for-k3-surfaces",
    "the-rational-hodge-conjecture-for-products-of-k3-surfaces",
)

def file_sha256(file: Path) -> str:
    digest = hashlib.sha256()
    with file.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main() -> None:
    if len(sys.argv) not in (2, 3):
        raise SystemExit("usage: python3 tools/openai_math_catalog.py SOURCE_REPO [OUTPUT_JSON]")
    repo = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2]) if len(sys.argv) == 3 else Path(".research/openai-math-catalog.json")
    if not (repo / "LICENSE").is_file():
        raise SystemExit("Expected complete upstream checkout and LICENSE")
    sha = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True
    ).stdout.strip()
    contents = (repo / "CONTENTS.md").read_text(encoding="utf-8")
    matches = list(FAMILY_RE.finditer(contents))
    families = []
    for number, m in enumerate(matches):
        family_id, title = m.group(1), m.group(2).strip()
        section = contents[m.end():matches[number+1].start() if number+1 < len(matches) else len(contents)]
        papers = []
        for ptitle, rel in PDF_RE.findall(section):
            path = (repo / rel).resolve()
            if not path.is_relative_to(repo):
                raise ValueError("Unsafe upstream path: " + rel)
            parent_readme = (path.parent / "README.md")
            notice = parent_readme.read_text(encoding="utf-8") if parent_readme.is_file() else ""
            withdrawn = any(name in rel.lower() for name in WITHDRAWN) or "withdrawn" in notice.lower()
            papers.append({
                "title": ptitle,
                "path": rel,
                "sha256": file_sha256(path) if path.is_file() else None,
                "state": "WITHDRAWN" if withdrawn else "INDEXED_UNVERIFIED",
                "production_approved": False
            })
        families.append({
            "family_id": family_id,
            "title": title,
            "formalization_available": (repo / "lean" / "docs" / (family_id + ".md")).is_file(),
            "formalization_compiled_by_beesmash": False,
            "papers": papers,
            "production_approved": False
        })
    result = {
        "repository": "https://github.com/openai/math",
        "sha": sha,
        "indexed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "families": families,
        "notes": "Unverified source claims; independent validation and approval required."
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    count = sum(len(f["papers"]) for f in families)
    print(f"Indexed {len(families)} result families and {count} paper links at {sha}")
    if len(families) != 372 or count != 719:
        print("NOTE: Catalogue differs from Oct 8 snapshot; inspect source revisions and parsing.", file=sys.stderr)
    print(out)

if __name__ == "__main__":
    main()
