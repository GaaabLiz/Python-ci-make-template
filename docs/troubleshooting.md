# Troubleshooting

## `dist/*` does not match any files in release jobs

Check these first:

- run `make ci-build-release-assets`
- run `make ci-list-build-artifacts`
- confirm `RELEASE_ARTIFACTS` matches the generated files
- if your project is package-only, keep `APPS_LIST` empty and make sure `make build` succeeds
- if your project ships installers, add installer paths such as `Output/*.exe`

## CI does not run tests

Check:

- `CI_RUN_TESTS`
- `TESTS_PATH`
- whether your test dependencies are in the `dev` group used by `uv sync --all-groups`

Use `make ci-log-config` locally to verify the effective values.

## PyInstaller builds do nothing

If `APPS_LIST` is empty, executable targets log a skip by design.

Set:

- `APPS_LIST`
- `<app>_NAME`
- `<app>_MAIN`
- `<app>_ICO`
- `<app>_ICNS`

## Windows installer build fails

Check:

- `ENABLE_WINDOWS_INSTALLER=1`
- `INNO_APP_EXE` points to the actual built executable
- `INNO_APP_ICON` points to a real `.ico` file
- Inno Setup is available on the Windows runner or local machine

## Logo conversion errors

`make gen-logo-icons` expects an SVG input.

Example:

```bash
make gen-logo-icons SVG=resources/logo.svg
```

The command uses `.mk/scripts.py convert-logo`, `skia-python`, and Pillow from the `dev` dependency group.