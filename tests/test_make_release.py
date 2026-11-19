import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def _git(repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )


class TestReleaseMakeTargets(unittest.TestCase):
    def test_release_tag_stops_when_bump_commit_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            self._assert_release_tag_stops_after_failed_commit(Path(temporary_directory))

    def _assert_release_tag_stops_after_failed_commit(self, tmp_path: Path) -> None:
        repository = tmp_path / "project"
        remote = tmp_path / "remote.git"
        fake_bin = tmp_path / "bin"
        repository.mkdir()
        fake_bin.mkdir()

        for filename in ("Makefile", "project.mk", "pyproject.toml"):
            shutil.copy2(REPOSITORY_ROOT / filename, repository / filename)
        shutil.copytree(
            REPOSITORY_ROOT / ".mk",
            repository / ".mk",
            ignore=shutil.ignore_patterns("__pycache__"),
        )

        _git(tmp_path, "init", "--bare", str(remote))
        _git(repository, "init", "--initial-branch=main")
        _git(repository, "config", "user.name", "Release Test")
        _git(repository, "config", "user.email", "release-test@example.invalid")
        _git(repository, "add", "Makefile", "project.mk", "pyproject.toml", ".mk")
        _git(repository, "commit", "-m", "initial project")
        _git(repository, "remote", "add", "origin", str(remote))
        _git(repository, "push", "--set-upstream", "origin", "main")

        uv = fake_bin / "uv"
        uv.write_text(
            "#!/bin/sh\n"
            'if [ "$1" = "version" ] && [ "$2" = "--short" ]; then\n'
            '    printf "0.0.3\\n"\n'
            "fi\n"
            "exit 0\n",
            encoding="utf-8",
        )
        uv.chmod(0o755)

        environment = os.environ.copy()
        environment["PATH"] = f"{fake_bin}{os.pathsep}{environment['PATH']}"
        environment["LC_ALL"] = "C"
        result = subprocess.run(
            [
                "make",
                "--no-print-directory",
                "release-patch-tag",
                f"INNO_SETUP_FILE={tmp_path / 'missing-installer.iss'}",
            ],
            cwd=repository,
            env=environment,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(
            result.returncode,
            0,
            "release-patch-tag unexpectedly succeeded after the bump commit failed:\n"
            f"{result.stdout}{result.stderr}",
        )
        self.assertIn("nothing to commit", result.stdout + result.stderr)
        tag = subprocess.run(
            ["git", "-C", str(repository), "show-ref", "--verify", "--quiet", "refs/tags/v0.0.3"],
            check=False,
            capture_output=True,
            text=True,
        )
        remote_tag = subprocess.run(
            [
                "git",
                "--git-dir",
                str(remote),
                "show-ref",
                "--verify",
                "--quiet",
                "refs/tags/v0.0.3",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(
            tag.returncode, 0, "a failed bump commit must not leave a local release tag"
        )
        self.assertNotEqual(
            remote_tag.returncode, 0, "a failed bump commit must not publish a release tag"
        )
