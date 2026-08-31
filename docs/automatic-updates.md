# Automatic Updates

The template can check and install assets from the latest stable release of a public GitHub
repository. It does not use a GitHub token and deliberately does not support private repositories.

## How it works

1. `myapp/project.py` supplies the installed version and generated update settings.
2. The updater calls `GET /repos/{owner}/{repository}/releases/latest` anonymously.
3. It compares the release tag with the installed version using PEP 440 rules.
4. It selects exactly one release asset using the configured platform pattern.
5. It downloads that asset over HTTPS and verifies its size and GitHub SHA-256 digest.
6. It installs a wheel with the current environment's `pip` or `uv`, or launches a Windows
   installer with the configured arguments.

Drafts and pre-releases are not returned by GitHub's `latest` endpoint. Source archives are never
used as an implicit fallback.

## Package or wheel setup

Declare the public repository, console command, and update policy in `pyproject.toml`:

```toml
[project]
dependencies = ["packaging>=24.2"]

[project.scripts]
myapp = "myapp.cli:main"

[project.urls]
Repository = "https://github.com/your-org/your-repo"

[tool.python-ci-make-template.auto-update]
enabled = true
strategies = { default = "pip" }
asset-patterns = { default = "myapp-*.whl" }
```

Wheel names normalize hyphens to underscores. Check the real name produced in `dist/` before
choosing the pattern. Keep `dist/*` in `RELEASE_ARTIFACTS` so the release workflow uploads it.

Regenerate the runtime metadata after changing the configuration:

```bash
make gen-project-module
```

## Windows installer setup

For a Windows executable packaged by Inno Setup, publish the installer and override the Windows
strategy:

```toml
[tool.python-ci-make-template.auto-update]
enabled = true
strategies = { default = "pip", windows = "installer" }
asset-patterns = { default = "myapp-*.whl", windows = "myapp-setup.exe" }
installer-args = ["/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART", "/SP-"]
```

The matching release configuration is typically:

```makefile
ENABLE_WINDOWS_INSTALLER ?= 1
RELEASE_ARTIFACTS ?= dist/* Output/*.exe
```

The `installer` strategy accepts only a Windows `.exe`. It launches the verified installer and
returns, so an application embedding the updater must then exit. The provided CLI exits naturally.

## Platform-specific assets

Both `strategies` and `asset-patterns` accept `windows`, `macos`, and `linux` keys, with `default`
as fallback. A pattern can use shell wildcards and these placeholders:

- `{version}`: normalized release version, for example `1.4.0`
- `{tag}`: exact GitHub tag, for example `v1.4.0`
- `{platform}`: `windows`, `macos`, or `linux`
- `{machine}`: value reported by Python's `platform.machine()`

The pattern must match exactly one asset. Zero or multiple matches stop the update.

## User commands

Check without modifying the installation:

```bash
myapp update
```

Download, verify, and install without an interactive confirmation:

```bash
myapp update --install
```

The latter form is suitable for a scheduled task or an application-owned update action. It still
requires a restart before the running process uses the new code.

## Application integration

Applications can use the same flow without the template CLI:

```python
from myapp.updater import check_configured_update, install_update

available = check_configured_update()
if available is not None:
    result = install_update(available)
    if result.restart_required:
        raise SystemExit(0)
```

Do not run this synchronously on a GUI thread. Check in a worker, show the release/version to the
user, then install only after an explicit application decision.

## Boundaries and failure modes

- Only `https://github.com/<owner>/<repository>` URLs are accepted.
- Requests are anonymous. A private or missing repository is reported as unavailable.
- Anonymous GitHub API rate limits apply.
- Releases must contain the configured asset and a GitHub `sha256:` digest.
- The `pip` strategy requires a wheel plus either `pip` in the current interpreter or the `uv`
  executable. It does not work from a frozen PyInstaller executable.
- The built-in native installer strategy is Windows/Inno Setup only. macOS app bundles, Linux
  packages, and standalone binary replacement need a project-specific installer strategy.
- Software installed through Homebrew, Chocolatey, or WinGet should normally be upgraded through
  that package manager instead of modifying files behind its back.

Download or integrity failures leave the currently installed version untouched. Downloads use a
temporary `.part` file and are moved into place only after integrity checks pass. A package-manager
failure follows that package manager's own rollback behavior.