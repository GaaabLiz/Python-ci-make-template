# Publishing to Homebrew

[Homebrew](https://brew.sh/) is a package manager used on macOS and Linux. Users can install your app from a terminal with a command such as `brew install yourname/tap/myapp`. A **formula** is Homebrew's set of instructions for installing a package.

Homebrew publishing is optional. GitHub Actions can publish for you; you do not need Homebrew installed on your computer to enable the workflow. Homebrew is needed only if you want to install or test the formula locally.

## Before you start

This template creates a Homebrew formula that installs your Python package from PyPI. Before enabling it:

1. Set up [PyPI publishing](publishing-pypi.md).
2. Publish at least one version to PyPI.
3. If your package has Python runtime dependencies, prepare a Homebrew resource file as described below.

## 1. Create a Homebrew tap

A **tap** is a GitHub repository that stores Homebrew formulas. Create a repository whose name starts with `homebrew-`, for example `yourname/homebrew-tap`.

Create a GitHub access token that can write to this tap repository. Then, in the main project repository, open **Settings → Environments**, create an environment named `homebrew`, and add a secret named `HOMEBREW_TAP_TOKEN` containing the token. An environment is a named place for release settings and private secrets. If you choose another environment name, set `CI_HOMEBREW_ENVIRONMENT` in `project.mk` to match.

## 2. Set formula details in `project.mk`

Edit the existing Homebrew settings:

- Set `CI_HOMEBREW_TAP_REPO` to `yourname/homebrew-tap`.
- Set `CI_HOMEBREW_FORMULA_NAME` to the command users will install.
- Set `CI_HOMEBREW_HOMEPAGE`, `CI_HOMEBREW_DESCRIPTION`, and `CI_HOMEBREW_LICENSE` to real project details. The license is an SPDX identifier such as `MIT`.
- Set `CI_ENABLE_HOMEBREW_PUBLISH` to `1` only after PyPI publication is configured.

Update the existing lines in `project.mk`; do not paste in a second copy. Keep the tap token in the GitHub environment, not in a project file.

## 3. Add Python dependencies (if needed)

If `pyproject.toml` lists Python packages that your app needs when it runs, Homebrew needs their pinned download details too. Set `CI_HOMEBREW_RESOURCES_FILE` in `project.mk` to a file such as `.github/homebrew-resources.rb` and add a Ruby `resource` block for each dependency there.

First generate a formula for a version already published on PyPI:

```sh
make ci-generate-homebrew-formula
```

Homebrew can then help create the resource blocks:

```sh
brew update-python-resources dist/homebrew/<formula-name>.rb
```

Copy the generated `resource` blocks from the formula into the file named by `CI_HOMEBREW_RESOURCES_FILE`. Review their download URLs and SHA-256 values. This step requires Homebrew on the computer where you run it. The configuration check will stop publication if runtime dependencies are missing from the formula.

## 4. Publish a release

Push a version tag after PyPI publishing is ready. The release workflow publishes the package to PyPI first, then creates a formula using that exact source archive and checksum and commits it to your tap. Users can install it with:

```sh
brew install yourname/tap/myapp
```

Replace `yourname/tap/myapp` with the owner, tap name, and formula name you configured.

## Optional: install Homebrew to test locally

Follow the instructions on [brew.sh](https://brew.sh/) to install Homebrew on macOS or Linux. The installer explains what it will do. After it is installed, you can install tools such as `uv` with `brew install uv`.

To inspect the generated formula, run `make ci-generate-homebrew-formula` and open `dist/homebrew/<formula-name>.rb`. Formula generation requires the package version to exist on PyPI.

## If publishing fails

- Check that `CI_ENABLE_PYPI_PUBLISH=1` and `CI_ENABLE_HOMEBREW_PUBLISH=1` are both set.
- Check that the `homebrew` GitHub environment contains `HOMEBREW_TAP_TOKEN` and that the token can write to the tap.
- Confirm the tap repository exists and its name starts with `homebrew-`.
- If the formula has missing Python packages, add their `resource` blocks and set `CI_HOMEBREW_RESOURCES_FILE`.
