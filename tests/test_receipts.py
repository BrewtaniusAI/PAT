import json
from pathlib import Path
from pat_audit.receipts import write_receipt

def test_receipt_written(tmp_path: Path):
    p = tmp_path / "output.json"
    p.write_text(json.dumps({"ok": True}), encoding="utf-8")
    receipt = write_receipt(p)
    assert receipt.exists()
    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert "sha256" in data
