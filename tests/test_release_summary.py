from pat_release_pack import generate_release_summary

def test_release_summary_runs():
    result = generate_release_summary(".")
    assert result["name"] == "PAT"
    assert "version" in result
    assert "publication_docs" in result
