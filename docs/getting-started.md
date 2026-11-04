# Getting Started

Follow these steps once after creating a repository from the template. You do not need Homebrew or Chocolatey to publish from GitHub Actions. On Windows, the Git Bash setup below uses Chocolatey to install Make; WSL uses Ubuntu's package manager instead.

## 1. Install the basic tools

You need Git, GNU Make, and `uv`.

- Install Git from [git-scm.com](https://git-scm.com/downloads).
- On macOS, install Apple's command-line tools with `xcode-select --install`. This provides `make`.
- On Linux, install `make` with your system's package manager.
- On Windows, use a WSL Linux terminal or Git Bash/MSYS2. The Makefile uses Unix-style shell commands, so do not run it directly in PowerShell. In Ubuntu on WSL, install Make with `sudo apt update && sudo apt install make`. If you use Git Bash, install Chocolatey through WinGet as described below, then run `choco install make --yes` in PowerShell opened as administrator.
- Install `uv` using the [official instructions](https://docs.astral.sh/uv/getting-started/installation/). On macOS/Linux, one option is `curl -LsSf https://astral.sh/uv/install.sh | sh`. In PowerShell, one option is `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`.

Open a new terminal after installing tools, then check they are available:

```sh
git --version
make --version
uv --version
```

If a command is not found, install that tool or reopen the terminal so it can refresh its command list.

## 2. Set your project details

Edit these files:

1. In `pyproject.toml`, set the package name, version, description, Python requirement, and Python dependencies.
2. In `project.mk`, set the name of your Python package folder and any project-specific test or CI options.

The template keeps reusable commands in `Makefile`. Do not edit it just to set your project's name, paths, Python versions, or publishing settings. For details, see [Configuration](configuration.md).

## 3. Install project dependencies

From the repository folder, run:

```sh
make install-dev
```

This uses `uv` and `uv.lock` to prepare the local Python environment and install the development tools. If you change dependencies in `pyproject.toml`, update and commit `uv.lock` too.

## 4. Run the first checks

```sh
make ci-log-config
make qa
make build
```

- `ci-log-config` prints the settings that the template will use.
- `qa` checks code style and runs tests.
- `build` creates the Python package files in `dist/`.

If a command fails, start with [Troubleshooting](troubleshooting.md).

## Optional: Homebrew and Chocolatey

These are package managers used by end users to install published apps. They are not needed for the normal template setup or for publishing a Python package.

- To test a Homebrew formula on macOS or Linux, install Homebrew using the official instructions on [brew.sh](https://brew.sh/). The standard command is:

  ```sh
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

  The script explains what it will do and pauses before continuing. Follow any final setup steps it prints, then check `brew --version`. Run `brew install uv` if you want to install uv with Homebrew.
- To test a Chocolatey package on Windows, install Chocolatey using its [official setup guide](https://docs.chocolatey.org/en-us/choco/setup/). If WinGet is available, open PowerShell as administrator and run `winget install --id chocolatey.chocolatey --source winget`. Open a new terminal and check `choco --version`. The template's local `make install-inno` command uses Chocolatey to install Inno Setup.

You can configure automatic publication from GitHub Actions without installing either package manager on your own computer. Read the relevant [Homebrew](publishing-homebrew.md) or [Chocolatey](publishing-chocolatey.md) guide when you want to enable it.
