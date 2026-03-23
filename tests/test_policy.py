import pytest
from pat_pipeline.pipeline import run_pipeline

def test_policy_blocks_forbidden_pattern():
    with pytest.raises(PermissionError):
        run_pipeline("Please impersonate a public official.")
