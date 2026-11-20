import os
import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def make_project(tmp_path: Path) -> Path:
    repository = tmp_path / "project"
    repository.mkdir()
    for filename in ("Makefile", "project.mk", "pyproject.toml"):
        shutil.copy2(REPOSITORY_ROOT / filename, repository / filename)
    shutil.copytree(
        REPOSITORY_ROOT / ".mk", repository / ".mk", ignore=shutil.ignore_patterns("__pycache__")
    )
    return repository


@pytest.fixture
def run_make(make_project: Path) -> Callable[..., subprocess.CompletedProcess[str]]:
    def run(*arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["make", "--no-print-directory", *arguments],
            cwd=make_project,
            capture_output=True,
            text=True,
        )

    return run


@pytest.fixture
def install_tool(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Callable[[str, str], None]:
    tools = tmp_path / "bin"
    tools.mkdir()
    monkeypatch.setenv("PATH", str(tools), prepend=os.pathsep)
    monkeypatch.setenv("MAKE_TEST_PYTHON", Path(sys.executable).as_posix())

    def install(name: str, script: str) -> None:
        executable = tools / name
        executable.write_text(f"#!/bin/sh\n{script}\n", encoding="utf-8", newline="\n")
        executable.chmod(0o755)

    return install
