# Project Structure

The important idea is simple: project settings, shared commands, and Python package details live in different places.

## Files you will use

| File or folder | What it is for |
| --- | --- |
| `project.mk` | Settings for this project: package folder, tests, CI versions, release files, and optional publishers. Start here when configuring the template. |
| `Makefile` | Default help, platform detection, and includes for shared commands such as `make test`, `make qa`, and `make build`. |
| `.mk/*.mk` | Shared target implementations for development, builds, CI, releases, and publishing. |
| `pyproject.toml` | Python package name, version, dependencies, supported Python versions, and build settings. |
| `uv.lock` | Exact dependency versions used by `uv`. Commit this file and update it after changing dependencies. |
| `.github/workflows/` | GitHub Actions instructions for running checks, builds, and releases. These workflows read project settings and call Make targets. |
| `.mk/*.py` | Internal CLI and helpers for CI configuration, package metadata, app icons, and publisher files. |

## Example project files

- `myapp/` is the example Python package. Replace it with your package folder and update `PYTHON_MAIN_PACKAGE` in `project.mk`.
- `tests/` contains example tests. Set `TESTS_PATH` in `project.mk` if yours are somewhere else.
- `resources/` contains sample logo files. You can generate `.ico` and `.icns` app icons from an SVG logo.
- `Dockerfile` is the sample Docker image recipe; it is only used if you enable Docker Hub publishing.
- `.mk/templates/installer.iss` defines the Inno Setup layout. `make gen-inno-iss` combines it with the `INNO_*` settings to generate `installer.iss`.
- `cliff.toml` controls the per-release notes created from Git history. CI publishes these notes with GitHub and PyPI releases without committing them to the repository.

## GitHub workflows

- `ci.yml` checks code, runs tests, and builds the Python package.
- `release.yml` starts when you push a version tag. It reuses the CI checks and can build release files and call optional publishers.
- `publish-*.yml` files contain the steps for individual optional publishers.

For normal project setup, change values in `project.mk` and package details in `pyproject.toml`. Change a workflow only when you need to change the pipeline itself.
