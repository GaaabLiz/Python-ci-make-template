# Python CI Make Template

[![CI](https://img.shields.io/github/actions/workflow/status/GaaabLiz/Python-ci-make-template/ci.yml?branch=main&label=CI)](https://github.com/GaaabLiz/Python-ci-make-template/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/actions/workflow/status/GaaabLiz/Python-ci-make-template/release.yml?label=Release)](https://github.com/GaaabLiz/Python-ci-make-template/actions/workflows/release.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](docs/getting-started.md)

A starter template for Python projects. It uses `make` for common commands, `uv` for Python packages, and GitHub Actions for checks and releases.

## Start here

1. Create a repository from this template.
2. Set your package name, version, description, and dependencies in `pyproject.toml`.
3. Set your project-specific options in `project.mk`.
4. Install the tools and run the first checks by following [Getting Started](docs/getting-started.md).

You usually only need to edit `pyproject.toml` and `project.mk`:

- `pyproject.toml` describes your Python package and its dependencies.
- `project.mk` contains the settings for your project: package folder, tests, supported Python versions, release files, and optional publishers.
- `Makefile` contains the shared commands. Leave it as it is when configuring a project. Change it only when adding or fixing a command that should work the same way for all projects using this template.

## What this template does

- Uses the same `make` commands on your computer and in GitHub Actions.
- Checks code style, runs tests, and builds Python packages.
- Can optionally build standalone apps and Windows installers.
- Can optionally publish to PyPI, Docker Hub, Chocolatey, Homebrew, and WinGet.

Publishing is off by default. You do not need Homebrew or Chocolatey to use the template or publish a normal Python package. See the relevant guide only if you want that publishing option.

## First commands

After following the setup guide, run:

```sh
make ci-log-config
make qa
make build
```

`make` with no target shows the available commands.

## Guides

- [Getting Started](docs/getting-started.md): install tools and run the project for the first time
- [Configuration](docs/configuration.md): choose what to change in `project.mk`
- [Project Structure](docs/project-structure.md): understand the main files and folders
- [Development Workflow](docs/development.md): everyday commands
- [Build and Packaging](docs/build-and-packaging.md): Python packages, apps, icons, and Windows installers
- [CI/CD Automation](docs/ci-cd.md): automatic checks and releases
- [Release Automation](docs/release-automation.md): create and publish a version
- [Publishing to PyPI](docs/publishing-pypi.md)
- [Publishing to Docker Hub](docs/publishing-docker.md)
- [Publishing to Chocolatey](docs/publishing-chocolatey.md)
- [Publishing to Homebrew](docs/publishing-homebrew.md)
- [Publishing to WinGet](docs/publishing-winget.md)
- [Qt Support](docs/qt-support.md)
- [Troubleshooting](docs/troubleshooting.md)
