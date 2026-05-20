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

The release workflow uses git-cliff:

- `make ci-generate-changelog`
- `make ci-generate-release-notes`

Configuration comes from `cliff.toml` and the file paths declared in `project.mk`.

## How release asset building behaves

- If `APPS_LIST` is empty, release builds create a normal Python package so `dist/*` exists.
- If `APPS_LIST` is set, release builds create the package and one-file executables.
- If Windows installer support is enabled, Windows release builds generate the installer as well.

## Common release mistake

If GitHub Releases report that `dist/*` matches no files, the project is usually in one of these states:

- the build step did not produce a package
- `RELEASE_ARTIFACTS` does not match the real output paths
- installer or executable paths were never added to `RELEASE_ARTIFACTS`

The updated workflow now prints the generated files and validates the glob patterns before upload.