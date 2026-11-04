# Development Workflow

Run commands from the repository folder. All commands are Make targets, so they begin with `make`.

## Prepare your environment

After installing `uv` and Make, run this once (and again after changing dependencies):

```sh
make install-dev
```

This installs the project's development dependencies, including its test and code-check tools.

## Check and test your code

```sh
make lint          # find common code problems
make format-check  # check formatting without changing files
make test          # run tests
make qa             # run the configured code checks and tests
```

To fix supported lint issues automatically, run `make lint-fix`. To format files, run `make format`.

`make qa` uses the quality targets listed in `CI_QUALITY_TARGETS` in `project.mk`, then runs tests. Type checking is optional; add `type-check` to that list if you use the `ty` tool.

## Build the package

```sh
make build
```

The command writes a Python wheel and a source archive to `dist/`. It also creates a small Python file containing the name and version from `pyproject.toml`.

## Helpful CI commands

- `make ci-log-config`: print the settings that CI will use
- `make ci-quality`: run the same code checks used in CI
- `make ci-test`: run the test command set in `CI_TEST_COMMAND`
- `make ci-list-build-artifacts`: show files that could be included in a release

If something fails, check that `project.mk`, `pyproject.toml`, and `uv.lock` agree. See [Troubleshooting](troubleshooting.md) for common fixes.

## Generate optional files

Generate the Python metadata module by itself:

```sh
make gen-project-module
```

Generate app icons from an SVG logo:

```sh
uv sync --group graphics
make gen-logo-icons SVG=resources/logo.svg
```

Generate API documentation with `pdoc` (requires the `docs` dependency group):

```sh
uv sync --group docs
make docs
```

The generated API pages go in `docs/api/`. The authored guides in `docs/` remain in place when you run `make clean-all`.
