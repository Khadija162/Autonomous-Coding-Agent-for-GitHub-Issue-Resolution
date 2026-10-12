"""Read-only software engineering investigation API. No writes, test jobs, or PR publishing."""
import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent.research import search
from agent.llm import propose

app = FastAPI(title="GitHub Issue Resolution Agent", version="0.1.0")

class Issue(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(default="", max_length=6000)

@app.get("/health")
def health():
    return {"status": "ok", "llm_mode": os.getenv("LLM_MODE", "mock")}

@app.post("/api/issues/analyze")
def analyze(issue: Issue):
    try:
        evidence = search(os.getenv("TARGET_REPO", "sample_repo"), issue.title + " " + issue.description)
        ai = propose(issue.model_dump(), evidence)
        return {"stage": "review", "issue": issue.model_dump(), "evidence": evidence,
                "recommendation": ai, "code_modified": False, "pr_created": False}
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    except requests.RequestException as exc:
        raise HTTPException(502, "Open-weight model unavailable") from exc
