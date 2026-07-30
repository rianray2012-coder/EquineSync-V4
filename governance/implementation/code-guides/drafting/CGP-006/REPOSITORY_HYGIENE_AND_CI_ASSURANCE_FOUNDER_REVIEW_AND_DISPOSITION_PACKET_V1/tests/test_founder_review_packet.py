import subprocess
from pathlib import Path


def test_founder_review_packet_validator_passes():
    package_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["python3", str(package_root / "validators" / "validate_founder_review_packet.py"), str(package_root)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
