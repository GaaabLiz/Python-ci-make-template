# Getting Started

This template is designed to give new Python projects a consistent local workflow and a CI/release setup with very little custom scripting.

## Requirements

- Git
- `make`
- `uv`
- Python compatible with the version declared in `pyproject.toml`

On Windows, use GNU Make from a Git Bash/MSYS2 or WSL environment; Makefile recipes use a POSIX-compatible shell.

Official `uv` installation instructions:

- https://docs.astral.sh/uv/

## Fast setup

1. Create a new repository from the template.
2. Rename the Python package directory if needed.
3. Update `pyproject.toml` metadata.
4. Update `project.mk` values for your project, including the Python and OS matrices.
5. Install dependencies and run the standard checks.

```bash
make install-dev
make ci-log-config
make qa
make build
```

## Minimum files to review first

- `pyproject.toml`
- `project.mk`
- `Makefile`
- `.github/workflows/ci.yml`
- `.github/workflows/release.yml`

## Recommended first checklist

- Set `PYTHON_MAIN_PACKAGE` in `project.mk`
- Set project name, version, description, and Python requirement in `pyproject.toml`
- Make sure `TESTS_PATH` points to your real test directories
- Set `CI_PYTHON_VERSION`, `CI_PYTHON_VERSIONS`, and `CI_TEST_OS_MATRIX` to match your support policy
- Set `CI_TEST_COMMAND` if you use a runner other than pytest
- Confirm `RELEASE_ARTIFACTS` matches the files you expect to publish

## When you need more than a package build

The template also supports optional features that you can enable later:

- PyInstaller executables through `APPS_LIST`
- Windows installers through Inno Setup variables
- Release publication through GitHub Releases
- Optional PyPI, Docker Hub, Chocolatey, Homebrew, and WinGet publication jobs
- Optional Qt resource compilation through `qt.mk`
