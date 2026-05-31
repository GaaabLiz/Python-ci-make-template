# Publishing to WinGet

This guide explains how to configure automatic WinGet manifest publication for each release. WinGet lets Windows users install your application with commands such as `winget install YourCompany.MyApp`.

---

## Prerequisites

### Project prerequisites

Before publishing to WinGet, your project must provide:

1. A working Windows installer that supports silent installation.
2. `ENABLE_WINDOWS_INSTALLER=1` in `project.mk`.
3. A `.exe` release asset published on GitHub with a stable URL for each version.
4. A unique package identifier in `Publisher.Package` format.

WinGet validation is strict about these points:

- the installer must support unattended installation
- the installer URL must be public and use HTTPS
- `InstallerSha256` must match the downloadable binary exactly
- `Publisher` and `PackageName` must match what users see in Windows application metadata

### External setup on GitHub

#### 1. Fork `microsoft/winget-pkgs`

Open the official repository at `https://github.com/microsoft/winget-pkgs`, click `Fork`, and create a fork under your user or organization, for example `your-user/winget-pkgs`.

The template does not publish directly to Microsoft's repository. It pushes a branch to your fork and then opens a pull request against `microsoft/winget-pkgs`.

#### 2. Create a GitHub Personal Access Token

Create a token from GitHub settings. The simplest option is a classic token with `repo` scope because the workflow needs to:

- push to your fork
- create a pull request against the upstream repository

Save the token immediately because GitHub will not show it again.

#### 3. Create a GitHub environment

In the repository that uses this template:

1. Go to `Settings -> Environments`
2. Create the `winget` environment
3. Add the `WINGET_GITHUB_TOKEN` secret with the token created above

You can use a different environment name, but it must match `CI_WINGET_ENVIRONMENT` in `project.mk`.

---

## Template configuration

Set at least these variables in `project.mk`:

```makefile
CI_ENABLE_WINGET_PUBLISH ?= 1
CI_WINGET_ENVIRONMENT ?= winget
CI_WINGET_FORK_REPO ?= your-user/winget-pkgs
CI_WINGET_PACKAGE_IDENTIFIER ?= YourCompany.MyApp
CI_WINGET_PACKAGE_NAME ?= My App
CI_WINGET_PUBLISHER ?= Your Company
CI_WINGET_PACKAGE_LOCALE ?= en-US
CI_WINGET_SHORT_DESCRIPTION ?= Windows installer for My App
CI_WINGET_LICENSE ?= MIT
CI_WINGET_LICENSE_URL ?= https://github.com/your-org/your-repo/blob/main/LICENSE
CI_WINGET_HOMEPAGE ?= https://github.com/your-org/your-repo
CI_WINGET_TAGS ?= python cli
CI_WINGET_INSTALLER_URL ?= https://github.com/your-org/your-repo/releases/download/v{version}/myapp-setup.exe
CI_WINGET_INSTALLER_TYPE ?= inno
CI_WINGET_INSTALLER_ARCHITECTURE ?= x64
CI_WINGET_INSTALLER_FILE ?= Output/myapp-setup.exe
```

Important notes:

- `CI_WINGET_PACKAGE_IDENTIFIER` must be unique across WinGet.
- `CI_WINGET_INSTALLER_URL` must point to the real GitHub Release asset.
- `CI_WINGET_INSTALLER_TYPE` is normally `inno` for this template.
- `CI_WINGET_INSTALLER_FILE` is the local file used to calculate `InstallerSha256`.

---

## What the template provides

The template now includes:

- `../.github/workflows/publish-winget.yml`
- `make ci-build-winget-assets`
- `make ci-generate-winget-manifests`
- `make ci-validate-winget-manifests`
- `make ci-publish-winget`

The automation flow is:

1. GitHub Actions reads configuration from `project.mk`.
2. It builds the Windows assets needed by the manifest.
3. It generates the three WinGet manifest files.
4. It validates them with `winget validate` when the command is available.
5. It clones your `winget-pkgs` fork.
6. It copies the generated manifests into the path required by Microsoft.
7. It pushes a branch to your fork.
8. It opens a pull request to `microsoft/winget-pkgs`.

---

## Generated manifests

The template generates the multi-file format recommended by Microsoft:

