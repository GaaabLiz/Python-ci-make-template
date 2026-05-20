# Project Structure

The repository is split so reusable automation and project-specific settings stay separate.

## Main files

- `Makefile`: reusable targets for install, quality checks, build, docs, release, and CI helpers
- `project.mk`: values that each project is expected to customize
- `qt.mk`: optional Qt/PySide6 helper targets
- `pyproject.toml`: package metadata, dependencies, and build backend configuration
- `CHANGELOG.md`: generated or curated changelog file used by release automation
- `cliff.toml`: git-cliff configuration for changelog and release notes generation

## Source and tests

- `myapp/`: example Python package used by the template
- `tests/`: example test suite executed by `make test` and CI
- `resources/`: sample logo assets used by the icon generation helper

## Automation directories

- `.github/workflows/ci.yml`: install, quality checks, tests, and package build
- `.github/workflows/release.yml`: changelog, release creation, platform builds, and release asset upload
- `.github/workflows/publish-pypi.yml`: optional PyPI publishing
- `.github/workflows/publish-dockerhub.yml`: optional Docker Hub publishing
- `.github/workflows/publish-chocolatey.yml`: optional Chocolatey publishing
- `.mk/scripts.py`: internal helper entrypoint used by Make targets for generated files and logo conversion

## Design rule behind the layout

Keep logic in one place:

- workflow files orchestrate jobs
- Make targets contain the command logic
- `project.mk` contains the settings that vary from project to project

That keeps local commands and CI behavior aligned.