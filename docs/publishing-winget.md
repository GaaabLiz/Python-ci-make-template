# Publishing to WinGet

[WinGet](https://learn.microsoft.com/windows/package-manager/winget/) is Windows' built-in package manager. Users can install your app from a terminal with a command such as `winget install YourCompany.MyApp`.

This template sends a package update to Microsoft's community catalog. It is optional and off by default. Microsoft reviews and accepts the update before it appears in WinGet.

The update uses three small YAML files, called **manifests**, to describe the package, its version, and its installer.

## Before you start

You need a Windows installer that can install silently, without opening questions or windows that need user input. This template uses Inno Setup. See [Build and Packaging](build-and-packaging.md#windows-installer-optional).

Set `APPS_LIST` and the app's settings, then set `ENABLE_WINDOWS_INSTALLER=1` and `CI_BUILD_WINDOWS=1` in `project.mk`. Add the installer path, usually `Output/*.exe`, to `RELEASE_ARTIFACTS`.

## 1. Fork the WinGet packages repository

The official catalog is [microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs). Create a fork under your GitHub account or organization. The template opens a pull request from your fork to Microsoft's repository; it does not publish directly to Microsoft.

## 2. Add a GitHub token

Create a GitHub token that can write to your fork and open a pull request to `microsoft/winget-pkgs`. In your project repository, open **Settings → Environments**, create an environment named `winget`, and add a secret called `WINGET_GITHUB_TOKEN`. An environment is a named place for release settings and private secrets. If you use another environment name, set `CI_WINGET_ENVIRONMENT` in `project.mk` to match.

Keep the token secret. Do not put it in `project.mk` or commit it to the repository.

## 3. Set the package details in `project.mk`

Edit the existing `CI_WINGET_...` settings:

- `CI_WINGET_FORK_REPO`: your fork, such as `yourname/winget-pkgs`
- `CI_WINGET_PACKAGE_IDENTIFIER`: a unique ID in `Publisher.AppName` form, such as `YourCompany.MyApp`
- `CI_WINGET_PACKAGE_NAME` and `CI_WINGET_PUBLISHER`: the names users see in Windows
- `CI_WINGET_LICENSE`, `CI_WINGET_LICENSE_URL`, `CI_WINGET_HOMEPAGE`, and `CI_WINGET_SHORT_DESCRIPTION`: real package information
- `CI_WINGET_INSTALLER_URL`: the public GitHub Release URL; keep the `{version}` placeholder and use the actual installer filename
- `CI_WINGET_INSTALLER_FILE`: the path to that installer in the release build, usually already set by the template
- `CI_ENABLE_WINGET_PUBLISH`: set to `1` after the fork, token, and installer are ready

Update the existing lines rather than adding a second copy of them.

## 4. Push a release tag

When you push a version tag, GitHub builds the Windows installer once. That exact Windows build is attached to the GitHub Release and downloaded by the WinGet job. The job calculates a SHA-256 fingerprint from this installer and writes it into the manifest. WinGet uses it to check that the downloaded file is the same installer.

The job creates the three manifest files and opens a pull request to Microsoft's repository. Microsoft reviews the pull request; the package is available in WinGet after it is accepted.

## Optional: check the manifest on Windows

The release workflow handles the build and hash for you, so local setup is optional. To check locally, use Git Bash or MSYS2 on Windows. The asset build installs Inno Setup with Chocolatey; see [Getting Started](getting-started.md#optional-homebrew-and-chocolatey) first.

```sh
make install-pyinstaller
make ci-build-winget-assets
make ci-generate-winget-manifests
make ci-validate-winget-manifests
```

Review the files in `dist/winget/`. Check that the package ID, version, installer URL, publisher, and package name are correct. Run a test installation in Windows Sandbox before asking Microsoft to accept the package.

## If publishing fails

- Check that the fork exists and `CI_WINGET_FORK_REPO` uses `owner/winget-pkgs` format.
- Check the `winget` environment contains the `WINGET_GITHUB_TOKEN` secret and that the token can access the fork.
- Make sure `CI_WINGET_INSTALLER_URL` points to the public release asset and its filename matches the installer.
- If Microsoft rejects the pull request, read its feedback and correct the project settings or installer before sending an update.
