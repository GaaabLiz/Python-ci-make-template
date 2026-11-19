# Python CI Make Template

[![CI](https://img.shields.io/github/actions/workflow/status/GaaabLiz/Python-ci-make-template/ci.yml?branch=main&label=CI)](https://github.com/GaaabLiz/Python-ci-make-template/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/actions/workflow/status/GaaabLiz/Python-ci-make-template/release.yml?label=Release)](https://github.com/GaaabLiz/Python-ci-make-template/actions/workflows/release.yml)
[![Python](https://img.shields.io/badge/python-3.14-blue)](docs/getting-started.md)

A starter template for Python projects. It uses `make` for common commands, `uv` for Python packages, and GitHub Actions for checks and releases.

## Optional release documentation PRs

Release notes are published with the GitHub and PyPI releases; they are not committed back to the repository. If you set `CI_ENABLE_RELEASE_DOCS=1`, the workflow opens a pull request for generated API documentation. GitHub's repository settings must allow `GITHUB_TOKEN` to create pull requests; the `pull-requests: write` permission in the workflow file alone is not enough. If that setting is unavailable under your organization policy, configure a `RELEASE_AUTOMATION_TOKEN` repository secret with permission to write repository contents and create pull requests.

## Start here

1. Create a repository from this template. A one-time workflow removes the template-specific AI-agent context files and commits that cleanup.
2. Set your package name, version, description, and dependencies in `pyproject.toml`.
3. Set your project-specific options in `project.mk`.
4. Install the tools and run the first checks by following [Getting Started](docs/getting-started.md).

You usually only need to edit `pyproject.toml` and `project.mk`:

- `pyproject.toml` describes your Python package and its dependencies.
- `project.mk` contains the settings for your project: package folder, tests, supported Python versions, release files, and optional publishers.
- `Makefile` lists the shared commands and loads their implementations from `.mk/`.

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

- [AI project context](AI_CONTEXT.md) and [AI working rules](AGENTS.md): architecture, CI flow, and maintenance requirements
- [Getting Started](docs/getting-started.md): install tools and run the project for the first time
- [Configuration](docs/configuration.md): choose what to change in `project.mk`
- [Project Structure](docs/project-structure.md): understand the main files and folders
- [Development Workflow](docs/development.md): everyday commands
- [CI, release, and template setup diagrams](docs/ci-workflows.drawio): editable overview of the workflow jobs and dependencies
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
