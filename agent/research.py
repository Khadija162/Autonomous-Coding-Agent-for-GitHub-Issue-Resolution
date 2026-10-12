"""Read-only source exploration; bounded file sizes and deterministic evidence."""
from pathlib import Path
import re

EXTENSIONS = {".py", ".md", ".toml", ".yml", ".yaml"}
EXCLUDE = {".git", ".venv", "node_modules", "__pycache__", ".terraform"}

def search(root: str, issue: str, limit: int = 6):
    base = Path(root).resolve()
    if not base.is_dir():
        raise ValueError("Target repository not available")
    words = set(re.findall(r"[a-z_]{3,}", issue.lower()))
    found = []
    for item in base.rglob("*"):
        relative = item.relative_to(base)
        if any(p in EXCLUDE for p in relative.parts) or not item.is_file() or item.suffix not in EXTENSIONS:
            continue
        if item.stat().st_size > 75000:
            continue
        content = item.read_text(encoding="utf-8", errors="replace")[:12000]
        score = sum(content.lower().count(w) for w in words)
        if score:
            found.append({"file": relative.as_posix(), "score": score, "excerpt": content[:2000]})
    return sorted(found, key=lambda f: -f["score"])[:limit]
