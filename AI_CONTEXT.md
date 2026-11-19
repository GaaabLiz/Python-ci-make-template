# Project Context for AI Assistants

## What this repository is

This repository is a reusable starter template for Python projects. It provides a shared, self-documenting `Makefile`, project-specific settings in `project.mk`, dependency and package management with `uv`, and GitHub Actions workflows for checks, builds, releases, and optional publishing. The `myapp/` package is a small example used to demonstrate the template; it is not the main product.

The sample command `python -m myapp` prints `2 + 3 = 5`. Its actual calculation is in `myapp/core.py`; `myapp/cli.py` provides the argument parser and version option.

## Sources of truth

- `.github/workflows/*.yml` defines the actual CI, release, and publisher jobs, triggers, dependencies, permissions, and conditions.
- `.github/workflows/template-context-cleanup.yml` removes `AGENTS.md`, `AI_CONTEXT.md`, `CLAUDE.md`, `GEMINI.md`, `.aider.conf.yml`, `.windsurfrules`, `.github/copilot-instructions.md`, `.clinerules/project-context.md`, and `.cursor/rules/project.mdc` from a newly generated repository, then removes itself in the cleanup commit.
- `project.mk` defines project-specific Make settings and the defaults read by CI. Command-line Make assignments can override its `?=` defaults.
- `Makefile` loads the reusable developer, build, release, and CI targets from `.mk/`. Workflows call these targets so local and hosted operations share behavior.
- `pyproject.toml` defines package identity, version, supported Python, dependencies, and build backend. `uv.lock` records resolved dependencies and must stay in sync.
- `docs/` describes intended use. Update relevant prose and `docs/ci-workflows.drawio` whenever GitHub Actions behavior changes, including CI, release, and template setup.
- `AI_CONTEXT.md` is the shared architecture and workflow overview; `AGENTS.md` contains required agent maintenance rules.

If generated files or narrative docs disagree with an executable configuration file, treat the executable configuration as authoritative and correct the stale copy.

## Current project configuration

- Package: `python-ci-make-template`, version `0.0.2`, Python `>=3.14,<3.15`.
- Build backend: Hatchling; package directory: `myapp`.
- Runtime dependencies are currently empty. Optional dependency groups are `dev` (pytest, pytest-cov, Ruff), `build` (PyInstaller), `typing` (`ty`), `docs` (`pdoc`), and `graphics` (image/PDF tooling).
- `project.mk` defaults CI to Python `3.14`, tests on Ubuntu, macOS, and Windows, and pins uv to `0.13.6`.
- Quality defaults to Ruff lint and format checks. Type checking is available and can be added to `CI_QUALITY_TARGETS`.
- Standalone application builds and all publishers are optional. Publisher settings default to disabled (`0`).
- `myapp/project.py` is generated from `pyproject.toml` by the Make workflow; do not use it as the source of package metadata.

## Main files and folders

| Path | Role |
| --- | --- |
| `project.mk` | Project identity, build paths, CI settings, release settings, app configuration, and publisher options. Start here for template customization. |
| `Makefile` | Default help, platform detection, and includes for the shared Make targets. |
| `.mk/*.mk` | Shared targets grouped by development, build, CI, release, and publishing. |
| `pyproject.toml` / `uv.lock` | Package metadata, dependency groups, build configuration, and locked dependency versions. |
| `.github/workflows/ci.yml` | Reusable and event-triggered quality, test, and package build workflow. |
| `.github/workflows/release.yml` | Version-tag release orchestration and optional publishers. |
| `.github/workflows/publish-*.yml` | Reusable jobs for Docker Hub, Chocolatey, Homebrew, and WinGet. |
| `.github/workflows/template-context-cleanup.yml` | One-time removal of template-specific AI context from repositories generated from this template. |
| `.mk/scripts.py` | CLI entry point for CI settings, project metadata, icons, installers, and publisher files. |
| `.mk/ci_config.py`, `.mk/project_metadata.py`, `.mk/winget.py` | Config validation and export, runtime metadata generation, and WinGet manifest generation. |
| `myapp/` | Example CLI package, calculation, and generated package metadata module. |
| `tests/` | Example tests; test path and command are configurable in `project.mk`. |
| `resources/` | Sample SVG logo and generated icon formats. |
| `qt.mk` | Optional Qt Make targets; not enabled by default. |
| `Dockerfile`, `installer.iss` | Example recipes used only when the matching app/publisher options are enabled. |
| `docs/` | Setup, configuration, development, packaging, release, publishing, troubleshooting guides, and the editable CI diagram. |

