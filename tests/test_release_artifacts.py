import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest


@pytest.fixture
def release_tools(install_tool: Callable[[str, str], None]) -> None:
    install_tool("uv", 'shift 3\nexec "$MAKE_TEST_PYTHON" "$@"')
    install_tool("python3", 'exec "$MAKE_TEST_PYTHON" "$@"')


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
    make_project: Path,
    run_make: Callable[..., subprocess.CompletedProcess[str]],
    release_tools: None,
    installer: str,
    globs: str,
    error: str | None,
) -> None:
    dist = make_project / "dist"
    dist.mkdir()
    (dist / "myapp-windows.exe").touch()
    installer_path = make_project / "Custom Output" / "setup.exe"
    installer_path.parent.mkdir()
    if installer == "file":
        installer_path.touch()
    elif installer == "directory":
        installer_path.mkdir()

    result = run_make(
        "ci-verify-release-artifacts",
        "OS_NAME=windows",
        "ENABLE_WINDOWS_INSTALLER=1",
        "APPS_LIST=myapp",
        "INNO_OUTPUT_DIR=Custom Output",
        "INNO_OUTPUT_BASE_FILENAME=setup",
        f"RELEASE_ARTIFACTS={globs}",
    )

    output = result.stdout + result.stderr
    if error is None:
        assert result.returncode == 0, output
    else:
        assert result.returncode != 0, output
        assert f"Custom Output/setup.exe {error}" in output


@pytest.mark.parametrize(
    ("patterns", "accepted"),
    [
        ([], False),
        (['RELEASE_ARTIFACTS=dist/* "Custom [[]x] Output/**/*.exe"'], True),
        (['RELEASE_ARTIFACTS=dist/* "Custom [[]x] Output/*.exe"'], False),
        (['RELEASE_ARTIFACTS=dist/* "Custom [[]x] Output/**/*.exe" "!**/setup.exe"'], False),
    ],
)
def test_config_and_staging_select_the_same_files(
    make_project: Path,
    run_make: Callable[..., subprocess.CompletedProcess[str]],
    release_tools: None,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    patterns: list[str],
    accepted: bool,
) -> None:
    (make_project / "main.py").touch()
    (make_project / "demo.ico").touch()
    settings = [
        "CI_BUILD_WINDOWS=1",
        "OS_NAME=windows",
        "ENABLE_WINDOWS_INSTALLER=1",
        "APPS_LIST=demo",
        "demo_NAME=Demo App",
        "demo_MAIN=main.py",
        "demo_ICO=demo.ico",
        "INNO_APP_ICON=demo.ico",
        "INNO_APP_EXE=dist/Demo App-windows.exe",
        "INNO_OUTPUT_DIR=Custom [x] Output/nested",
        "INNO_OUTPUT_BASE_FILENAME=setup",
        *patterns,
    ]
    config = run_make("ci-validate-config", *settings)

    artifact_paths = ["dist/Demo App-windows.exe", "Custom [x] Output/nested/setup.exe"]
    for relative_path in artifact_paths:
        file = make_project / relative_path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(relative_path, encoding="utf-8")
    (make_project / "dist/.gitignore").touch()
    output = tmp_path / "github-output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    monkeypatch.setenv("RUNNER_TEMP", str(tmp_path))
    staged = run_make("ci-stage-release-artifacts", *settings)

    if accepted:
        assert config.returncode == 0, config.stdout + config.stderr
        assert staged.returncode == 0, staged.stdout + staged.stderr
        root = Path(output.read_text(encoding="utf-8").removeprefix("directory=").strip())
        files = sorted(
            path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()
        )
        assert files == sorted(artifact_paths)
        for relative_path in artifact_paths:
            assert (root / relative_path).read_text(encoding="utf-8") == relative_path
    else:
        assert config.returncode != 0, config.stdout + config.stderr
        assert "must include the configured Inno Setup installer" in config.stderr
        assert staged.returncode != 0, staged.stdout + staged.stderr
        assert "setup.exe is not included in RELEASE_ARTIFACTS" in staged.stderr
        assert not output.exists()
