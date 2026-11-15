@AGENTS.md
@AI_CONTEXT.md

Follow the imported project architecture and maintenance rules.

Every change that affects GitHub Actions behavior (CI, release, or template setup) must update `docs/ci-cd.md` and `docs/ci-workflows.drawio` in the same change. Inspect all affected workflows, including reusable publisher workflows, and keep the diagram accurate for triggers, jobs, dependencies, conditions, artifacts, gates, and destinations. Update the relevant setup or publisher guide when its behavior changes.
