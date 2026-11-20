import subprocess
import textwrap
from collections.abc import Callable
from pathlib import Path

import pytest


def test_build_uv_is_standalone(
    make_project: Path,
    run_make: Callable[..., subprocess.CompletedProcess[str]],
    install_tool: Callable[[str, str], None],
) -> None:
    install_tool("uv", '[ "$1" = build ]')

    result = run_make("build-uv")

    assert result.returncode == 0, result.stdout + result.stderr
    assert not (make_project / ".metadata-generated").exists()


@pytest.mark.parametrize(
    ("target", "pyinstaller_mode"),
    [("build", None), ("build-app", "onedir"), ("build-app-onefile", "onefile")],
)
def test_build_serializes_clean_generation_and_packaging(
    make_project: Path,
    run_make: Callable[..., subprocess.CompletedProcess[str]],
    install_tool: Callable[[str, str], None],
    target: str,
    pyinstaller_mode: str | None,
) -> None:
    dirty_artifact = make_project / "dist" / "stale.whl"
    dirty_artifact.parent.mkdir()
    dirty_artifact.touch()
    fake_uv = """
        case "$1:$2" in
          run:python)
            sleep 0.2
            [ ! -e dist/stale.whl ] || exit 21
            touch .metadata-generated
            ;;
          build:)
            [ -f .metadata-generated ] || exit 22
            mkdir -p dist
            touch dist/package.whl
            ;;
          run:pyinstaller)
            [ -f dist/package.whl ] || exit 23
            case " $* " in
              *" --onefile "*) printf 'onefile' > .pyinstaller-mode ;;
              *) printf 'onedir' > .pyinstaller-mode ;;
            esac
            ;;
          *) exit 24 ;;
        esac
    """
    install_tool("uv", textwrap.dedent(fake_uv))

    result = run_make("-j4", target, "APPS_LIST=myapp", "myapp_MAIN=myapp/__main__.py")

    assert result.returncode == 0, result.stdout + result.stderr
    assert not dirty_artifact.exists(), "clean must finish before the build starts"
    assert (make_project / ".metadata-generated").exists()
    assert (make_project / "dist" / "package.whl").exists()
    mode_file = make_project / ".pyinstaller-mode"
    if pyinstaller_mode is None:
        assert not mode_file.exists()
    else:
        assert mode_file.read_text(encoding="utf-8") == pyinstaller_mode
