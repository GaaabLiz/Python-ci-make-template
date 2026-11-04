# Release Automation

The template includes Make targets for version bumps, tagging, changelog generation, and GitHub Release publication.

## Version bump targets

- `make bump-patch-beta`
- `make bump-patch`
- `make bump-minor`
- `make bump-major`

## Release targets

- `make release-patch-beta`
- `make release-patch`
- `make release-minor`
- `make release-major`
- `make tag`
- `make release-patch-beta-tag`
- `make release-patch-tag`
- `make release-minor-tag`
- `make release-major-tag`

## Changelog and release notes

The release workflow only runs on version tags. It calls the same reusable CI workflow used for branch builds, verifies that the tag matches the project version, and keeps the GitHub release as a draft until validation and builds complete.

It uses git-cliff for changelog and notes:

- `make ci-generate-changelog`
- `make ci-generate-release-notes`

Configuration comes from `cliff.toml` and the file paths declared in `project.mk`.
The workflow opens or updates a pull request against `RELEASE_CHANGELOG_TARGET_BRANCH`; it does not push generated files directly to a protected branch. The release tag must point to a commit already contained in the target branch. Set the optional `RELEASE_AUTOMATION_TOKEN` secret if pull requests should trigger CI checks; the token is used for both the automation branch push and the PR operation.

When `CI_ENABLE_RELEASE_DOCS=1`, pdoc output is stored under `docs/api/` and included in the same pull request. Existing authored guides under `docs/` are preserved.

## How release artifact building behaves

- The CI gate builds and smoke-tests the wheel and sdist once; release publication reuses those exact files.
- Native application asset builds are opt-in through `CI_BUILD_LINUX`, `CI_BUILD_MACOS`, and `CI_BUILD_WINDOWS`.
- If `APPS_LIST` is set, enabled platform jobs create one-file executables.
- Every configured app executable must exist and be included in `RELEASE_ARTIFACTS` on each enabled platform.
- If Windows installer support is enabled, Windows release builds generate the installer as well.

## Common release mistake

If an optional platform build reports that `RELEASE_ARTIFACTS` matches no files, the project is usually in one of these states:

- `APPS_LIST` or Windows installer settings were not configured
- the enabled platform build did not produce an asset
- `RELEASE_ARTIFACTS` does not match the real output paths

The workflow prints generated files and validates platform asset patterns before upload. Wheel and sdist are built by the CI gate and do not depend on `RELEASE_ARTIFACTS`.
