from pat_version import get_version

def test_version_present():
   assert get_version() == "1.0.0"
