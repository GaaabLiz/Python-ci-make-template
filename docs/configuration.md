# Configuration

Most projects only need to edit `pyproject.toml` and `project.mk`.

## `pyproject.toml`

Set at least:

- project name
- project version
- description
- `requires-python`
- runtime dependencies
- development dependency groups if your project needs extra tools

The template uses `uv build` with Hatchling as the build backend by default.

### Public repository and automatic updates

Set `[project.urls].Repository` to the public GitHub repository URL. Optional automatic-update
settings live in `[tool.python-ci-make-template.auto-update]`:

- `enabled`: opt in to configured update checks
- `strategies`: installation strategy per platform or `default`
- `asset-patterns`: release asset glob per platform or `default`
- `installer-args`: optional arguments for the Windows installer strategy

Run `make gen-project-module` after editing these values. See
[Automatic Updates](automatic-updates.md) for complete wheel and installer examples.

## `project.mk`

### Core project identity

- `PYTHON_MAIN_PACKAGE`: importable package directory
- `FILE_PROJECT_TOML`: normally `pyproject.toml`
- `FILE_PROJECT_PY_GENERATED`: generated Python module with project metadata

### Test configuration

- `TESTS_PATH`: directory or pytest arguments used by `make test`, `make test-cov`, and CI
- `CI_RUN_TESTS`: `1` to run tests in CI, `0` to log a skip instead

### Release artifact configuration

- `RELEASE_ARTIFACTS`: glob list uploaded to GitHub Releases
- `CI_BUILD_LINUX`, `CI_BUILD_MACOS`, `CI_BUILD_WINDOWS`: enable per-platform release builds
- `ENABLE_WINDOWS_INSTALLER`: enable Inno Setup packaging on Windows

If your project is package-only, the default `dist/*` is usually enough.

If your project also publishes installers or extra binaries, add those paths explicitly. Example:

```makefile
RELEASE_ARTIFACTS ?= dist/* Output/*.exe
```

### Executable configuration

Set `APPS_LIST` only when you want PyInstaller executables.

For each entry in `APPS_LIST`, define:

- `<app>_NAME`
- `<app>_MAIN`
- `<app>_ICO`
- `<app>_ICNS`

### Release and publication toggles

- `CI_ENABLE_RELEASE_DOCS`
- `CI_ENABLE_PYPI_PUBLISH`
- `CI_ENABLE_DOCKERHUB_PUBLISH` — see [publishing-docker.md](publishing-docker.md)
- `CI_ENABLE_CHOCOLATEY_PUBLISH` — see [publishing-chocolatey.md](publishing-chocolatey.md)
- `CI_ENABLE_HOMEBREW_PUBLISH` — see [publishing-homebrew.md](publishing-homebrew.md)
- `CI_ENABLE_WINGET_PUBLISH` — see [publishing-winget.md](publishing-winget.md)

These stay disabled by default until the corresponding secrets and environments are configured.

## Recommended sequence

1. Configure package metadata in `pyproject.toml`
2. Set package name and test path in `project.mk`
3. Decide which artifact types your project will produce
4. Run `make ci-log-config` and confirm the printed values match expectations