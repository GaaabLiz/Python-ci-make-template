# Build And Packaging

The template supports both standard Python packages and optional executable distribution.

## Standard Python package build

Build wheel and source distribution:

```bash
make build
```

This runs:

- clean steps
- project metadata generation
- `uv build`

Artifacts are written to `dist/`.

## PyInstaller executables

If `APPS_LIST` is configured, you can build executables as well.
Install the optional build tools with `make install-pyinstaller`. CI installs the separate `build` dependency group automatically for native release jobs.

The default keeps the console visible, which suits CLI programs. Set `PYINSTALLER_WINDOWED=1` only for GUI apps.

One-folder executables:

```bash
make build-exe
```

One-file executables:

```bash
make build-exe-onefile
```

Combined package and executable builds:

```bash
make build-app
make build-app-onefile
```

## Windows installer

When `ENABLE_WINDOWS_INSTALLER=1`, the template can generate an Inno Setup script and build an installer.

Relevant variables live in `project.mk`:

- `INNO_SETUP_FILE`
- `INNO_APP_NAME`
- `INNO_APP_PUBLISHER`
- `INNO_APP_ICON`
- `INNO_APP_EXE`
- `INNO_OUTPUT_DIR`
- `INNO_OUTPUT_BASE_FILENAME`

Typical flow on Windows:

```bash
make gen-inno-iss
make installer
make build-installer
```

## Release asset expectations

CI builds and smoke-tests the wheel and sdist once, then uploads them to the GitHub Release. `RELEASE_ARTIFACTS` is for optional application binaries and installers only.

- package-only projects should leave `CI_BUILD_LINUX`, `CI_BUILD_MACOS`, and `CI_BUILD_WINDOWS` at 0
- application projects should enable only the platform jobs they need
- projects with installers should usually add `Output/*.exe`
- projects with extra binaries should add the matching output paths explicitly

Enabled platform jobs print generated files and verify that every configured app output exists and is included in `RELEASE_ARTIFACTS`. For release uploads, a windowed macOS `.app` bundle is archived as a `.app.zip` file.

## Logo and icon assets

If your app needs icons for executables or installers, generate them from SVG once and commit the outputs you want to keep:

```bash
make gen-logo-icons SVG=resources/logo.svg
```
