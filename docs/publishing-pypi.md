# Publishing to PyPI

[PyPI](https://pypi.org/) is the main site for sharing Python packages. This template can publish a package after you push a version tag. Publishing is optional and off by default.

## Before you start

- Set the package name, version, dependencies, and Python requirement in `pyproject.toml`.
- Push your project to GitHub.
- Decide on the PyPI package name. If the package already exists, you need access to its settings. If it is new, configure a pending publisher from your PyPI account settings; see [PyPI's guide for new projects](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/).

## Set up trusted publishing

Trusted publishing lets GitHub prove to PyPI that a release comes from your repository. It uses a short-lived identity, so you do not need to create or store a PyPI API token.

1. In your GitHub repository, open **Settings → Environments** and create an environment named `pypi`. An environment is a named place for release settings and optional approvals. If you choose another name, set `CI_PYPI_ENVIRONMENT` in `project.mk` to match.
2. In the PyPI project settings, add a **Trusted Publisher** for GitHub Actions. For a new package, add a pending publisher from your PyPI account settings instead.
3. Enter your GitHub owner, repository name, workflow filename `release.yml`, and the same environment name. For a new package, also enter the project name exactly as it appears in `pyproject.toml`.
4. In `project.mk`, change the existing `CI_ENABLE_PYPI_PUBLISH` value from `0` to `1`.
5. Push a version tag that matches `pyproject.toml`, for example `v1.2.3` for version `1.2.3`.

Update the existing setting in `project.mk`; do not add a second copy of the line. See [Release Automation](release-automation.md) for creating a tag.

## What happens

GitHub runs the required checks, builds the wheel and source archive once, then gives those same checked files to PyPI. If publishing fails, the GitHub Release is not made public.

You can add approval rules to the `pypi` GitHub environment if a maintainer must approve each publication. For detailed setup, see [PyPI's trusted publisher guide](https://docs.pypi.org/trusted-publishers/).
