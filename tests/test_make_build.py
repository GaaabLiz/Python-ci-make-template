import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class TestBuildMakeTargets(unittest.TestCase):
    def test_build_uv_is_standalone(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tmp_path = Path(temporary_directory)
            repository = tmp_path / "project"
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

            uv = fake_bin / "uv"
            uv.write_text('#!/bin/sh\n[ "$1" = build ]\n', encoding="utf-8")
            uv.chmod(0o755)

            environment = os.environ.copy()
            environment["PATH"] = f"{fake_bin}{os.pathsep}{environment['PATH']}"
            result = subprocess.run(
                ["make", "--no-print-directory", "build-uv"],
                cwd=repository,
                env=environment,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse((repository / ".metadata-generated").exists())

    def test_build_serializes_clean_generation_and_uv_build(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            tmp_path = Path(temporary_directory)
            repository = tmp_path / "project"
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

            dirty_artifact = repository / "dist" / "stale.whl"
            dirty_artifact.parent.mkdir()
            dirty_artifact.touch()

            uv = fake_bin / "uv"
            uv.write_text(
                "#!/bin/sh\n"
                'if [ "$1" = "run" ]; then\n'
                "    sleep 0.2\n"
                "    if [ -e dist/stale.whl ]; then\n"
                '        echo "generation started before clean completed" >&2\n'
                "        exit 21\n"
                "    fi\n"
                "    touch .metadata-generated\n"
                'elif [ "$1" = "build" ]; then\n'
                "    if [ ! -e .metadata-generated ]; then\n"
                '        echo "build started before metadata generation completed" >&2\n'
                "        exit 22\n"
                "    fi\n"
                "    mkdir -p dist\n"
                "    touch dist/package.whl\n"
                "fi\n"
                "exit 0\n",
                encoding="utf-8",
            )
            uv.chmod(0o755)

            environment = os.environ.copy()
            environment["PATH"] = f"{fake_bin}{os.pathsep}{environment['PATH']}"
            result = subprocess.run(
                ["make", "--no-print-directory", "-j4", "build"],
                cwd=repository,
                env=environment,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse(dirty_artifact.exists(), "clean must finish before the build starts")
            self.assertTrue((repository / ".metadata-generated").exists())
            self.assertTrue((repository / "dist" / "package.whl").exists())


if __name__ == "__main__":
    unittest.main()
