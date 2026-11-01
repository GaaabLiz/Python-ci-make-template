# Troubleshooting

## Platform release assets do not match `RELEASE_ARTIFACTS`

Check these first:

- check that the matching `CI_BUILD_LINUX`, `CI_BUILD_MACOS`, or `CI_BUILD_WINDOWS` flag is enabled
- run `make ci-build-release-assets` on the matching platform
- run `make ci-list-build-artifacts`
- confirm `RELEASE_ARTIFACTS` matches the generated files
- if your project is package-only, leave all `CI_BUILD_*` values at 0; CI builds and publishes the Python distributions separately
- if your project ships installers, add installer paths such as `Output/*.exe`

## CI does not run tests

Check:

- `CI_TEST_COMMAND` and its arguments
- whether test dependencies are declared in the `dev` group
- whether `CI_PYTHON_VERSIONS` and `CI_TEST_OS_MATRIX` contain valid JSON arrays

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

The command uses `.mk/scripts.py convert-logo`, `skia-python`, and Pillow from the optional `graphics` dependency group.
