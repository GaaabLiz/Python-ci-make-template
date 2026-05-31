# Publishing to Homebrew

This guide explains how to configure automatic publication of a Homebrew formula for each release. Homebrew lets macOS and Linux users install your app with commands such as `brew install acme/tap/myapp`.

---

## Prerequisites

### Project prerequisites

Before publishing to Homebrew, your project must:

1. Already be published on PyPI, because the generated formula installs from PyPI with `pip`.
2. Have `CI_ENABLE_PYPI_PUBLISH=1` configured in `project.mk`.
3. Have at least one successful PyPI release before Homebrew publication is enabled.

If PyPI publication is not configured yet, start with the existing `publish-pypi.yml` workflow.

### On GitHub

1. Create the tap repository.
   - A tap is a Git repository that stores Homebrew formulas.
   - The repository name must start with `homebrew-`.
   - Example: `acme/homebrew-tap`.
2. Generate a Personal Access Token.
   - Fine-grained tokens work well.
   - Give the token `Contents: Read and write` access to the tap repository.
   - Save the token immediately because GitHub will not display it again.
3. Create a GitHub environment in the main project repository.
   - Use `homebrew` unless you also change `CI_HOMEBREW_ENVIRONMENT`.
4. Add the `HOMEBREW_TAP_TOKEN` secret to that environment.

---

## Template configuration

Update the Homebrew settings in `project.mk`:

```makefile
CI_ENABLE_HOMEBREW_PUBLISH ?= 1
CI_HOMEBREW_TAP_REPO ?= acme/homebrew-tap
CI_HOMEBREW_FORMULA_NAME ?= myapp
CI_HOMEBREW_HOMEPAGE ?= https://github.com/acme/myapp
CI_HOMEBREW_DESCRIPTION ?= A Python CLI application
CI_HOMEBREW_LICENSE ?= MIT
```

---

## Tap repository layout

After the first publication, the tap usually looks like this:

```text
homebrew-tap/
|-- README.md
`-- Formula/
    `-- myapp.rb
```

Users can then install the formula with either of these commands:

```bash
brew tap acme/tap
brew install myapp
```

or directly:

```bash
brew install acme/tap/myapp
```

---

## Generated formula

`make ci-generate-homebrew-formula` generates a Ruby formula similar to this:

```ruby
class Myapp < Formula
  desc "A Python CLI application"
  homepage "https://github.com/acme/myapp"
  url "https://pypi.io/packages/source/m/myapp/myapp-1.2.3.tar.gz"
  license "MIT"

  depends_on "python@3.13"

  def install
    virtualenv_install_with_resources
  end

  test do
    system bin/"myapp", "--version"
  end
end
```

The formula downloads the source tarball from PyPI, creates an isolated virtual environment, installs the package and its dependencies, and exposes the CLI entry point in `bin/`.

---

## Local testing

Generate and review the formula locally before enabling the workflow:

```bash
make ci-generate-homebrew-formula
cat dist/homebrew/myapp.rb
mkdir -p "$(brew --repository)/Library/Taps/acme/homebrew-tap/Formula"
cp dist/homebrew/myapp.rb "$(brew --repository)/Library/Taps/acme/homebrew-tap/Formula/"
brew install acme/tap/myapp
myapp --version
brew uninstall myapp
brew untap acme/tap
```

Run a strict audit as well:

```bash
brew audit --strict --new dist/homebrew/myapp.rb
```

---

## How the workflow works

The workflow in `../.github/workflows/publish-homebrew.yml` runs when:

- a `v*` tag is pushed
- the workflow is started manually with `workflow_dispatch`

It performs these steps:

1. Read configuration from `project.mk`.
2. Continue only when `CI_ENABLE_HOMEBREW_PUBLISH=1`.
3. Generate the formula with `make ci-generate-homebrew-formula`.
4. Clone the tap repository using `HOMEBREW_TAP_TOKEN`.
5. Copy the formula into `Formula/myapp.rb`.
6. Commit and push the change to the tap repository.

### Release ordering

Homebrew publication should happen only after PyPI publication succeeds:

```text
make release-patch-tag
-> push tag v1.2.3
-> publish-pypi.yml publishes the package to PyPI
-> publish-homebrew.yml updates the tap formula
-> users can run brew upgrade myapp
```

If the package is not available on PyPI yet when the formula is updated, `brew install` fails with a 404 response. Keep the PyPI workflow ahead of the Homebrew workflow in your release process.

---

## Python and system dependencies

Runtime Python dependencies declared in `pyproject.toml` are handled automatically by `virtualenv_install_with_resources`.

If the formula also needs system dependencies, add them manually in the tap formula, for example:

```ruby
depends_on "libffi"
depends_on "openssl@3"
```

---

## Submitting to homebrew-core

For mature and widely used projects, you can later submit the formula to [homebrew-core](https://github.com/Homebrew/homebrew-core) so users can install it without adding a tap first.

Typical requirements include:

- an actively maintained project
- meaningful adoption signals
- a formula that passes `brew audit --strict --new`
- compliance with the [Acceptable Formulae guidelines](https://docs.brew.sh/Acceptable-Formulae)

The typical process is:

1. Fork `Homebrew/homebrew-core`.
2. Add the formula under the correct `Formula/<first-letter>/` path.
3. Test with `brew install --build-from-source myapp`.
4. Open a pull request to `Homebrew/homebrew-core`.
5. Address maintainer feedback.

Even if the formula is accepted into homebrew-core, it is often still useful to keep your own tap for faster updates and full control.

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| Workflow does not start | `CI_ENABLE_HOMEBREW_PUBLISH=0` | Set it to `1` in `project.mk` |
| Authentication fails while pushing to the tap | Wrong or expired token | Regenerate the PAT and update `HOMEBREW_TAP_TOKEN` |
| Repository not found during clone | Tap repo does not exist or the token lacks access | Create `homebrew-tap` and verify token permissions |
| `brew install` returns 404 | The package is not on PyPI yet | Ensure `publish-pypi.yml` finishes first |
| `brew audit` fails | Formula metadata is incomplete or invalid | Check `CI_HOMEBREW_DESCRIPTION`, `CI_HOMEBREW_LICENSE`, and `CI_HOMEBREW_HOMEPAGE` |
| `No bottle available` warning appears | This is normal for personal taps | It is not an error; Homebrew builds from source |
| Python dependencies are missing at install time | Package metadata is incomplete | Verify runtime dependencies in `pyproject.toml` |
