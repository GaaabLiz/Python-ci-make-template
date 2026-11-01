# Publishing to PyPI

PyPI publication is an optional job inside release.yml. It receives the exact wheel and source distribution that passed the CI installation smoke tests, so it does not rebuild the package with a different toolchain.

## Configure Trusted Publishing

1. Create or select the package project on PyPI.
2. In the GitHub repository, create an environment named pypi, or set CI_PYPI_ENVIRONMENT to a different name.
3. In the PyPI project settings, add a GitHub Actions trusted publisher with the repository owner, repository name, workflow filename release.yml, and the matching GitHub environment.
4. Set CI_ENABLE_PYPI_PUBLISH to 1 in project.mk.
5. Push a version tag whose value matches the version in pyproject.toml, for example v1.2.3.

No PyPI API token secret is required. The publication job receives id-token permission only after the CI gate and configured release asset builds succeed. It publishes before the GitHub draft release becomes public; if PyPI fails, the release remains a draft.

## Release flow

The release workflow validates the tagged commit, builds and tests the distributions once, optionally publishes them to PyPI, then publishes the GitHub Release. Homebrew waits for PyPI to finish successfully.

Use GitHub environment protection rules if PyPI publication needs maintainer approval. The workflow_dispatch trigger is intentionally absent from publication workflows; manual CI runs cannot publish a branch.
