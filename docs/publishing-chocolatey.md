# Publishing to Chocolatey

This guide explains how to configure automatic Chocolatey publication for each release. Chocolatey is a Windows package manager and lets users install your app with `choco install myapp`.

---

## Prerequisites

### Project prerequisites

Before publishing to Chocolatey, your project must have:

1. A working Windows installer. Chocolatey downloads and installs your `.exe` silently.
2. `ENABLE_WINDOWS_INSTALLER=1` in `project.mk`.
3. A GitHub Release that includes the installer executable as an asset.

If the Windows installer is not set up yet, start with [build-and-packaging.md](build-and-packaging.md#windows-installer).

### On Chocolatey.org

1. Create an account at [community.chocolatey.org](https://community.chocolatey.org/account/Register).
2. Get your API key from `Account -> API Keys`.
3. Check whether your package ID is already taken by searching [community.chocolatey.org/packages](https://community.chocolatey.org/packages).

The first successful push reserves the package ID. You do not need to register it separately.

### On GitHub

4. Create an environment from `Settings -> Environments -> New environment`.
   - Use `chocolatey` unless you also change `CI_CHOCOLATEY_ENVIRONMENT` in `project.mk`.
5. Add this secret to the `chocolatey` environment:

   | Secret | Value |
   |--------|-------|
   | `CHOCOLATEY_API_KEY` | The API key copied from Chocolatey |

---

## Template configuration

Update the Chocolatey settings in `project.mk`:

```makefile
CI_ENABLE_CHOCOLATEY_PUBLISH ?= 1
CI_CHOCOLATEY_PACKAGE_ID ?= myapp
CI_CHOCOLATEY_PACKAGE_TITLE ?= My App
CI_CHOCOLATEY_AUTHORS ?= Your Name
CI_CHOCOLATEY_PROJECT_URL ?= https://github.com/your-org/your-repo
CI_CHOCOLATEY_LICENSE_URL ?= https://github.com/your-org/your-repo/blob/main/LICENSE
CI_CHOCOLATEY_TAGS ?= python cli utility
CI_CHOCOLATEY_SUMMARY ?= Windows package for My App
CI_CHOCOLATEY_DESCRIPTION ?= My App packaged from the GitHub release artifacts.
CI_CHOCOLATEY_INSTALLER_URL ?= https://github.com/your-org/your-repo/releases/download/v{version}/myapp-setup.exe
CI_CHOCOLATEY_SILENT_ARGS ?= /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-
```

Make sure these values stay aligned:

- `CI_CHOCOLATEY_INSTALLER_URL` must point to the actual GitHub Release asset.
- The filename in the URL must match `INNO_OUTPUT_BASE_FILENAME` plus `.exe`.
- The installer must support the silent flags in `CI_CHOCOLATEY_SILENT_ARGS`.

---

## Local testing on Windows

```powershell
make build-installer
make ci-pack-chocolatey
choco install dist/chocolatey/myapp.1.0.0.nupkg --source . --yes
myapp --version
choco uninstall myapp --yes
```

---

## How the workflow works

The workflow in `../.github/workflows/publish-chocolatey.yml` runs when:

- a `v*` tag is pushed, for example `v1.2.3`
- the workflow is started manually with `workflow_dispatch`

The workflow does the following:

1. Read configuration from `project.mk` with `make ci-export-config`.
2. Continue only when `CI_ENABLE_CHOCOLATEY_PUBLISH=1`.
3. Install `make` and `uv` on the Windows runner.
4. Build Windows release assets with `make ci-build-chocolatey-assets`.
5. Generate the `.nuspec` and `chocolateyinstall.ps1` files with `make ci-pack-chocolatey`.
6. Push the `.nupkg` to Chocolatey with `make ci-publish-chocolatey`.

`ci-pack-chocolatey` generates:

```text
.chocolatey/
|-- myapp.nuspec
`-- tools/
    `-- chocolateyinstall.ps1

dist/chocolatey/
`-- myapp.1.2.3.nupkg
```

---

## Chocolatey moderation

After the first push to the community feed, the package goes through automated checks and sometimes manual moderation.

Typical checks include:

- package structure validation
- installer download validation
- checksum verification
- antivirus and reputation checks
- metadata and packaging guideline review

Typical timing:

- automated validation: minutes
- first package manual review: often 1 to 7 days
- later updates: often much faster if the package stays consistent

To reduce moderation delays:

- keep `CI_CHOCOLATEY_INSTALLER_URL` public and stable
- provide clear project metadata
- verify the installer is fully silent
- keep the same package ID after the first release

---

## Typical release flow

```text
make release-patch-tag
-> push tag v1.2.3
-> release.yml publishes the installer asset
-> publish-chocolatey.yml generates and pushes the package
-> Chocolatey validates it
-> users can run choco install myapp
```

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| Workflow does not start | `CI_ENABLE_CHOCOLATEY_PUBLISH=0` | Set it to `1` in `project.mk` |
| `API key is invalid` | Wrong secret value | Check `CHOCOLATEY_API_KEY` in the GitHub environment |
| `No .nupkg file found` | Packaging step was not run | Run `make ci-pack-chocolatey` first |
| Validation fails because the URL is unavailable | Release is private or the URL is wrong | Verify the GitHub Release asset URL |
| Validation fails because installation times out | Silent flags are not correct | Test the installer locally with `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-` |
| Package is rejected in moderation | Metadata or package behavior does not meet guidelines | Review the moderator feedback and update the package |
| Version conflict | The same version already exists on Chocolatey | Bump the version and publish again |
