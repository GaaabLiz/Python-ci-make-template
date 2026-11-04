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

1. Configure a PyInstaller app and the `INNO_*` values in `project.mk`.
2. Set `ENABLE_WINDOWS_INSTALLER=1` and `CI_BUILD_WINDOWS=1` in `project.mk`.
3. Add the installer path (usually `Output/*.exe`) to `RELEASE_ARTIFACTS`.
4. To build locally, install Inno Setup, then run `make build-installer` from Git Bash or MSYS2 on Windows. The target detects a real Windows shell; it does not work from WSL.

The `make install-inno` helper installs Inno Setup with Chocolatey. It therefore needs Chocolatey to be installed first; see the [official Chocolatey setup guide](https://docs.chocolatey.org/en-us/choco/setup/). You can also install Inno Setup directly and skip that helper, but make sure `ISCC.exe` is available on your `PATH` so Make can find it.

## Release files

`RELEASE_ARTIFACTS` in `project.mk` lists the app files and installers attached to a GitHub Release. It does not include the Python wheel and source archive; those are uploaded separately.

The release job checks that each enabled platform created the expected files and that the file patterns match `RELEASE_ARTIFACTS`. Use these commands to inspect the results:

```sh
make ci-build-release-assets
make ci-list-build-artifacts
```

Run the build on the matching operating system. The Windows installer can only be built on Windows, for example.

## App icons (optional)

Start with an SVG logo, then generate the Windows `.ico` and macOS `.icns` files:

```sh
make gen-logo-icons SVG=resources/logo.svg
```

The generated ICO contains several sizes so Windows and the installer can choose a suitable one. Commit the icon files if you want to keep them in the project.