- `PackageIdentifier.yaml` for the version manifest
- `PackageIdentifier.locale.en-US.yaml` for the default locale metadata
- `PackageIdentifier.installer.yaml` for installer metadata

The generated files are written under a path like this:

```text
dist/winget/manifests/y/YourCompany/MyApp/1.2.3/
```

This matches the repository convention:

```text
manifests/<publisher-first-letter>/<Publisher>/<Package>/<Version>/
```

---

## Recommended local testing

Before enabling the workflow, test the flow on Windows.

### 1. Build the installer

```powershell
make ci-build-winget-assets
```

### 2. Generate the manifests

```powershell
make ci-generate-winget-manifests
```

### 3. Validate the manifests

```powershell
make ci-validate-winget-manifests
```

### 4. Inspect the generated metadata

Verify that:

- `PackageIdentifier` is correct
- `PackageVersion` matches the release
- `InstallerUrl` points to the real asset
- `InstallerSha256` was calculated from the correct file
- `Publisher` and `PackageName` match the Windows installed-app metadata

### 5. Verify unattended installation

For Inno Setup installers, test at least this command:

```powershell
Output\myapp-setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-
```

Microsoft also recommends testing the manifest in Windows Sandbox before the first submission.

---

## How publication actually works

The workflow in `../.github/workflows/publish-winget.yml` runs when:

- a `v*` tag is pushed
- the workflow is started manually with `workflow_dispatch`

A typical flow looks like this:

```text
make release-patch-tag
-> release.yml publishes the release and uploads the installer
-> publish-winget.yml generates the manifests
-> publish-winget.yml opens a pull request against microsoft/winget-pkgs
-> Microsoft validates the pull request
-> the package enters the WinGet catalog
```

WinGet does not publish directly from your repository. The package becomes available only after Microsoft accepts the pull request in `microsoft/winget-pkgs`.

---

## Microsoft review process

After the pull request is created, Microsoft runs automated validation and may also perform manual review. The published documentation highlights checks such as:

- manifest syntax and schema validation
- repository path validation
- installer URL availability
- SHA256 hash verification
- silent install and uninstall behavior
- security and antivirus checks

Common outcomes to expect:

- the first package often receives more manual review
- packages can be rejected if silent installation is not reliable
- pull requests may be closed if feedback is not addressed
- only one package version should be submitted per pull request

---

## Practical checks before opening a pull request

Before submitting, confirm that:

1. The installer URL is public and uses HTTPS.
2. The URL content does not change after the release is published.
3. The binary is not rebuilt after `InstallerSha256` is generated.
4. Silent installation really works without blocking UI.
5. `Publisher` and `PackageName` match Add/Remove Programs metadata.
6. The package identifier does not conflict with an existing WinGet package.

You can search locally with:

```powershell
winget search MyApp
```

It is also worth searching the `microsoft/winget-pkgs` repository before deciding on `CI_WINGET_PACKAGE_IDENTIFIER`.

---

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|--------------|-----|
| Workflow does not start | `CI_ENABLE_WINGET_PUBLISH=0` | Set it to `1` in `project.mk` |
| Fork-related error | `CI_WINGET_FORK_REPO` is wrong or the fork does not exist | Create the fork and fix the value |
| GitHub authentication error | Missing secret or expired token | Regenerate the token and update `WINGET_GITHUB_TOKEN` |
| Manifest validation error | Invalid YAML or invalid fields | Run `make ci-validate-winget-manifests` and correct the manifest |
| Hash mismatch | The installer changed or the URL points to a different file | Regenerate the manifest and make sure the local file matches the release asset |
| Installer availability error | The URL is not public or the filename is wrong | Check the GitHub Release asset URL |
| `Validation-Unattended-Failed` | The installer is not fully silent | Test the Inno Setup silent switches manually |
| `Validation-Domain` or `Validation-Indirect-URL` | The installer URL is not considered direct or trusted enough | Use the direct publisher-controlled release asset URL |
| Pull request already exists | The workflow was rerun for the same version | The target detects the existing pull request and does not open a second one |

---

## WinGet and Chocolatey together

If you already ship a Windows installer, supporting both WinGet and Chocolatey is often useful:

- Chocolatey is common in environments standardized on `choco`
- WinGet is Microsoft's native package catalog and integrates well with modern Windows setups

The two channels complement each other. This template can now drive both from the same Inno Setup installer.