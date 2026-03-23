from pat_pipeline.pipeline import run_pipeline

def test_pipeline_returns_structured_result():
    result = run_pipeline("Hello Africa")
    assert result["status"] == "processed"
    assert result["tokens"] == ["hello", "africa"]
    assert result["policy"]["passed"] is True

def test_pipeline_with_profile():
    result = run_pipeline("Ẹ káàárọ̀ ilẹ̀ Africa", profile_code="yo")
    assert result["profile_code"] == "yo"
    assert result["dialect"]["label"] in ("yo", "unknown")
