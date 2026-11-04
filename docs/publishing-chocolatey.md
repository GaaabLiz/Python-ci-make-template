# Publishing to Chocolatey

[Chocolatey](https://chocolatey.org/) is a package manager for Windows. Users install your app from a Windows terminal with a command such as `choco install myapp`.

Publishing to Chocolatey is optional. You do not need Chocolatey installed on your computer for the GitHub release workflow to publish a package. It is useful to install it if you want to test the package locally.

## Before you start

This template's Chocolatey package installs a Windows installer that is attached to your GitHub Release. You need to:

1. Configure a PyInstaller app and Inno Setup installer. See [Build and Packaging](build-and-packaging.md#windows-installer-optional).
2. Set `ENABLE_WINDOWS_INSTALLER=1` and `CI_BUILD_WINDOWS=1` in `project.mk`.
3. Add the installer path, usually `Output/*.exe`, to `RELEASE_ARTIFACTS`.
4. Make sure the installer can run silently, without asking the user questions.

## 1. Create your Chocolatey account and package

1. Create an account at [Chocolatey Community](https://community.chocolatey.org/account/Register).
2. Search [existing packages](https://community.chocolatey.org/packages) to make sure your package ID is available.
3. Create an API key from your Chocolatey account settings. Keep it private.

Chocolatey reserves the package ID when you publish your first version.

## 2. Add the secret to GitHub

In your GitHub repository, open **Settings → Environments** and create an environment named `chocolatey`. An environment is a named place for release settings and private secrets. Add a secret named `CHOCOLATEY_API_KEY` and set its value to the API key from Chocolatey. If you choose another environment name, set `CI_CHOCOLATEY_ENVIRONMENT` in `project.mk` to match.

## 3. Set Chocolatey details in `project.mk`

Edit the existing settings in `project.mk`:

- `CI_CHOCOLATEY_PACKAGE_ID`: the name users type after `choco install`
- `CI_CHOCOLATEY_PACKAGE_TITLE` and `CI_CHOCOLATEY_AUTHORS`: the display name and publisher
- `CI_CHOCOLATEY_PROJECT_URL` and `CI_CHOCOLATEY_LICENSE_URL`: real HTTPS links
- `CI_CHOCOLATEY_SUMMARY` and `CI_CHOCOLATEY_DESCRIPTION`: short and full package descriptions
- `CI_CHOCOLATEY_INSTALLER_URL`: the public URL for the GitHub Release installer

For example, the installer URL should look like:

```text
https://github.com/OWNER/REPOSITORY/releases/download/v{version}/myapp-setup.exe
```

`{version}` is replaced with the version being released. The filename must match the installer name configured by `INNO_OUTPUT_BASE_FILENAME`. Set `CI_CHOCOLATEY_SILENT_ARGS` to the silent-install options supported by your installer; the provided Inno Setup example already uses silent options.

Then set `CI_ENABLE_CHOCOLATEY_PUBLISH` to `1`. Change the existing lines in `project.mk`; do not add a duplicate block. Keep your API key only in the GitHub environment secret.

## 4. Publish a release

Push a version tag such as `v1.2.3`. GitHub builds the Windows installer, adds it to the release, creates the Chocolatey package, and sends it to Chocolatey for review. The package may not appear in search until the review is complete.

## Optional: install Chocolatey to test locally

You can skip this if you only want automatic GitHub publishing. If you want to build or install a package locally, install Chocolatey by following its [official setup guide](https://docs.chocolatey.org/en-us/choco/setup/). The guide includes a WinGet install option. For example, in PowerShell:

```powershell
winget install --id chocolatey.chocolatey --source winget
```

Open a new terminal and check `choco --version`. In Git Bash, build the installer and the Chocolatey package:

```sh
make install-pyinstaller
make ci-build-chocolatey-assets
make ci-pack-chocolatey
```

The package file is written to `dist/chocolatey/`. To install a package after its installer URL is available in a GitHub Release, use an elevated PowerShell or Command Prompt:

```powershell
choco install dist/chocolatey/myapp.1.2.3.nupkg --source . --yes
```

Replace the example filename with the package file in `dist/chocolatey/`. To remove a locally installed test package, run `choco uninstall myapp --yes`.

## If publishing fails

- Confirm `CI_ENABLE_CHOCOLATEY_PUBLISH=1` and `CI_BUILD_WINDOWS=1` in `project.mk`.
- Check the GitHub environment name and the `CHOCOLATEY_API_KEY` secret.
- Make sure the release installer URL is public and points to the right filename.
- If installation fails during review, test the installer with the silent options in `CI_CHOCOLATEY_SILENT_ARGS`.
