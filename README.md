# Autonomous Coding Agent for GitHub Issue Resolution

**Full-stack, open-source coding-agent research prototype** with read-only GitHub issue integration, source-code retrieval, tree-sitter Python parsing, an optional open-weight **Qwen2.5-Coder** model served by Ollama, FastAPI backend, Streamlit frontend, original CC0 issue fixtures, evaluation logging, Docker, CI and Azure Terraform.

> **Implementation status:** This is a **review-first issue investigation system**. It DOES NOT yet apply patches, automatically run untrusted GitHub repositories, create pull requests or autonomously resolve issues. No cloud deployment has occurred.

## Architecture

```text
Open synthetic issue / optional public GitHub REST issue fetch
          |
    Read-only local repository search -> contextual code snippets
          |
    Mock planner or local Ollama Qwen coding LLM
          |
    Proposed fix + regression test ideas -> FastAPI -> Streamlit human review

Standalone tools: tree-sitter Python syntax parser, approved local Docker unittest runner,
                 JSONL evaluation event writer, open-source issue fixtures.
Future: audited approvals -> constrained patch engine -> isolated CI -> draft PR.
```

## Windows PowerShell quick start

```powershell
git clone https://github.com/Khadija162/Autonomous-Coding-Agent-for-GitHub-Issue-Resolution.git
cd Autonomous-Coding-Agent-for-GitHub-Issue-Resolution
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Start backend and frontend in separate terminals:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

Or launch both in Docker Desktop:

```powershell
docker compose up --build
```

- Backend API docs: http://localhost:8000/docs
- Web interface: http://localhost:8501

The API has read-only /health and POST /api/issues/analyze operations. It cannot execute code or push changes.

## Open-weight LLM

By default `LLM_MODE=mock`. Install [Ollama](https://ollama.com/) and pull Qwen2.5-Coder for actual local inference:

```powershell
ollama pull qwen2.5-coder:7b
$env:LLM_MODE="ollama"
$env:OLLAMA_MODEL="qwen2.5-coder:7b"
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

This connects a host-side FastAPI process to host-side Ollama; Docker Compose uses mock mode until configured separately. Models require sufficient memory. LLM output is **advice only**.

## Data engineering and open-source fixtures

`data/public/issues.jsonl` and `sample_repo/` are original **CC0 1.0** evaluation fixtures. `agent/evaluation.py` emits JSONL traces to ignored `artifacts/` for future analytics. These fixtures are not the SWE-bench benchmark. See [source provenance](data/public/README.md).

## Azure cloud plan

The Terraform starter in `infra/terraform/` declares an Azure resource group and Storage Account only. A target enterprise design uses authenticated Azure Container Apps, PostgreSQL for state, Blob/ADLS artifacts, isolated disposable runners for untrusted code, Azure Monitor, Key Vault and optional separately hosted open-weight coding models. None of these cloud services have been deployed; applying Terraform can incur costs.

## Security and limits

No sandbox execution is exposed to the web API. The `agent/sandbox.py` fixed-command Docker helper is for **explicit invocation on trusted local sample code only**, not security isolation for hostile repositories. Do not mount host Docker sockets or production GitHub write tokens in untrusted containers. Auth, quotas, human approvals, tenant isolation and sandboxed CI are required before production.

**Validation:** Files are committed to GitHub; live CI tests, Docker startup and Ollama inference have not been independently verified. See [architecture](docs/architecture.md) for the roadmap.
