# Python CI Make Template

[![CI](https://img.shields.io/github/actions/workflow/status/GaaabLiz/Python-ci-make-template/ci.yml?branch=main&label=CI)](https://github.com/GaaabLiz/Python-ci-make-template/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/actions/workflow/status/GaaabLiz/Python-ci-make-template/release.yml?label=Release)](https://github.com/GaaabLiz/Python-ci-make-template/actions/workflows/release.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](docs/getting-started.md)

Reusable Python project template built around `make`, `uv`, and GitHub Actions.

This template gives you:

- a reusable `Makefile` for local development, build, release, and CI helpers
- a `project.mk` file where each project keeps its own settings
- GitHub Actions workflows that call `make` targets instead of ad-hoc shell commands
- optional packaging and publication flows for PyInstaller, Inno Setup, PyPI, Docker Hub, Chocolatey, Homebrew, and WinGet

## How to use it

1. Create a new repository from this template, or copy the core files into your project.
2. Update `pyproject.toml` with your package metadata and dependencies.
3. Update `project.mk` with your package name, supported Python/OS matrices, test command, and release asset settings.
4. Install development dependencies with `make install-dev`.
5. Run `make qa` and `make build` before pushing changes.
6. If you build executables or installers, configure `APPS_LIST`, installer variables, `CI_BUILD_*`, and `RELEASE_ARTIFACTS`.

## Minimal first run

```bash
make install-dev
make ci-log-config
make qa
make build
```

## Key files

- `Makefile`: reusable commands shared by projects that adopt the template
- `project.mk`: project-specific configuration and CI toggles
- `.github/workflows/`: CI, release, and publication workflows
- `.mk/scripts.py`: internal helper script used by the Make targets

## Documentation

Use the shorter guides below for the parts you need:

- [Getting Started](docs/getting-started.md)
- [Project Structure](docs/project-structure.md)
- [Configuration](docs/configuration.md)
- [Development Workflow](docs/development.md)
- [Build And Packaging](docs/build-and-packaging.md)
- [CI/CD Automation](docs/ci-cd.md)
- [Publishing to PyPI](docs/publishing-pypi.md)
- [Release Automation](docs/release-automation.md)
- [Qt Support](docs/qt-support.md)
- [Troubleshooting](docs/troubleshooting.md)

## Core idea

The template keeps one source of truth:

- local development uses `make`
- CI uses the same `make` targets
- release automation also uses `make`

The release workflow runs the reusable CI gate first and builds the Python distributions once. Optional PyPI, Docker Hub, Chocolatey, Homebrew, and WinGet jobs run only after that gate and the configured asset builds succeed.

That keeps project setup predictable and reduces duplication between shell scripts, workflow YAML, and developer instructions.
