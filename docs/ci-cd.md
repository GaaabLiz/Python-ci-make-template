# CI and Releases

GitHub Actions runs the checks and release steps for you. The workflow files call the same Make targets that you can run on your own computer.

See the [editable CI, release, and template setup diagrams](ci-workflows.drawio) for the workflow triggers, jobs, dependencies, parallel release branches, and optional publishers.

## When someone creates a repository from this template

GitHub copies all files from the template's default branch. On the new repository's initial push to `main`, `template-context-cleanup.yml` removes `AGENTS.md`, `AI_CONTEXT.md`, `CLAUDE.md`, `GEMINI.md`, `.aider.conf.yml`, `.windsurfrules`, `.github/copilot-instructions.md`, `.clinerules/project-context.md`, `.cursor/rules/project.mdc`, and their README link. It then commits the cleanup and deletes its own workflow. GitHub has no dedicated Actions event for template instantiation, so the workflow listens to `push` on `main`; its job condition limits the cleanup to a newly created branch and skips this source repository and other templates. Regular pushes to `main` can show a skipped workflow run while the cleanup workflow remains in the source template. It needs Actions enabled and permission for `GITHUB_TOKEN` to write repository contents; repository rules that block that write can prevent the cleanup commit.

## What happens on a change

The `ci.yml` workflow runs for:

- Pushes to any branch
- Pull requests when opened, synchronized, or reopened
- Merge queue checks (`merge_group`)
- Manual runs (`workflow_dispatch`)
- Calls from another workflow (`workflow_call`); the release workflow uses this to validate a tagged commit

Its jobs run in this order:

1. `workflow-lint` checks every workflow file with actionlint. It runs independently.
2. `ci-config` runs `make ci-export-config`. Make resolves the settings from `project.mk` and passes them to the Python helper in `.mk/ci_config.py`. The target validates the settings before exporting job outputs, including the Python version, test OS matrix, uv version, and release-notes path.
3. `quality` and `tests` start after `ci-config` and run in parallel. Quality checks run on Ubuntu. Tests use the configured Python version on each OS in `CI_TEST_OS_MATRIX`.
4. `build-package` waits for `ci-config`, `quality`, and every test job to succeed. On ordinary runs `make build` serially cleans artifacts, generates the project metadata module, and calls `build-uv`; on a version tag it verifies the tag version, generates release notes, and builds release distributions with those notes in the PyPI description. It smoke-tests both distributions and uploads them as `python-package-dist`. Tag runs also upload a `release-notes` artifact. `build-uv` remains available as a standalone target.

Tests are always required. If you use a test runner other than pytest, set `CI_TEST_COMMAND` in `project.mk`.

## What happens on a release

The `release.yml` workflow runs when you push a version tag such as `v1.2.3`. Its `ci-config` job validates release settings and checks that the tagged commit is already part of the branch named by `RELEASE_TARGET_BRANCH`. The reusable CI gate also checks that the tag version matches the one in `pyproject.toml`.

The local `release-*-tag` Make targets run the version bump and metadata generation in order, commit and push the bump to the release branch, and only then tag that pushed commit. A failed bump, generation, commit, rebase, or branch push stops the sequence before tag creation.

After the reusable CI gate succeeds, `release-notes-and-draft` creates a draft GitHub Release while the optional API-docs PR, enabled native app builds, and PyPI publication run as independent branches. `release-ready` requires valid configuration, a successful CI gate, the draft release, and every enabled native build; disabled native builds are accepted as skipped. The final GitHub Release waits for `release-ready` and for PyPI when PyPI publishing is enabled. Optional Docker Hub, Chocolatey, Homebrew, and WinGet publishers run after the GitHub Release is published; Homebrew also requires PyPI publication to succeed.

The notes become the draft release body and a downloadable file on the GitHub Release. The same notes are included in the PyPI package description for that version. They are not committed to the repository. Python packages and platform app files are built once and reused for their release uploads. A windowed macOS `.app` is zipped so that it can be downloaded as one file.

All optional publishers are disabled until you configure them. Homebrew waits for the PyPI job because its formula installs the Python package from PyPI.

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

`ci-log-config` prints the active settings. It uses `uv` when the system `python3` is older than 3.11 or unavailable. `ci-validate-config` uses `python3` (3.11 or newer) to report missing or inconsistent options. `qa` runs the configured checks and tests.

## Dependencies and generated changes

`make install-dev` installs the `dev` dependency group, which includes test and code-quality tools. Optional tools are kept in separate groups: `build` for PyInstaller, `typing` for `ty`, `docs` for `pdoc`, and `graphics` for app icons.

If you change dependencies, update `uv.lock` and commit it. The CI workflow uses the lock file so it installs the versions selected by the project.

Release notes are published with each release and are not written back to the source branch. API documentation is included in a separate generated-files pull request only when `CI_ENABLE_RELEASE_DOCS=1`; configure the repository's Actions pull-request permission or `RELEASE_AUTOMATION_TOKEN` for that optional feature.
