from pat_core.language_profiles import list_profiles, load_profile

# All 71 African language profiles that must be present
ALL_EXPECTED_PROFILES = [
    # West Africa
    "ha", "ig", "yo", "ak", "tw", "ee", "ff", "wo", "bm", "fon",
    "kr", "mnk", "snk", "dag", "mos", "dyu", "sus", "tem", "men",
    # East Africa
    "sw", "am", "om", "ti", "so", "lg", "rw", "rn", "ki", "luo",
    "kam", "guz", "mas",
    # Southern Africa
    "zu", "xh", "st", "tn", "ss", "ve", "ts", "nr", "nso", "af",
    "sn", "ny", "bem", "tum", "loz", "nd",
    # Central Africa
    "ln", "kg", "lu", "lua", "sg", "sw_cd",
    # North Africa
    "ar_mag", "kab", "tzm", "zgh", "shi",
    # Island
    "mg",
    # Nilo-Saharan
    "din", "nus",
    # Additional
    "gaa", "ber", "tmh", "son", "swa", "tig", "sid", "wal", "gez",
]


def test_profiles_exist():
    profiles = list_profiles()
    assert "yo" in profiles
    assert "sw" in profiles
    assert "zu" in profiles


def test_all_african_language_profiles_exist():
    profiles = list_profiles()
    missing = [code for code in ALL_EXPECTED_PROFILES if code not in profiles]
    assert missing == [], f"Missing language profiles: {missing}"


def test_load_profile():
    profile = load_profile("yo")
    assert profile["code"] == "yo"


def test_all_profiles_load_and_have_required_fields():
    for code in list_profiles():
        profile = load_profile(code)
        assert profile["code"] == code, f"Profile {code}: code field mismatch"
        assert "name" in profile, f"Profile {code}: missing 'name'"
        assert isinstance(profile["preserve_characters"], list), (
            f"Profile {code}: 'preserve_characters' must be a list"
        )
        assert isinstance(profile["keywords"], list), (
            f"Profile {code}: 'keywords' must be a list"
        )


def test_profile_count():
    profiles = list_profiles()
    assert len(profiles) >= 71, (
        f"Expected at least 71 language profiles, found {len(profiles)}"
    )
