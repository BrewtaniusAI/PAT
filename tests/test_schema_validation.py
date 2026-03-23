import json
from pathlib import Path
from pat_pipeline.pipeline import run_pipeline
from pat_validation.schema_check import validate_pipeline_output_file

def test_pipeline_output_validates_against_schema(tmp_path: Path):
    output = tmp_path / "output.json"
    output.write_text(json.dumps(run_pipeline("Hello Africa"), ensure_ascii=False), encoding="utf-8")
    result = validate_pipeline_output_file(output, "schemas/pipeline_output.schema.json")
    assert result["valid"] is True
