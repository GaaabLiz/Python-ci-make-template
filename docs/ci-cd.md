# CI/CD Automation

The workflows in `.github/workflows/` are intentionally thin. Most of the logic lives in `Makefile` targets.

## `ci.yml`

The CI workflow performs:

1. checkout
2. `uv` installation
3. `make ci-setup`
4. `make ci-log-config`
5. `make ci-quality`
6. `make ci-test`
7. `make build`
8. `make ci-list-build-artifacts`

This means every CI run prints enough configuration and artifact state to debug common setup mistakes.

## `release.yml`

The release workflow performs:

- CI configuration export from `project.mk`
- changelog generation with git-cliff
- release creation on tags
- per-platform builds for Linux, macOS, and Windows
- artifact verification before upload

## Important CI variables

- `CI_PYTHON_VERSION`
- `TESTS_PATH`
- `CI_RUN_TESTS`
- `RELEASE_ARTIFACTS`
- `CI_BUILD_LINUX`
- `CI_BUILD_MACOS`
- `CI_BUILD_WINDOWS`
- `CI_ENABLE_RELEASE_DOCS`
- `CI_ENABLE_WINGET_PUBLISH`

## Publish workflows

The repository also includes optional workflows for:

- PyPI publication — see `publish-pypi.yml`
- Docker Hub publication — see [publishing-docker.md](publishing-docker.md)
- Chocolatey publication — see [publishing-chocolatey.md](publishing-chocolatey.md)
- Homebrew publication — see [publishing-homebrew.md](publishing-homebrew.md)
- WinGet publication — see [publishing-winget.md](publishing-winget.md)

Keep the related flags disabled until the required secrets and environments exist.

## Debugging signals now present in CI logs

- `make ci-log-config` prints the values driving the pipeline
- `make ci-list-build-artifacts` prints `dist/`, `Output/`, and artifact patterns
- `make ci-verify-release-artifacts` fails before upload if patterns match nothing

That makes it easier to understand whether a project is configured as a package-only distribution, an executable project, or an installer project.