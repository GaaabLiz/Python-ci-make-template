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

GitHub Release uploads use `RELEASE_ARTIFACTS`.

- package-only projects should usually keep `RELEASE_ARTIFACTS=dist/*`
- projects with installers should usually add `Output/*.exe`
- projects with extra binaries should add the matching output paths explicitly

The release workflow now prints generated files and fails early if `RELEASE_ARTIFACTS` matches nothing.

## Logo and icon assets

If your app needs icons for executables or installers, generate them from SVG once and commit the outputs you want to keep:

```bash
make gen-logo-icons SVG=resources/logo.svg
```