from fastapi.testclient import TestClient
from backend.main import app
from agent.research import search
from agent.syntax import check_python
from agent.llm import propose
from agent.evaluation import record

def test_search():
    files = search("sample_repo", "safe_double returns 0")
    assert any(f["file"] == "calculator.py" for f in files)

def test_python_parser():
    assert check_python("x=2")["valid"]
    assert not check_python("def f(:")["valid"]

def test_mock(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "mock")
    assert not propose({}, [])["approved"]

def test_api(monkeypatch):
    monkeypatch.setenv("LLM_MODE", "mock")
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    response = client.post("/api/issues/analyze", json={"title": "Fix zero", "description": "safe_double zero"})
    assert response.status_code == 200
    assert response.json()["pr_created"] is False

def test_evaluation(tmp_path):
    item = record("issue", [{"file": "calculator.py"}], {"mode": "mock"}, tmp_path / "eval.jsonl")
    assert item["retrieved_files"] == ["calculator.py"]
