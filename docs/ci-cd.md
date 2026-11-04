# CI and Releases

GitHub Actions runs the checks and release steps for you. The workflow files call the same Make targets that you can run on your own computer.

## What happens on a change

The `ci.yml` workflow runs for pull requests, branch pushes, and manual CI runs. It:

1. Reads and checks the CI settings in `project.mk`.
2. Checks workflow files and Python code style.
3. Runs tests for each Python version and operating system listed in `project.mk`.
4. Builds a wheel and source archive, installs each in a clean environment, and checks that your package can be imported.

Tests are always required. If you use a test runner other than pytest, set `CI_TEST_COMMAND` in `project.mk`.

## What happens on a release

The `release.yml` workflow runs when you push a version tag such as `v1.2.3`. The version must match the one in `pyproject.toml`, and the tagged commit must already be part of the branch named by `RELEASE_CHANGELOG_TARGET_BRANCH`.

The workflow runs CI, prepares changelog and release notes, and builds any app files enabled in `project.mk`. It then publishes the GitHub Release and runs the optional publishers you enabled. Python packages and platform app files are built once and reused for their release uploads. A windowed macOS `.app` is zipped so that it can be downloaded as one file.

The release starts as a draft while checks and builds run. Optional publishers are disabled until you configure them. Homebrew waits for the PyPI job because its formula installs the Python package from PyPI.

## Settings to review

Set these values in `project.mk`:

- `CI_PYTHON_VERSION`, `CI_PYTHON_VERSIONS`, and `CI_TEST_OS_MATRIX`: what Python versions and operating systems to use
- `CI_TEST_COMMAND`: how to run your tests
- `CI_QUALITY_TARGETS`: which code-quality checks to run
- `CI_BUILD_LINUX`, `CI_BUILD_MACOS`, and `CI_BUILD_WINDOWS`: which app builds to run
- `RELEASE_ARTIFACTS`: which app files and installers to attach to the GitHub Release
- `RELEASE_CHANGELOG_TARGET_BRANCH`: the branch used for the generated changelog pull request
- `CI_ENABLE_..._PUBLISH`: optional publication jobs; see each publisher's guide

Keep the Python test versions inside the range in `pyproject.toml`. The template example uses Python 3.11 through 3.14.

## Check settings before pushing

Run these commands locally:

```sh
make ci-log-config
make ci-validate-config
make qa
```

`ci-log-config` prints the active settings. `ci-validate-config` reports missing or inconsistent options. `qa` runs the configured checks and tests.

## Dependencies and generated changes

`make install-dev` installs the `dev` dependency group, which includes test and code-quality tools. Optional tools are kept in separate groups: `build` for PyInstaller, `typing` for `ty`, `docs` for `pdoc`, and `graphics` for app icons.

If you change dependencies, update `uv.lock` and commit it. The CI workflow uses the lock file so it installs the versions selected by the project.

When a release is made, the workflow opens or updates a pull request for generated changelog files. Set the optional `RELEASE_AUTOMATION_TOKEN` secret if that pull request should start the normal CI checks. API documentation is included only when `CI_ENABLE_RELEASE_DOCS=1`.
