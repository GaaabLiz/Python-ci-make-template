# Build and Packaging

This template can build a Python package. If you want, it can also build standalone apps and a Windows installer.

## Python package

For most projects, this is the only build you need:

```sh
make build
```

It creates a wheel (a ready-to-install package) and a source archive in `dist/`. These files can be published to PyPI. The release workflow builds and checks them once, then reuses those files.

## Standalone apps with PyInstaller (optional)

Use this when people should be able to download and run your app without setting up Python themselves. First configure `APPS_LIST` and its app settings in `project.mk`; see [Configuration](configuration.md#python-package-or-standalone-app).

Install the app-building dependencies and build:

```sh
uv sync --group dev --group build
make gen-project-module
make build-exe-onefile
```

The one-file app is placed in `dist/`. `make build-exe` creates a folder containing the app and its supporting files instead. `make build-app-onefile` builds the Python package and app together.

The default keeps a terminal window open, which is right for command-line apps. Set `PYINSTALLER_WINDOWED=1` in `project.mk` only for an app with a graphical window. On macOS, a windowed app is saved as a `.app` bundle and packaged as a `.app.zip` file for download.

For release builds, also set the needed `CI_BUILD_LINUX`, `CI_BUILD_MACOS`, or `CI_BUILD_WINDOWS` value to `1`. The release jobs generate the project version module before building PyInstaller apps.

## Windows installer (optional)

An installer is a setup program that guides Windows users through installing and removing an app. This template uses [Inno Setup](https://jrsoftware.org/isinfo.php).

1. Configure a PyInstaller app in `project.mk` and set `INNO_APP_EXE` to its Windows executable. The sample uses `dist/myapp-windows.exe`.
2. Set `ENABLE_WINDOWS_INSTALLER=1` and `CI_BUILD_WINDOWS=1` in `project.mk`. Review the app name, publisher, and icon in the `INNO_*` settings.
3. Include the installer output in `RELEASE_ARTIFACTS`. With the default output directory, use `dist/* Output/*.exe`.
4. To build locally, install Inno Setup and run `make build-installer` in Git Bash or MSYS2 on Windows.

The build generates `installer.iss` from [the Inno Setup layout](../.mk/templates/installer.iss) and `project.mk`. Run `make gen-inno-iss` to generate the script on its own.

The `make install-inno` helper installs Inno Setup with Chocolatey. It therefore needs Chocolatey to be installed first; see the [official Chocolatey setup guide](https://docs.chocolatey.org/en-us/choco/setup/). You can also install Inno Setup directly and skip that helper, but make sure `ISCC.exe` is available on your `PATH` so Make can find it.

## Release files

`RELEASE_ARTIFACTS` defaults to `dist/*`. Add any installer or other native files outside `dist/` in `project.mk`. Quote paths with spaces, use `**` to match across directory levels, and prefix an exclusion with `!`. The CI package build handles the wheel and source archive separately.

Each enabled native build checks that its expected files exist and are included in `RELEASE_ARTIFACTS`. The job stages those selected files for upload, preserving their repository-relative paths. To run the local build and verification, use the matching operating system and run:

```sh
make ci-build-release-assets
make ci-verify-release-artifacts
```

## App icons (optional)

Start with an SVG logo, then generate the Windows `.ico` and macOS `.icns` files:

```sh
make gen-logo-icons SVG=resources/logo.svg
```

The generated ICO contains several sizes so Windows and the installer can choose a suitable one. Commit the icon files if you want to keep them in the project.
