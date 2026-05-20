# Getting Started

This template is designed to give new Python projects a consistent local workflow and a CI/release setup with very little custom scripting.

## Requirements

- Git
- `make`
- `uv`
- Python compatible with the version declared in `pyproject.toml`

Official `uv` installation instructions:

- https://docs.astral.sh/uv/

## Fast setup

1. Create a new repository from the template.
2. Rename the Python package directory if needed.
3. Update `pyproject.toml` metadata.
4. Update `project.mk` values for your project.
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
- Decide whether CI should run tests with `CI_RUN_TESTS`
- Confirm `RELEASE_ARTIFACTS` matches the files you expect to publish

## When you need more than a package build

The template also supports optional features that you can enable later:

- PyInstaller executables through `APPS_LIST`
- Windows installers through Inno Setup variables
- Release publication through GitHub Releases
- Optional PyPI, Docker Hub, and Chocolatey publication workflows
- Optional Qt resource compilation through `qt.mk`