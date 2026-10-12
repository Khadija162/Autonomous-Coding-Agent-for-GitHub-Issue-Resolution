"""Produce evaluation records for an open synthetic issue fixture."""
import json
from datetime import datetime, timezone
from pathlib import Path

def record(issue, evidence, proposal, output="artifacts/investigations.jsonl"):
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    item = {"timestamp": datetime.now(timezone.utc).isoformat(),
            "issue": issue[:300], "retrieved_files": [x["file"] for x in evidence],
            "proposal_mode": proposal["mode"], "approved": False}
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(item) + "\n")
    return item
