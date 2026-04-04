# Python CI Make Template

[![CI](https://img.shields.io/github/actions/workflow/status/GaaabLiz/Python-ci-make-template/ci.yml?branch=main&label=CI)](https://github.com/GaaabLiz/Python-ci-make-template/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/actions/workflow/status/GaaabLiz/Python-ci-make-template/release.yml?label=Release)](https://github.com/GaaabLiz/Python-ci-make-template/actions/workflows/release.yml)
[![Publish PyPI](https://img.shields.io/github/actions/workflow/status/GaaabLiz/Python-ci-make-template/publish-pypi.yml?label=PyPI)](https://github.com/GaaabLiz/Python-ci-make-template/actions/workflows/publish-pypi.yml)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue)](#before-you-start)


A simple, reusable, **low-setup** starter template for Python projects.

This repository gives you a clean foundation with:

- a documented `Makefile` for local development
- a documented `project.mk` for project-specific settings
- optional `qt.mk` support for Qt / PySide6 projects
- GitHub Actions workflows that call **Make targets**, not random shell commands
- a release flow for changelog generation, GitHub Releases, build artifacts, and optional PyPI publishing

The goal is simple:

> **Start fast, keep configuration predictable, and avoid repeating setup work in every Python project.**

---

## Table of Contents

1. [What This Template Gives You](#what-this-template-gives-you)
2. [Who Should Use It](#who-should-use-it)
3. [The Main Idea](#the-main-idea)
4. [Before You Start](#before-you-start)
5. [Quick Start](#quick-start)
6. [Minimal Setup Checklist](#minimal-setup-checklist)
7. [Repository Files Explained](#repository-files-explained)
8. [How to Start a New Project From This Template](#how-to-start-a-new-project-from-this-template)
9. [How to Configure `pyproject.toml`](#how-to-configure-pyprojecttoml)
10. [How to Configure `project.mk`](#how-to-configure-projectmk)
11. [Makefile Documentation](#makefile-documentation)
12. [CI/CD Documentation](#cicd-documentation)
13. [GitHub Repository Setup for CI/CD](#github-repository-setup-for-cicd)
14. [Copy-Paste Starter Project Example](#copy-paste-starter-project-example)
15. [Optional Qt Support](#optional-qt-support)
16. [Common Project Scenarios](#common-project-scenarios)
17. [Recommended First Commands](#recommended-first-commands)
18. [Troubleshooting](#troubleshooting)
19. [Final Advice](#final-advice)

---

## What This Template Gives You

This template is designed to remove the boring setup phase from a new Python project.

Instead of rebuilding the same tooling every time, you start with:

### Local development tools

- dependency management with `uv`
- quality checks with `ruff`
- type checking with `mypy`
- testing with `pytest`
- coverage with `pytest-cov`
- documentation generation with `pdoc`

### Build and packaging tools

- source distribution and wheel builds with `uv build`
- optional executable generation with PyInstaller
- optional Windows installer generation with Inno Setup

### Release automation

- version bump helpers in `make`
- changelog generation with `git-cliff`
- GitHub Release creation
- optional release asset upload for Linux, macOS, and Windows
- optional PyPI publishing

### Better project structure

The template separates responsibilities clearly:

- `Makefile` = reusable commands for every project
- `project.mk` = settings that are specific to **your** project
- `.github/workflows/*.yml` = CI/CD orchestration that calls `make`

This separation makes the template easier to understand, easier to reuse, and easier to maintain.

---

## Who Should Use It

This template is a good fit if you want to start:

- a Python library
- a CLI tool
- a Python app with one or more entry points
- a desktop app distributed with PyInstaller
- a project that needs GitHub Actions with low maintenance

It is especially useful if you want:

- one standard way to run quality checks
- one standard way to build artifacts
- one standard way to configure CI
- one place for reusable commands
- one place for project-specific settings

---

## The Main Idea

This template follows one very important rule:

> **Workflows should call Make targets.**

Why?

Because this gives you one source of truth.

If a command changes, you update it in one place:

- local terminal usage stays consistent
- CI stays consistent
- documentation stays consistent

That means:

- developers run `make qa`
- CI also runs `make qa`
- developers run `make build`
- CI also runs `make build`
- release automation uses `make` targets too

This is the main reason the template stays simple over time.

---

## Before You Start

This template is meant to be easy to adopt, but there are still a few things you should have ready.

### Required tools

#### 1. Git

You need Git for versioning, tags, and release automation.

#### 2. `make`

The whole template is built around `make` commands.

- macOS: usually available or easy to install through Xcode Command Line Tools
- Linux: usually available through your package manager
- Windows: the GitHub Actions workflow installs it automatically with Chocolatey, but locally you must install it yourself if you want to use the same commands

#### 3. `uv`

This template uses `uv` to manage Python environments, dependencies, and builds.

Install it before using the template locally.

You can find the official installation guide here:

- https://docs.astral.sh/uv/

#### 4. Python

The template currently defaults to Python `3.13` in CI through `CI_PYTHON_VERSION ?= 3.13`.

You can change that in `project.mk` if your project needs another version.

### What you do **not** need to set up immediately

To start a basic project, you do **not** need to configure all of this on day one:

- PyInstaller
- Inno Setup
- Qt / PySide6
- PyPI publishing
- GitHub Release assets for all platforms

You can start with a simple Python package first, then enable extra features only when you need them.

### Fastest possible mental model

If you are new to this template, remember just this:

1. edit `pyproject.toml`
2. edit `project.mk`
3. run `make install-dev`
4. run `make qa`
5. run `make build`

That is enough to get real value from the template.

---

## Quick Start

If you want the shortest possible path, do this.

### 1. Create a new repository from this template

If you use GitHub, create a new repository from this repository as a template.

If you want the cleanest experience, prefer the GitHub template flow over manual copy-paste.

That way you keep:

- the repository structure
- the workflow files
- the Make-based automation model
- a clean starting point for your own Git history

If you copy files manually, copy at least:

- `Makefile`
- `project.mk`
- `qt.mk`
- `pyproject.toml`
- `.github/workflows/`

### 2. Create your Python package directory

Replace `myapp` with your real package name.

```bash
mkdir -p myapp
printf '"""My application package."""\n' > myapp/__init__.py
```

### 3. Update `pyproject.toml`

At minimum, change:

- project name
- description
- Python version if needed
- dependencies

### 4. Update `project.mk`

At minimum, set:

```makefile
PYTHON_MAIN_PACKAGE ?= myapp
```

If you do not need executables yet, you can leave the rest as-is.

### 5. Install dependencies

For everyday development:

```bash
make install-dev
```

For a fuller environment:

```bash
make install
```

### 6. Run quality checks

```bash
make qa
```

### 7. Build the package

```bash
make build
```

If these steps work, your new project is ready to use.

### 8. Optional but recommended: run the help target once

```bash
make help
```

This gives you a quick overview of everything already available in the template.

---

## Minimal Setup Checklist

Use this checklist when starting a new project.

### Required

- [ ] Create your package directory (for example `myapp/`)
- [ ] Add `__init__.py`
- [ ] Update `pyproject.toml`
- [ ] Set `PYTHON_MAIN_PACKAGE` in `project.mk`
- [ ] Run `make install-dev`
- [ ] Run `make qa`
- [ ] Run `make build`

### Optional

- [ ] Define `APPS_LIST` if you want executables
- [ ] Add PyInstaller entry-point settings in `project.mk`
- [ ] Enable Windows installer support if needed
- [ ] Enable Qt support if needed
- [ ] Enable PyPI publishing in CI if needed
- [ ] Configure GitHub secrets for releases

---

## Repository Files Explained

Here is the role of each important file.

### `Makefile`

This is the reusable automation layer.

It contains generic commands that many Python projects can share:

- install commands
- build commands
- quality commands
- docs commands
- clean commands
- version and release commands
- CI helper commands

In short:

> Put reusable project-agnostic logic in `Makefile`.

### `project.mk`

This file contains settings that are different from one project to another.

Examples:

- package name
- CI Python version
- release branch
- whether to build on Linux/macOS/Windows
- whether to publish to PyPI
- executable definitions
- installer settings

In short:

> Put project-specific configuration in `project.mk`.

### `qt.mk`

This is an optional module.

Use it only if your project needs Qt resource compilation.

### `pyproject.toml`

This is your Python package metadata and dependency definition.

The template already includes a default `dev` dependency group with common tools used by the `Makefile`.

### `.github/workflows/ci.yml`

The main quality and build workflow.

### `.github/workflows/release.yml`

The GitHub Release workflow for changelog, release notes, and release assets.

### `.github/workflows/publish-pypi.yml`

The optional PyPI publishing workflow.

### `CHANGELOG.md`

The changelog file generated and updated by the release flow.

### `cliff.toml`

The `git-cliff` configuration file that defines how commit history is transformed into changelog entries.

---

## How to Start a New Project From This Template

This section is intentionally detailed.

### Step 1: Choose your package name

Pick the Python import name of your package.

Examples:

- `myapp`
- `awesome_cli`
- `company_tools`

This is the name used for imports:

```python
import myapp
```

It usually matches the package directory name.

### Step 2: Create the package directory

Example:

```bash
mkdir -p myapp
printf '"""Main package."""\n' > myapp/__init__.py
```

If you are building a library, this may be enough to start.

If you are building a CLI, you may also want:

```bash
printf 'def main() -> None:\n    print("Hello from myapp")\n' > myapp/cli.py
```

### Step 3: Update `pyproject.toml`

Start with the project metadata.

Example:

```toml
[project]
name = "myapp"
version = "0.1.0"
description = "A short description of my project"
requires-python = ">=3.13"
dependencies = []
```

Then add real dependencies as your project grows.

### Step 4: Update `project.mk`

At minimum:

```makefile
PYTHON_MAIN_PACKAGE ?= myapp
```

That single line is one of the most important settings in the template.

### Step 5: Install the development environment

```bash
make install-dev
```

This installs the default development toolchain defined in `pyproject.toml`.

If you want extras too:

```bash
make install
```

### Step 6: Add your code

Add your source files under your package directory.

Examples:

- `myapp/__init__.py`
- `myapp/cli.py`
- `myapp/core.py`
- `tests/test_core.py`

### Step 7: Run validation commands

```bash
make lint
make format-check
make type-check
make test
make build
```

Or just use the all-in-one quality target:

```bash
make qa
```

### Step 8: Configure CI only if you need changes

The workflows already exist.

In many cases, you only need to edit values in `project.mk`.

For example:

- disable macOS builds
- disable Windows builds
- enable PyPI publishing
- change the release branch

You usually do **not** need to edit workflow YAML files.

That is one of the main benefits of this template.

---

## How to Configure `pyproject.toml`

The `Makefile` uses tools that live in your Python environment, so `pyproject.toml` matters.

### Already included in this template

The template already defines a `dev` dependency group with:

- `ruff`
- `mypy`
- `pytest`
- `pytest-cov`
- `pdoc`

That means these commands are already supported by the template:

```bash
make install-dev
make qa
make docs
```

### What you should edit

At minimum, update:

- `name`
- `version`
- `description`
- `requires-python`
- `dependencies`

### Example

```toml
[project]
name = "myapp"
version = "0.1.0"
description = "A reusable example project"
requires-python = ">=3.13"
dependencies = [
    "requests>=2.32",
]

[dependency-groups]
dev = [
    "mypy",
    "pdoc",
    "pytest",
    "pytest-cov",
    "ruff",
]
```

### About the generated `project.py`

The target `make gen-project-py` reads `pyproject.toml` and creates:

```text
$(PYTHON_MAIN_PACKAGE)/project.py
```

This file contains values like:

- name
- version
- description
- requires Python
- authors

This is useful if your app wants to read project metadata from Python code.

---

## How to Configure `project.mk`

This file is the heart of project-specific configuration.

The rule is simple:

- if it is generic and reusable, it belongs in `Makefile`
- if it changes from project to project, it belongs in `project.mk`

Below is a practical explanation of the main variables.

### 1. Project identity

```makefile
PYTHON_MAIN_PACKAGE ?= myapp
```

This must match your package directory.

### 2. Key file paths

```makefile
FILE_PROJECT_TOML ?= pyproject.toml
FILE_PROJECT_PY_GENERATED ?= $(PYTHON_MAIN_PACKAGE)/project.py
```

In most projects, you can keep these defaults.

### 3. Release and CI settings

```makefile
RELEASE_CHANGELOG_TARGET_BRANCH ?= main
CI_PYTHON_VERSION ?= 3.13
CI_BUILD_LINUX ?= 1
CI_BUILD_MACOS ?= 1
CI_BUILD_WINDOWS ?= 1
CI_ENABLE_PYPI_PUBLISH ?= 0
CI_PYPI_ENVIRONMENT ?= pypi
CI_CHANGELOG_FILE ?= CHANGELOG.md
CI_RELEASE_NOTES_FILE ?= RELEASE_NOTES.md
CI_GIT_CLIFF_CONFIG ?= cliff.toml
```

These values control behavior in GitHub Actions.

#### What they mean

- `RELEASE_CHANGELOG_TARGET_BRANCH`
  Branch where the generated changelog is pushed.

- `CI_PYTHON_VERSION`
  Python version installed by `make ci-setup`.

- `CI_BUILD_LINUX`, `CI_BUILD_MACOS`, `CI_BUILD_WINDOWS`
  Set to `1` to build release assets for that platform, or `0` to skip it.

- `CI_ENABLE_PYPI_PUBLISH`
  Set to `1` only when you want the PyPI workflow to publish.

- `CI_PYPI_ENVIRONMENT`
  GitHub Actions environment name used by the PyPI workflow.

- `CI_CHANGELOG_FILE`, `CI_RELEASE_NOTES_FILE`
  Output file names used during the release workflow.

- `CI_GIT_CLIFF_CONFIG`
  Path to the `git-cliff` configuration file used to generate changelog and release notes.

### 4. Release artifact settings

```makefile
RELEASE_ARTIFACTS ?= dist/*
```

This tells GitHub Release which files to upload.

Examples:

```makefile
RELEASE_ARTIFACTS ?= dist/*
```

```makefile
RELEASE_ARTIFACTS ?= dist/* Output/*.exe
```

```makefile
RELEASE_ARTIFACTS ?= $(foreach a,$(APPS_LIST),dist/$($(a)_NAME)-*) Output/*.exe
```

### 5. Windows installer settings

```makefile
ENABLE_WINDOWS_INSTALLER ?= 0
INNO_SETUP_FILE ?= installer.iss
INNO_SETUP_VERSION_VARIABLE ?= MyAppVersion
```

Use these only if your project creates a Windows installer.

If you do not need a Windows installer, keep:

```makefile
ENABLE_WINDOWS_INSTALLER ?= 0
```

### 6. Executable app settings

If you want PyInstaller executables, define `APPS_LIST` and one block per app.

Example:

```makefile
APPS_LIST := myapp

myapp_NAME := myapp
myapp_MAIN := myapp/cli.py
myapp_ICO := resources/icon.ico
myapp_ICNS := resources/icon.icns
```

If you have multiple executables:

```makefile
APPS_LIST := myapp admin-tool

myapp_NAME := myapp
myapp_MAIN := myapp/cli.py
myapp_ICO := resources/icon.ico
myapp_ICNS := resources/icon.icns

admin-tool_NAME := admin-tool
admin-tool_MAIN := myapp/admin_cli.py
admin-tool_ICO := resources/admin.ico
admin-tool_ICNS := resources/admin.icns
```

### 7. Optional modules

If you need Qt support, enable:

```makefile
include qt.mk
```

You can keep it commented if you do not need it.

---

## Makefile Documentation

This section explains the purpose of the main target groups.

You can always inspect the available commands with:

```bash
make
```

or:

```bash
make help
```

### Environment targets

These targets prepare your local environment.

| Target | Purpose |
|---|---|
| `make install` | Sync dependencies and extras with `uv` |
| `make install-all` | Install Python, sync all groups, build the project |
| `make install-dev` | Sync only the `dev` dependency group |
| `make install-pyinstaller` | Add PyInstaller to the dev group |
| `make install-inno` | Install Inno Setup on Windows |

### Generate targets

| Target | Purpose |
|---|---|
| `make gen-project-py` | Generate `$(PYTHON_MAIN_PACKAGE)/project.py` from `pyproject.toml` |

### Quality targets

| Target | Purpose |
|---|---|
| `make lint` | Run Ruff checks |
| `make lint-fix` | Auto-fix Ruff issues when possible |
| `make format` | Format Python files |
| `make format-check` | Check formatting without changing files |
| `make type-check` | Run mypy |
| `make test` | Run tests |
| `make test-cov` | Run tests with coverage |
| `make qa` | Run the main quality pipeline |

### Build targets

| Target | Purpose |
|---|---|
| `make build` | Clean, generate metadata module, and build the package |
| `make build-uv` | Run `uv build` only |
| `make build-exe` | Build directory-style executables with PyInstaller |
| `make build-exe-onefile` | Build one-file executables with PyInstaller |
| `make build-app` | Build package + executables |
| `make build-app-onefile` | Build package + one-file executables |
| `make installer` | Build Windows installer |
| `make build-installer` | Build app and installer |

### Docs targets

| Target | Purpose |
|---|---|
| `make docs` | Generate documentation in `docs/` |
| `make docs-open` | Generate docs and open them locally |

### Clean targets

| Target | Purpose |
|---|---|
| `make clean` | Remove build artifacts and generated files |
| `make clean-all` | Also remove generated docs |
| `make clean-build` | Remove build directories and `.spec` files |
| `make clean-cache` | Remove caches |
| `make clean-docs` | Remove generated docs |
| `make clean-generated` | Remove generated source files |

### Versioning and release targets

| Target | Purpose |
|---|---|
| `make bump-patch-beta` | Bump patch pre-release |
| `make bump-patch` | Bump patch version |
| `make bump-minor` | Bump minor version |
| `make bump-major` | Bump major version |
| `make release-patch` | Bump patch + generate metadata + commit + push |
| `make release-minor` | Bump minor + generate metadata + commit + push |
| `make release-major` | Bump major + generate metadata + commit + push |
| `make tag` | Create and push a `vX.Y.Z` tag |
| `make release-patch-tag` | Release patch and create tag |
| `make release-minor-tag` | Release minor and create tag |
| `make release-major-tag` | Release major and create tag |

### CI helper targets

These are mainly for GitHub Actions, but they are still regular Make targets.

| Target | Purpose |
|---|---|
| `make ci-setup` | Install CI Python version and sync all groups |
| `make ci-export-config` | Export project CI settings to GitHub Actions |
| `make ci-install-git-cliff` | Install `git-cliff` |
| `make ci-generate-changelog` | Build the changelog file |
| `make ci-generate-release-notes` | Build release notes file |
| `make ci-commit-changelog` | Commit and push the changelog |
| `make ci-build-release-assets` | Build release assets for the current runner OS |
| `make ci-publish-pypi` | Publish to PyPI |

---

## CI/CD Documentation

The repository includes three GitHub Actions workflows.

They are intentionally small because most real logic lives in `Makefile`.

That is a feature, not a limitation.

---

### 1. `ci.yml`

File:

```text
.github/workflows/ci.yml
```

### What it does

This is the main validation workflow.

It runs on:

- pushes to `main`
- pull requests
- manual runs

### What it executes

It performs:

1. checkout
2. `uv` setup
3. `make ci-setup`
4. `make qa`
5. `make build`

### Why it is useful

This ensures every change is checked with the same commands you use locally.

If it passes locally, it should behave similarly in CI.

---

### 2. `release.yml`

File:

```text
.github/workflows/release.yml
```

### When it runs

It runs on:

- tags matching `v*`
- manual runs

### What it does

This workflow handles the GitHub Release process.

It has multiple jobs:

#### `ci-config`

Reads project configuration from `project.mk` through:

```bash
make ci-export-config
```

This exports values such as:

- release branch
- enabled build platforms
- artifact patterns
- changelog file name
- release notes file name

#### `changelog-and-release`

This job:

1. sets up the CI environment
2. installs `git-cliff`
3. generates the full changelog
4. commits and pushes the changelog to the configured branch
5. generates release notes
6. creates the GitHub Release

#### `build-linux`, `build-macos`, `build-windows`

These jobs build release assets only if the corresponding flags are enabled in `project.mk`.

They call:

```bash
make ci-build-release-assets
```

That target decides what to do based on project configuration.

For example:

- if Windows installer support is enabled on Windows, it builds the installer path
- otherwise it builds one-file executables with PyInstaller

### Important related settings in `project.mk`

```makefile
CI_BUILD_LINUX ?= 1
CI_BUILD_MACOS ?= 1
CI_BUILD_WINDOWS ?= 1
ENABLE_WINDOWS_INSTALLER ?= 0
RELEASE_ARTIFACTS ?= dist/*
RELEASE_CHANGELOG_TARGET_BRANCH ?= main
```

---

### 3. `publish-pypi.yml`

File:

```text
.github/workflows/publish-pypi.yml
```

### When it runs

It runs on:

- tags matching `v*`
- manual runs

### Important behavior

This workflow is **gated** by a project setting.

It will only publish if:

```makefile
CI_ENABLE_PYPI_PUBLISH ?= 1
```

If this value is `0`, the workflow will not publish.

### What it does

1. reads CI config with `make ci-export-config`
2. installs `uv`
3. runs `make ci-setup`
4. builds package artifacts with `make build-uv`
5. publishes with `make ci-publish-pypi`

### Required GitHub secret

To publish to PyPI, you need:

```text
PYPI_API_TOKEN
```

The workflow passes it as:

```text
UV_PUBLISH_TOKEN
```

### Related `project.mk` settings

```makefile
CI_ENABLE_PYPI_PUBLISH ?= 0
CI_PYPI_ENVIRONMENT ?= pypi
CI_GIT_CLIFF_CONFIG ?= cliff.toml
```

---

## GitHub Repository Setup for CI/CD

The workflows are designed to work with very little editing, but there are still a few repository-level settings you may want to configure.

### 1. Enable GitHub Actions

In most repositories this is already enabled, but if Actions are restricted in your organization, make sure workflows are allowed to run.

### 2. Decide which workflows you want to use immediately

You do **not** need to enable everything at once.

Suggested adoption order:

1. `ci.yml`
2. `release.yml`
3. `publish-pypi.yml`

This keeps your first setup simple.

### 3. Set repository secrets only when needed

#### For PyPI publishing

Create this repository secret:

```text
PYPI_API_TOKEN
```

Then enable PyPI publishing in `project.mk`:

```makefile
CI_ENABLE_PYPI_PUBLISH ?= 1
```

If you leave that variable at `0`, the publish workflow stays effectively disabled.

### 4. Optional: configure a GitHub Environment for PyPI

If you want approval rules or environment-level protection, create the environment named in:

```makefile
CI_PYPI_ENVIRONMENT ?= pypi
```

If you want another name, change it in `project.mk`.

### 5. Make sure release tags use the expected format

The release and PyPI workflows trigger on tags that match:

```text
v*
```

Examples:

- `v0.1.0`
- `v1.0.0`
- `v2.3.4`

The template is already aligned with this convention through:

```bash
make tag
make release-patch-tag
make release-minor-tag
make release-major-tag
```

### 6. Understand what the release workflow is allowed to do

The release workflow may:

- generate `CHANGELOG.md`
- commit that file
- push it to `RELEASE_CHANGELOG_TARGET_BRANCH`
- create a GitHub Release
- upload release assets

So if your repository has strict branch protection rules, review them carefully.

In particular, make sure the GitHub Actions bot can push changelog updates if you want that feature to work automatically.

### 7. Customize CI behavior without editing YAML files

This is one of the biggest advantages of the template.

You can change CI behavior directly in `project.mk`, for example:

```makefile
CI_BUILD_LINUX ?= 1
CI_BUILD_MACOS ?= 0
CI_BUILD_WINDOWS ?= 1
CI_ENABLE_PYPI_PUBLISH ?= 0
ENABLE_WINDOWS_INSTALLER ?= 0
```

In most cases, that is enough.

You usually do **not** need to edit the workflow YAML files at all.

---

## Copy-Paste Starter Project Example

If you want the fastest start possible, copy this minimal structure and then replace `myapp` with your package name.

### Suggested minimal tree

```text
my-new-project/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── release.yml
│       └── publish-pypi.yml
├── myapp/
│   ├── __init__.py
│   └── cli.py
├── tests/
│   └── test_smoke.py
├── CHANGELOG.md
├── cliff.toml
├── Makefile
├── project.mk
├── pyproject.toml
└── qt.mk
```

### Minimal `myapp/cli.py`

```python
def main() -> None:
    print("Hello from myapp")


if __name__ == "__main__":
    main()
```

### Minimal `tests/test_smoke.py`

```python
def test_smoke() -> None:
    assert True
```

### Minimal `project.mk` values to change first

```makefile
PYTHON_MAIN_PACKAGE ?= myapp

# Optional CI tuning
CI_BUILD_LINUX ?= 1
CI_BUILD_MACOS ?= 1
CI_BUILD_WINDOWS ?= 1
CI_ENABLE_PYPI_PUBLISH ?= 0
```

### Minimal `pyproject.toml` skeleton

```toml
[project]
name = "myapp"
version = "0.1.0"
description = "My new project"
requires-python = ">=3.13"
dependencies = []

[dependency-groups]
dev = [
    "mypy",
    "pdoc",
    "pytest",
    "pytest-cov",
    "ruff",
]
```

### First run commands

```bash
make install-dev
make qa
make build
```

If these pass, your starter project is correctly wired.

---

## Optional Qt Support

If your project uses Qt resources, the template already includes `qt.mk`.

You do not need to modify the main `Makefile`.

### Enable it

In `project.mk`, uncomment:

```makefile
include qt.mk
```

### Optional Qt variables

You can override:

```makefile
QT_COMMAND_GEN_RES ?= pyside6-rcc
QT_QRC_FILE ?= resources/resources.qrc
QT_RESOURCE_PY ?= $(PYTHON_MAIN_PACKAGE)/resource/resources_rc.py
```

### Generate the resource module

```bash
make gen-qt-res-py
```

### When to use it

Use this only if:

- your project uses PySide6 or PyQt
- you have `.qrc` resource files
- you want resource compilation as part of your standard tooling

If not, leave it disabled.

---

## Common Project Scenarios

This section helps you choose the simplest path.

### Scenario 1: Pure Python library

Use the template with minimal changes.

Recommended:

- set `PYTHON_MAIN_PACKAGE`
- keep `APPS_LIST` empty
- keep `ENABLE_WINDOWS_INSTALLER = 0`
- keep `CI_ENABLE_PYPI_PUBLISH = 0` until you are ready

Typical commands:

```bash
make install-dev
make qa
make build
```

### Scenario 2: CLI application

Define one executable in `project.mk`.

Example:

```makefile
APPS_LIST := myapp

myapp_NAME := myapp
myapp_MAIN := myapp/cli.py
myapp_ICO := resources/icon.ico
myapp_ICNS := resources/icon.icns
```

Then install PyInstaller:

```bash
make install-pyinstaller
```

Then build:

```bash
make build-exe-onefile
```

### Scenario 3: Desktop app with Windows installer

Set:

```makefile
ENABLE_WINDOWS_INSTALLER ?= 1
INNO_SETUP_FILE ?= installer.iss
INNO_SETUP_VERSION_VARIABLE ?= MyAppVersion
```

Also configure your executable app block and artifact patterns.

Example:

```makefile
RELEASE_ARTIFACTS ?= dist/* Output/*.exe
```

### Scenario 4: Package publishing to PyPI

Set:

```makefile
CI_ENABLE_PYPI_PUBLISH ?= 1
CI_PYPI_ENVIRONMENT ?= pypi
```

Then create the GitHub secret:

```text
PYPI_API_TOKEN
```

---

## Recommended First Commands

If you want a practical starting sequence, use this.

```bash
make install-dev
make format
make qa
make build
```

If you want to inspect the available targets:

```bash
make help
```

If you want to generate docs:

```bash
make docs
```

If you want to prepare a release:

```bash
make release-patch-tag
```

This creates and pushes a `vX.Y.Z` tag, which matches the release workflow trigger.

---

## Troubleshooting

### `make type-check` fails because my package does not exist yet

Make sure you created your package directory and set:

```makefile
PYTHON_MAIN_PACKAGE ?= myapp
```

### `make build-exe-onefile` does nothing useful

You probably did not define:

- `APPS_LIST`
- `<id>_NAME`
- `<id>_MAIN`
- `<id>_ICO`
- `<id>_ICNS`

### PyInstaller commands fail

Install it first:

```bash
make install-pyinstaller
```

### Windows installer build fails

Make sure all of these are true:

- you are on Windows
- `ENABLE_WINDOWS_INSTALLER ?= 1`
- `INNO_SETUP_FILE` points to a real `.iss` file
- Inno Setup is available

### PyPI workflow does not publish

Check all of these:

- `CI_ENABLE_PYPI_PUBLISH ?= 1`
- repository secret `PYPI_API_TOKEN` exists
- the workflow ran on a `v*` tag or manually

### I want to disable some release builds

Edit `project.mk`:

```makefile
CI_BUILD_LINUX ?= 1
CI_BUILD_MACOS ?= 0
CI_BUILD_WINDOWS ?= 1
```

---

## Final Advice

Use this template in the simplest possible way first.

Do not configure everything on day one.

A good path is:

1. set your package name
2. update `pyproject.toml`
3. run `make install-dev`
4. run `make qa`
5. run `make build`
6. only then add executables, installer logic, Qt support, or PyPI publishing

That keeps the learning curve low and makes the template feel light instead of heavy.

If you follow that approach, this template becomes a fast starting point rather than a complicated framework.

---

## One-Line Summary

**This template gives you a clean Python project starter where local development, builds, and CI/CD all speak the same language: `make`.**


