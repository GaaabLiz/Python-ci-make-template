# CI/CD Automation

GitHub Actions orchestrates the pipeline; shared commands live in Makefile targets. The template expects uv, GNU Make, GitHub Actions, and a PEP 621 pyproject.toml. Hatchling is the example build backend.

## CI workflow

CI runs for pull requests, pushes to any branch, and manual CI runs. It is also a reusable workflow called by release.yml so releases pass the same checks as normal changes.

The workflow:

1. validates CI matrix settings from project.mk
2. runs Ruff checks on CI_PYTHON_VERSION
3. runs tests across CI_PYTHON_VERSIONS and CI_TEST_OS_MATRIX
4. builds the wheel and sdist once
5. installs each distribution in isolation and imports PYTHON_MAIN_PACKAGE
6. uploads those verified files as a workflow artifact

Tests are required. Set CI_TEST_COMMAND to adapt the test runner; CI cannot be made green by skipping the test step.

## Release workflow

Push a version tag such as v1.2.3 to start a release. The workflow calls ci.yml against that tag, verifies that the tag version matches pyproject.toml, creates a draft release, and builds optional application assets for the enabled platforms.

The wheel and sdist are reused from the CI gate and built only once. Platform asset builds default to disabled; enable CI_BUILD_LINUX, CI_BUILD_MACOS, or CI_BUILD_WINDOWS only when the project configures APPS_LIST or a Windows installer. After validation and builds succeed, optional publication runs in order: PyPI, GitHub Release, then the other configured registries. Homebrew waits for PyPI because its formula installs the package from PyPI.

The release workflow only runs on version tags. It does not provide a manual dispatch path that could publish an arbitrary branch.

## CI configuration

Edit these values in project.mk:

- CI_PYTHON_VERSION: primary interpreter for quality checks and packaging
- CI_PYTHON_VERSIONS: JSON array of Python versions supported by the project
- CI_TEST_OS_MATRIX: JSON array of runner labels; use an Ubuntu-only list for Linux-only projects
- CI_UV_VERSION: exact uv version installed by the workflows
- CI_QUALITY_TARGETS: Make targets used for lint and formatting; add type-check when using ty
- CI_TEST_COMMAND: test command, defaulting to uv run pytest $(TESTS_PATH)
- RELEASE_ARTIFACTS: patterns for optional platform assets attached to GitHub Releases
- CI_BUILD_LINUX, CI_BUILD_MACOS, CI_BUILD_WINDOWS: optional executable/installer jobs
- CI_ENABLE_RELEASE_DOCS: API docs generation during the release
- CI_ENABLE_PYPI_PUBLISH, CI_ENABLE_DOCKERHUB_PUBLISH, CI_ENABLE_CHOCOLATEY_PUBLISH, CI_ENABLE_HOMEBREW_PUBLISH, CI_ENABLE_WINGET_PUBLISH: optional publishers

Keep CI_PYTHON_VERSIONS within the requires-python range in pyproject.toml. The sample supports Python 3.11 and newer, tests versions 3.11 through 3.14, and uses 3.14 as the primary interpreter.

## Dependency groups

make ci-setup installs the project and the dev group only. The sample groups optional tools separately:

- dev: pytest, pytest-cov, and Ruff
- typing: ty
- docs: pdoc
- graphics: SVG and icon conversion libraries

The lockfile is checked with --locked; update and commit uv.lock after changing dependencies or groups. CI uses a pinned uv version and pinned GitHub Action commits.

## Publication workflows

The Docker Hub, Chocolatey, Homebrew, and WinGet workflow files are reusable jobs called by release.yml; they do not publish independently on tag events or manual dispatch. Configure the required GitHub environments and secrets before enabling their flags.

PyPI publication is a job in release.yml so PyPI can trust the top-level workflow. Configure Trusted Publishing with workflow filename release.yml and the environment name in CI_PYPI_ENVIRONMENT; see Publishing to PyPI. No long-lived PyPI API token is needed.

## Release diagnostics

- make ci-log-config prints the effective settings.
- make ci-list-build-artifacts lists generated files and upload patterns.
- make ci-verify-release-artifacts checks that a platform asset build produced files matching RELEASE_ARTIFACTS.
- make ci-smoke-build installs wheel and sdist in isolated environments and imports the configured package.
