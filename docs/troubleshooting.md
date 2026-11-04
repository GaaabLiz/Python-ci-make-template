# Troubleshooting

## `make` or `uv` says "command not found"

Install the missing tool, close and reopen your terminal, then check again with `make --version` or `uv --version`. On Windows, run Make from Git Bash/MSYS2 or WSL rather than directly from PowerShell.

## Dependency installation fails

Check that `pyproject.toml` is valid and that `uv.lock` matches it. After changing dependencies, run:

```sh
uv lock
make install-dev
```

Commit the updated `uv.lock` file.

## Tests do not run

Check that `TESTS_PATH` in `project.mk` points to your tests. If you use another test tool, set `CI_TEST_COMMAND` to the command that runs it. Make sure the test tool is in the `dev` dependency group in `pyproject.toml`.

## CI says a setting is missing or invalid

Run `make ci-log-config` and `make ci-validate-config`. Check the reported values in `project.mk`. Python versions in `CI_PYTHON_VERSIONS` must be valid JSON and fall within the range in `pyproject.toml`.

## App files are missing from a release

Check that:

1. The matching `CI_BUILD_LINUX`, `CI_BUILD_MACOS`, or `CI_BUILD_WINDOWS` value is `1`.
2. `APPS_LIST` and its `<app>_NAME`, `<app>_MAIN`, `<app>_ICO`, and `<app>_ICNS` values are set if you build PyInstaller apps.
3. The matching Windows installer settings are set if you build an installer.
4. `RELEASE_ARTIFACTS` in `project.mk` matches the files the build creates.

Run `make ci-list-build-artifacts` on the matching operating system to see the files. A Python-only package does not need any `CI_BUILD_*` option enabled.

## PyInstaller uses an old version or fails to find `project.py`

The module path is set by `FILE_PROJECT_PY_GENERATED` in `project.mk`. `make build` and the release asset job generate the module before packaging. If building locally, run:

```sh
make gen-project-module
make build-exe-onefile
```

## Windows installer build fails

Confirm `ENABLE_WINDOWS_INSTALLER=1`, `INNO_APP_EXE` points to the built executable, and `INNO_APP_ICON` points to an existing `.ico` file. Inno Setup must be installed on the Windows machine. `make install-inno` installs it with Chocolatey; see [Getting Started](getting-started.md#optional-homebrew-and-chocolatey).

## Logo icon generation fails

The input must be an SVG file. Install the optional graphics dependencies, then try:

```sh
uv sync --group graphics
make gen-logo-icons SVG=resources/logo.svg
```

The generated icons are written beside the SVG file.

## Publisher job does not run

Publisher jobs are off by default. Follow the setup guide for that service, add its required secret to the GitHub environment, and then set the matching `CI_ENABLE_..._PUBLISH=1` value in `project.mk`. Check the failed or skipped job in GitHub Actions for details.
