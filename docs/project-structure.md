# Project Structure

The important idea is simple: project settings, shared commands, and Python package details live in different places.

## Files you will use

| File or folder | What it is for |
| --- | --- |
| `project.mk` | Settings for this project: package folder, tests, CI versions, release files, and optional publishers. Start here when configuring the template. |
| `Makefile` | Shared commands such as `make test`, `make qa`, and `make build`. Change it only to add or fix a command that should be common to all projects. |
| `pyproject.toml` | Python package name, version, dependencies, supported Python versions, and build settings. |
| `uv.lock` | Exact dependency versions used by `uv`. Commit this file and update it after changing dependencies. |
| `.github/workflows/` | GitHub Actions instructions for running checks, builds, and releases. These workflows read project settings and call Make targets. |
| `.mk/scripts.py` | Internal helper used by Make to generate files and app icons. You normally do not need to run or edit it directly. |

## Example project files

- `myapp/` is the example Python package. Replace it with your package folder and update `PYTHON_MAIN_PACKAGE` in `project.mk`.
- `tests/` contains example tests. Set `TESTS_PATH` in `project.mk` if yours are somewhere else.
- `resources/` contains sample logo files. You can generate `.ico` and `.icns` app icons from an SVG logo.
- `Dockerfile` is the sample Docker image recipe; it is only used if you enable Docker Hub publishing.
- `installer.iss` is the sample Inno Setup recipe for a Windows installer; it is only used if you enable that installer.
- `cliff.toml` controls the changelog and release notes created from Git history.

## GitHub workflows

- `ci.yml` checks code, runs tests, and builds the Python package.
- `release.yml` starts when you push a version tag. It reuses the CI checks and can build release files and call optional publishers.
- `publish-*.yml` files contain the steps for individual optional publishers.

For normal project setup, change values in `project.mk` and package details in `pyproject.toml`. Change a workflow only when you need to change the pipeline itself.
