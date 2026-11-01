# Configuration

This is an opinionated template for GitHub Actions projects managed with uv and GNU Make. It uses PEP 621 project metadata and Hatchling in the example pyproject.toml. Projects using another backend can keep uv build if their backend is declared in pyproject.toml; projects not using uv or Make need a different setup command.

## pyproject.toml

Set the project name, version, description, supported Python range, runtime dependencies, and the build backend. Update the Hatchling package configuration for the project's package layout, including src-layout or multiple packages.

The sample dependency groups keep optional developer tools separate:

- dev: pytest, pytest-cov, and Ruff, installed by CI
- typing: ty, selected when type checking is enabled
- docs: pdoc, selected when generating API documentation
- graphics: SVG and icon conversion libraries, selected by logo generation

After changing dependencies or groups, update and commit uv.lock.

## project.mk

### Package and tests

- PYTHON_MAIN_PACKAGE: importable package name; used for metadata generation and package smoke tests
- FILE_PROJECT_TOML: normally pyproject.toml
- FILE_PROJECT_PY_GENERATED: optional generated module containing project metadata
- TESTS_PATH: pytest arguments used by the default test command
- CI_TEST_COMMAND: override the default pytest command for unittest, nox, tox, or project-specific test runners

CI tests always run. The former CI_RUN_TESTS skip toggle has been removed so a skipped test suite cannot report success.

### Python and quality matrix

- CI_PYTHON_VERSION: primary Python interpreter for quality checks and packaging
- CI_PYTHON_VERSIONS: JSON array of supported Python versions tested in the matrix
- CI_TEST_OS_MATRIX: JSON array of runner labels, such as ["ubuntu-latest"] for Linux-only projects
- CI_UV_VERSION: exact uv version used by GitHub Actions
- CI_QUALITY_TARGETS: Make targets run in CI; default is lint and format-check. Add type-check to opt into ty.

Keep these values aligned with requires-python in pyproject.toml. The repository example supports Python 3.11 and newer, and tests Python 3.11 through 3.14 by default. Update the minimum version, Ruff target, and matrix together when adapting the template.

### Release artifacts

The CI gate builds and smoke-tests wheel and sdist once. Those verified files are reused by the GitHub Release and optional PyPI publisher.

- RELEASE_ARTIFACTS: glob patterns for platform executables and installers
- CI_BUILD_LINUX, CI_BUILD_MACOS, CI_BUILD_WINDOWS: default to 0; set to 1 only when building application assets on that runner
- ENABLE_WINDOWS_INSTALLER: enable Inno Setup packaging on Windows

For package-only projects, leave all CI_BUILD_* values at 0. For application releases, configure APPS_LIST and its entry variables, set the required platform flags, and include produced files in RELEASE_ARTIFACTS.

### Executables

Set APPS_LIST only when producing PyInstaller executables. For each entry, define:

- <app>_NAME
- <app>_MAIN
- <app>_ICO
- <app>_ICNS

### Publication

- CI_ENABLE_PYPI_PUBLISH uses Trusted Publishing from the top-level release.yml workflow; no PyPI API token is stored in GitHub secrets
- CI_ENABLE_DOCKERHUB_PUBLISH — see publishing-docker.md
- CI_ENABLE_CHOCOLATEY_PUBLISH — see publishing-chocolatey.md
- CI_ENABLE_HOMEBREW_PUBLISH — requires PyPI publication and see publishing-homebrew.md
- CI_ENABLE_WINGET_PUBLISH — see publishing-winget.md

Publication jobs are called from release.yml after the CI gate and asset builds. Keep flags disabled until their GitHub environments and required secrets are configured.

## First setup

1. Configure project metadata and supported Python range in pyproject.toml.
2. Set CI_PYTHON_VERSION, CI_PYTHON_VERSIONS, CI_TEST_OS_MATRIX, and CI_TEST_COMMAND in project.mk.
3. Update the package layout settings and generated metadata path.
4. Choose package-only or platform asset release.
5. Run make ci-log-config and confirm the printed values.
