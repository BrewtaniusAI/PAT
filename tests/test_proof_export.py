import json
from pathlib import Path
from pat_audit.proof_export import export_proof_bundle

def test_proof_bundle_written(tmp_path: Path):
    target = tmp_path / "artifact.json"
    target.write_text('{"ok": true}', encoding="utf-8")
    out = export_proof_bundle(target)
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["kind"] == "pat_proof_bundle"
    assert "receipt" in data
