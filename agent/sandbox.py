"""Separate, explicitly invoked fixed-command test runner. NEVER exposed through HTTP.
Use only on trusted local fixtures. Docker containers are not a hard isolation boundary.
"""
import subprocess
from pathlib import Path

def verify_fixture(root="sample_repo", timeout=90):
    path = Path(root).resolve()
    if not (path / "test_calculator.py").is_file():
        raise ValueError("Approved sample fixture not found")
    cmd = ["docker", "run", "--rm", "--network", "none", "--read-only",
           "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
           "--pids-limit", "64", "--memory", "512m", "--cpus", "1",
           "--user", "65534:65534", "--tmpfs", "/tmp:rw,nosuid,size=32m",
           "-v", f"{path}:/code:ro", "-w", "/code",
           "python:3.12-slim", "python", "-m", "unittest", "discover", "-v"]
    try:
        run = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return {"exit_code": run.returncode, "stdout": run.stdout[-4000:], "stderr": run.stderr[-2000:]}
    except subprocess.TimeoutExpired:
        return {"exit_code": 124, "stdout": "", "stderr": "Timed out"}
