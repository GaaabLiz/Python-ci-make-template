import shutil
import subprocess
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("installer", "globs", "error"),
    [
        ("missing", 'dist/* "Custom Output/*.exe"', "was not built"),
        ("directory", 'dist/* "Custom Output/*.exe"', "was not built"),
        ("file", "dist/*", "is not included in RELEASE_ARTIFACTS"),
        ("file", 'dist/* "Custom Output/*.exe"', None),
    ],
)
def test_windows_release_requires_the_configured_installer(
    tmp_path: Path, installer: str, globs: str, error: str | None
) -> None:
    for filename in ("Makefile", "project.mk"):
        shutil.copy2(REPOSITORY_ROOT / filename, tmp_path / filename)
    shutil.copytree(
        REPOSITORY_ROOT / ".mk", tmp_path / ".mk", ignore=shutil.ignore_patterns("__pycache__")
    )
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "myapp-windows.exe").touch()
    installer_path = tmp_path / "Custom Output" / "setup.exe"
    installer_path.parent.mkdir()
    if installer == "file":
        installer_path.touch()
    elif installer == "directory":
        installer_path.mkdir()

    result = subprocess.run(
        [
            "make",
            "--no-print-directory",
            "ci-verify-release-artifacts",
            "OS_NAME=windows",
            "ENABLE_WINDOWS_INSTALLER=1",
            "APPS_LIST=myapp",
            "INNO_OUTPUT_DIR=Custom Output",
            "INNO_OUTPUT_BASE_FILENAME=setup",
            f"RELEASE_ARTIFACTS={globs}",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    output = result.stdout + result.stderr
    if error is None:
        assert result.returncode == 0, output
    else:
        assert result.returncode != 0, output
        assert f"Custom Output/setup.exe {error}" in output
