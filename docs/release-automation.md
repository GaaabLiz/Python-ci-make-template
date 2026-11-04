# Release Automation

A release is a published version of your project. This template starts a release when you push a version tag, for example `v1.2.3`.

## Before your first release

1. Set the version in `pyproject.toml`.
2. Set the release options in `project.mk`.
3. Run `make qa` and `make build` locally.
4. Push your changes to the branch named by `RELEASE_CHANGELOG_TARGET_BRANCH` (usually `main`).
5. Follow the setup guide for each publisher you want to enable. All publishers start disabled.

The release tag must point to a commit already included in the target branch. The workflow also checks that the tag version matches `pyproject.toml`.

## Create and push a version tag

The release Make targets update the version in `pyproject.toml`, update the installer version if configured, commit and push the version change, then create and push a Git tag. They send changes to GitHub automatically.

Before running one, make sure your work is committed, your working tree is clean, and you are on the release branch (usually `main`) with the latest changes. For a patch release, run:

```sh
make release-patch-tag
```

This makes a patch release, for example changing `1.2.3` to `1.2.4`, and starts the release workflow by pushing the new tag. Other options are `make release-minor-tag`, `make release-major-tag`, and `make release-patch-beta-tag`. To see all available commands, run `make`.

If you prefer to create a release manually, update the version in `pyproject.toml`, commit and push that change to the release branch, then create and push a matching `v`-prefixed Git tag. The tag must point to a commit already on the release branch.

## What GitHub does

GitHub Actions runs CI, creates a draft release, builds the configured app files, and prepares changelog and release notes. When all required jobs pass, it publishes the GitHub Release and runs any enabled publishers.

The wheel and source archive are built and checked once, then reused. WinGet uses the same Windows installer artifact that is attached to the GitHub Release when it calculates the installer hash. macOS graphical apps are zipped before upload.

The workflow opens or updates a pull request with generated changelog files instead of writing them directly to your protected branch. The tag must already be on the target branch. Set `RELEASE_AUTOMATION_TOKEN` in GitHub only if the generated-files pull request should start normal CI checks.

## Changelog and API documentation

`cliff.toml` controls generated changelog and release notes. The relevant output paths are set in `project.mk`.

API documentation is optional. Set `CI_ENABLE_RELEASE_DOCS=1` in `project.mk` to generate it during a release. The generated pages go in `docs/api/`; the guides you wrote in `docs/` are kept.

## If a release build fails

Check the failed job in the repository's GitHub Actions page. For app build failures, confirm that the matching `CI_BUILD_*` option is `1`, `APPS_LIST` and its app settings are correct, and `RELEASE_ARTIFACTS` includes the generated files. Run `make ci-log-config` to see the settings the workflow receives.