## CI workflow (`.github/workflows/ci.yml`)

The workflow starts on pushes to any branch, pull requests opened/synchronized/reopened, merge queue requests (`merge_group`), manual dispatch, and reusable workflow calls. `release.yml` calls it to validate release commits.

Job flow:

1. `workflow-lint` checks every workflow YAML file with actionlint. It runs independently.
2. `ci-config` runs `make ci-export-config`. Make passes the effective project settings to `.mk/ci_config.py` for validation and export of Python, OS matrix, uv, and release-notes settings.
3. `quality` and `tests` each depend on `ci-config` and then run in parallel. Quality runs on Ubuntu. Tests use `CI_PYTHON_VERSION` across `CI_TEST_OS_MATRIX`.
4. `build-package` waits for `ci-config`, `quality`, and all test jobs. On normal runs it calls `make build`. On a version tag it validates the tag version, generates per-release notes, and builds release distributions with those notes included in the PyPI package description. It smoke-tests the wheel and source archive, uploads `python-package-dist`, and on tag runs also uploads `release-notes`.

`CI_TEST_COMMAND`, `CI_TEST_OS_MATRIX`, `CI_PYTHON_VERSION`, `CI_QUALITY_TARGETS`, and `CI_UV_VERSION` are configured in `project.mk`. The CI gate is required for a release.

## Release workflow (`.github/workflows/release.yml`)

The workflow starts on a pushed `v[0-9]*` tag.

1. `ci-config` prints and validates release settings and confirms the tag commit belongs to `RELEASE_TARGET_BRANCH`.
2. `ci-gate` calls the reusable CI workflow. Its tagged package build verifies the tag matches `pyproject.toml` and creates the release notes and package artifacts.
3. After the gate, these jobs can run independently: `release-notes-and-draft`; optional `publish-release-docs`; configured Linux, macOS, and Windows app builds; and optional PyPI publication.
4. `release-ready` requires valid configuration, the successful CI gate, the draft release, and all enabled native builds. A native build disabled in `project.mk` is allowed to be skipped.
5. `publish-release` makes the GitHub Release public only after `release-ready` and PyPI publication when PyPI is enabled. It downloads the verified package distributions, release notes, and enabled native assets.
6. Docker Hub, Chocolatey, Homebrew, and WinGet publishing jobs run after the GitHub Release is published, when individually enabled. Homebrew also waits for successful PyPI publication. Failure of a downstream publisher does not roll back the GitHub Release.

API documentation publication is also optional: `CI_ENABLE_RELEASE_DOCS=1` generates `docs/api/` and opens or updates a PR. It does not gate publishing the release. Optional publisher jobs require their corresponding GitHub environments and credentials.

## Common commands

Run these from the repository root:

```sh
make                 # list available targets
make install-dev     # install test and quality tools
make qa              # configured quality targets and tests
make build           # build wheel and source distribution
make ci-log-config   # show active CI/release settings
make ci-validate-config
```

High-level build targets run cleanup, `gen-project-module`, and `build-uv` sequentially, including under parallel Make. `build-uv` remains a standalone package build. Release targets sequence the version bump, metadata generation, commit, branch rebase/push, and (for `release-*-tag`) tag creation/push; the tag points to the bump commit only after that commit is published on the release branch. A failed step stops the sequence.

For optional features, consult `docs/build-and-packaging.md`, `docs/publishing-*.md`, and `docs/qt-support.md` before changing their configuration.

## Documentation update contract

Any change that affects GitHub Actions behavior (CI, release, or template setup) must update `docs/ci-cd.md` and `docs/ci-workflows.drawio` in the same change. This includes changes to workflow triggers, jobs, dependencies, gates, conditions, artifacts, Python/OS matrices, CI Make targets, CI-related `project.mk` values, release packaging, publishers, or template initialization.

Before editing the diagram, inspect every workflow involved, including the reusable publisher workflows. The diagram must match the real trigger list, job names and dependencies, optional branches, release gates, uploaded/downloaded artifacts, and destinations. Keep its CI, release, optional-publisher, and template-setup pages consistent with the workflows. Update publisher-specific guides when their setup or behavior changes.

When validating a diagram change, make sure the `.drawio` XML remains parseable and inspect the changed page in diagrams.net when available. Report which validations were performed.
