# Development Workflow

The normal local workflow is Make-based.

## Environment setup

Install the core development dependencies used by CI (pytest and Ruff):

```bash
make install-dev
```

Install all dependency groups and build once:

```bash
make install-all
```

## Quality commands

- `make lint`: Ruff lint checks
- `make lint-fix`: Ruff lint with safe autofixes
- `make format`: Ruff formatter
- `make format-check`: formatting check without changes
- `make type-check`: static analysis through `ty`
- `make test`: run pytest using `TESTS_PATH`
- `make test-cov`: pytest plus terminal coverage report
- `make qa`: the configured CI quality targets plus tests; add `type-check` to `CI_QUALITY_TARGETS` to enable ty

## Useful CI-oriented local checks

- `make ci-log-config`: print the effective CI and release settings
- `make ci-quality`: run the same static quality checks used in CI
- `make ci-test`: run the required CI test command from `CI_TEST_COMMAND`
- `make ci-list-build-artifacts`: print the current artifact directories and patterns

## Generated metadata and logo assets

The template uses `.mk/scripts.py` as an internal helper entrypoint.

Generate the Python metadata module:

```bash
make gen-project-module
```

Generate PNG, JPG, ICO, and ICNS assets from an SVG logo:

```bash
make gen-logo-icons SVG=resources/logo.svg
```

Direct script usage is also available when needed:

```bash
uv run python .mk/scripts.py gen-project-module pyproject.toml myapp/project.py
uv run --group graphics python .mk/scripts.py convert-logo resources/logo.svg
```

## Documentation generation

Generate API documentation with pdoc:

```bash
make docs
```

Generated API pages go to `docs/api/`; authored guides in `docs/` are preserved by `make clean-all`.

Open generated docs locally:

```bash
make docs-open
```
