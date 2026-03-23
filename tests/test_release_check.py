from pathlib import Path
from pat_release import check_release_readiness

def test_release_check_runs():
    result = check_release_readiness(Path("."))
    assert "ready" in result
    assert "present" in result
    assert "missing" in result
