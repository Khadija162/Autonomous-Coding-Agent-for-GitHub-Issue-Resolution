"""Optional read-only GitHub issue ingestion from the public REST API."""
import os
import re
import requests

def fetch_issue(owner: str, repository: str, number: int):
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", owner) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", repository) or number < 1:
        raise ValueError("Invalid issue reference")
    headers = {"Accept": "application/vnd.github+json"}
    if os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    result = requests.get(f"https://api.github.com/repos/{owner}/{repository}/issues/{number}", headers=headers, timeout=20)
    result.raise_for_status()
    data = result.json()
    if "pull_request" in data:
        raise ValueError("Reference is a pull request, not an issue")
    return {"title": data["title"], "body": (data.get("body") or "")[:8000], "source_url": data["html_url"]}
