import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest


def _git(repository: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=check,
        capture_output=True,
        text=True,
    )


def test_release_tag_stops_when_bump_commit_fails(
    make_project: Path,
    run_make: Callable[..., subprocess.CompletedProcess[str]],
    install_tool: Callable[[str, str], None],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    remote = tmp_path / "remote.git"
    _git(tmp_path, "init", "--bare", str(remote))
    _git(make_project, "init", "--initial-branch=main")
    _git(make_project, "config", "user.name", "Release Test")
    _git(make_project, "config", "user.email", "release-test@example.invalid")
    _git(make_project, "add", "Makefile", "project.mk", "pyproject.toml", ".mk")
    _git(make_project, "commit", "-m", "initial project")
    _git(make_project, "remote", "add", "origin", str(remote))
    _git(make_project, "push", "--set-upstream", "origin", "main")
    install_tool(
        "uv",
        'if [ "$1:$2" = "version:--short" ]; then printf "0.0.3\n"; fi\nexit 0',
    )
    monkeypatch.setenv("LC_ALL", "C")

    result = run_make("-j4", "release-patch-tag", f"INNO_SETUP_FILE={tmp_path / 'missing.iss'}")

    assert result.returncode != 0, result.stdout + result.stderr
    assert "nothing to commit" in result.stdout + result.stderr
    for repository in (make_project, remote):
        tag = _git(repository, "show-ref", "--verify", "--quiet", "refs/tags/v0.0.3", check=False)
        assert tag.returncode != 0, f"failed bump commit left a tag in {repository}"
