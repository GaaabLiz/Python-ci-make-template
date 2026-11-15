Read the repository root `AGENTS.md` and `AI_CONTEXT.md` before making changes. Follow their architecture and maintenance rules.

Any change that affects GitHub Actions behavior (CI, release, or template setup) must update `docs/ci-cd.md` and `docs/ci-workflows.drawio` in the same change. Inspect all affected workflow files, including reusable publishers, and keep the diagram accurate for triggers, jobs, dependencies, conditions, gates, artifacts, and destinations.
