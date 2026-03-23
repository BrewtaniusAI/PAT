from pat_core.language_profiles import list_profiles, load_profile

def test_profiles_exist():
    profiles = list_profiles()
    assert "yo" in profiles
    assert "sw" in profiles
    assert "zu" in profiles

def test_load_profile():
    profile = load_profile("yo")
    assert profile["code"] == "yo"
