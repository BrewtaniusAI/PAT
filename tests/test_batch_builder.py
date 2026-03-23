import json
from pathlib import Path
from pat_builder.batch import build_dataset_batch

def test_batch_builder(tmp_path: Path):
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    input_dir.mkdir()
    (input_dir / "a.json").write_text(json.dumps({"id": 1}), encoding="utf-8")
    (input_dir / "b.json").write_text(json.dumps({"id": 2}), encoding="utf-8")

    result = build_dataset_batch(input_dir, output_dir)
    assert result["count_built"] == 2
    assert (output_dir / "a.json").exists()
    assert (output_dir / "b.json").exists()
