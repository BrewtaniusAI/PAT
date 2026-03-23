import json
from pathlib import Path

def test_provenance_file_exists():
    path = Path("provenance.json")
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["version"] == "0.8.0"
