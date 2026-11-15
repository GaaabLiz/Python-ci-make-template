# CI and Releases

GitHub Actions runs the checks and release steps for you. The workflow files call the same Make targets that you can run on your own computer.

See the [editable CI and release diagrams](ci-workflows.drawio) for the complete job flow, including the parallel release branches and optional publishers.

## What happens on a change

The `ci.yml` workflow runs for pull requests, branch pushes, and manual CI runs. It:

1. Reads and checks the CI settings in `project.mk`.
2. Checks workflow files and Python code style.
3. Runs tests with the one Python version in `CI_PYTHON_VERSION` on each operating system listed in `project.mk`.
4. Builds a wheel and source archive, installs each in a clean environment, and checks that your package can be imported.

Tests are always required. If you use a test runner other than pytest, set `CI_TEST_COMMAND` in `project.mk`.

## What happens on a release

The `release.yml` workflow runs when you push a version tag such as `v1.2.3`. The version must match the one in `pyproject.toml`, and the tagged commit must already be part of the branch named by `RELEASE_TARGET_BRANCH`.

The workflow runs CI, creates `ReleaseNotes.md` from the changes since the previous tag, and builds any app files enabled in `project.mk`. The notes become the body and a downloadable file on the GitHub Release. The same notes are included in the PyPI package description for that version. They are not committed to the repository. Python packages and platform app files are built once and reused for their release uploads. A windowed macOS `.app` is zipped so that it can be downloaded as one file.

The release starts as a draft while checks and builds run. Optional publishers are disabled until you configure them. Homebrew waits for the PyPI job because its formula installs the Python package from PyPI.

## Settings to review

Set these values in `project.mk`:

- `CI_PYTHON_VERSION` and `CI_TEST_OS_MATRIX`: the one Python version and the operating systems to use
- `CI_TEST_COMMAND`: how to run your tests
- `CI_QUALITY_TARGETS`: which code-quality checks to run
- `CI_BUILD_LINUX`, `CI_BUILD_MACOS`, and `CI_BUILD_WINDOWS`: which app builds to run
- `RELEASE_ARTIFACTS`: which app files and installers to attach to the GitHub Release
- `RELEASE_TARGET_BRANCH`: the branch that release tags must belong to; optional API documentation PRs target this branch
- `CI_ENABLE_..._PUBLISH`: optional publication jobs; see each publisher's guide

Set `CI_PYTHON_VERSION` to the project's chosen Python major and minor version. CI uses that same version for tests, quality checks, and builds. Keep `requires-python` in `pyproject.toml` consistent with that choice; the example is restricted to Python 3.14.

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

Release notes are published with each release and are not written back to the source branch. API documentation is included in a separate generated-files pull request only when `CI_ENABLE_RELEASE_DOCS=1`; configure the repository's Actions pull-request permission or `RELEASE_AUTOMATION_TOKEN` for that optional feature.
