# Instructions for AI coding agents

Before changing code or documentation, read [AI_CONTEXT.md](AI_CONTEXT.md) and inspect the current files involved. The workflows, `project.mk`, and `Makefile` are the source of truth for behavior; documentation must describe them accurately.

## Required maintenance rules

- Whenever a change affects GitHub Actions behavior (CI, release, or template setup), update `docs/ci-cd.md` and `docs/ci-workflows.drawio` in the same change. This includes workflow triggers or jobs, dependencies, conditions, artifacts, Make CI targets, relevant `project.mk` settings, package/build steps, and publisher behavior.
- Check all relevant files in `.github/workflows/`, not only `ci.yml`: release behavior is split between `ci.yml`, `release.yml`, and the reusable `publish-*.yml` workflows.
- Keep the draw.io diagram accurate for triggers, jobs, dependencies, optional branches, gates, artifacts, and publishing destinations. Update the diagram's existing pages instead of leaving conflicting or obsolete flow descriptions.
- Update the relevant setup, build, release, or publisher guide when its instructions or behavior change. Keep the README and AI context files accurate when the project purpose, architecture, or working rules change.
- Keep `pyproject.toml` as the source of package metadata and dependency requirements; update and commit `uv.lock` when dependencies change. Regenerate `myapp/project.py` with `python3 .mk/scripts.py gen-project-module pyproject.toml myapp/project.py` rather than editing generated metadata by hand.
- Put project-specific defaults in `project.mk`. Keep `Makefile` commands reusable across projects; change it only when a shared command or behavior needs to change.
- Preserve pinned GitHub Action commit SHAs and least-privilege workflow permissions when editing Actions workflows.
- Keep `.github/workflows/template-context-cleanup.yml` in the template source. It removes this template's AI-specific instruction files from generated repositories and deletes itself after its one-time cleanup commit.
- Report which checks or validations were actually performed; do not claim unrun checks passed.

## Quick reference

- Run `make` to list commands. Common commands: `make install-dev`, `make qa`, `make build`, `make ci-log-config`, and `make ci-validate-config`.
- The project is a reusable Python/Make/uv/GitHub Actions template. `myapp/` is only the sample package.
- See [AI_CONTEXT.md](AI_CONTEXT.md) for the architecture, current pipeline, file map, configuration, and known project details.
