# Configuration

Start with two files:

- `pyproject.toml` describes the Python package: its name, version, dependencies, and the versions of Python it supports.
- `project.mk` sets the options for this particular project: which package folder to build, where tests are, which Python versions to check, and which optional release features to use.

`Makefile` contains commands shared by all projects using the template. Do not put project-specific settings there. Normally, you do not need to edit it. Add or change a rule there only when it is a reusable command, not a setting for one project.

## Basic settings

Open `project.mk` and check these values:

| Setting | What it means | Example |
| --- | --- | --- |
| `PYTHON_MAIN_PACKAGE` | Name of the Python package folder to import | `myapp` |
| `FILE_PROJECT_TOML` | Path to your package metadata file | `pyproject.toml` |
| `TESTS_PATH` | Folder containing your tests | `tests` |
| `CI_PYTHON_VERSION` | Python version used for code checks and builds | `3.14` |
| `CI_PYTHON_VERSIONS` | Python versions tested in GitHub Actions | `["3.11", "3.12", "3.13", "3.14"]` |
| `CI_TEST_OS_MATRIX` | Operating systems used for tests | `["ubuntu-latest"]` for Linux only |
| `CI_TEST_COMMAND` | Command used to run your tests | Default: `uv run pytest $(TESTS_PATH)` |
| `CI_DOCKER_ENTRYPOINT` | Command that starts the app in its Docker image | Default: `python -m $(PYTHON_MAIN_PACKAGE)` |

Keep the Python versions here inside the range declared by `requires-python` in `pyproject.toml`. If your project uses a different test tool, set `CI_TEST_COMMAND` to its command.

The example `pyproject.toml` uses the standard Python project format and Hatchling to build the package files. Most projects can keep this setup and change the package details and dependencies. If you choose another build tool, declare it in `pyproject.toml`.

## Python dependencies

Add dependencies to `pyproject.toml`, not to `Makefile`. This template keeps optional tools in separate groups:

- `dev`: test and code-quality tools, installed by `make install-dev` and CI
- `build`: PyInstaller, used only to build standalone apps
- `typing`: the optional `ty` type checker
- `docs`: the optional API documentation generator
- `graphics`: tools used to turn an SVG logo into app icons

After changing dependencies, run `uv lock` and commit the updated `uv.lock` file.

## Python package or standalone app?

For a normal Python library or command-line package, keep `APPS_LIST` empty and leave the `CI_BUILD_*` values at `0`. The template still builds a wheel and a source archive for every release.

To also build standalone apps with PyInstaller, set `APPS_LIST` and define the four values for each app. For example:

```makefile
APPS_LIST := myapp
myapp_NAME := myapp
myapp_MAIN := myapp/__main__.py
myapp_ICO := resources/logo.ico
myapp_ICNS := resources/logo.icns
```

Then set `CI_BUILD_LINUX`, `CI_BUILD_MACOS`, or `CI_BUILD_WINDOWS` to `1` for the platforms you need. Set `PYINSTALLER_WINDOWED=1` only for a graphical app. A command-line app should keep its terminal window.

For a Windows installer, also set `ENABLE_WINDOWS_INSTALLER=1` and review the `INNO_*` settings in `project.mk`. See [Build and Packaging](build-and-packaging.md).

`RELEASE_ARTIFACTS` lists the app files and installers to attach to the GitHub Release. It does not control the Python wheel and source archive; those are handled separately.

## Publishing to package services

All publishers are off by default. For each one, follow its guide first, then set the matching `CI_ENABLE_..._PUBLISH` value in `project.mk` to `1`:

- PyPI: `CI_ENABLE_PYPI_PUBLISH` — [guide](publishing-pypi.md)
- Docker Hub: `CI_ENABLE_DOCKERHUB_PUBLISH` — [guide](publishing-docker.md)
- Chocolatey: `CI_ENABLE_CHOCOLATEY_PUBLISH` — [guide](publishing-chocolatey.md)
- Homebrew: `CI_ENABLE_HOMEBREW_PUBLISH` — [guide](publishing-homebrew.md); it requires PyPI publication
- WinGet: `CI_ENABLE_WINGET_PUBLISH` — [guide](publishing-winget.md)

Before enabling a publisher, replace example names, URLs, and licenses with real project details. Add the required secret to the matching GitHub environment as described in that publisher's guide. The configuration check reports common missing values before a release.

A GitHub environment is a named place in repository settings for release settings and secrets. A secret is a private token or password used by a workflow; never put it in `project.mk` or commit it to Git.

## Where do I put a change?

- A name, URL, path, Python version, test command, or publisher setting for this project goes in `project.mk` (package metadata and dependencies go in `pyproject.toml`).
- A command that should work in every project using the template goes in `Makefile`.
- GitHub workflow files normally only need changes if you are changing how jobs run, not to set project values.

To see the effective settings, run:

```sh
make ci-log-config
```
