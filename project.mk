# ==============================================================================
#
#  _____  _____   ____       _ ______ _____ _______
# |  __ \|  __ \ / __ \     | |  ____/ ____|__   __|
# | |__) | |__) | |  | |    | | |__ | |       | |
# |  ___/|  _  /| |  | |_   | |  __|| |       | |
# | |    | | \ \| |__| | |__| | |___| |____   | |
# |_|    |_|  \_\\____/ \____/|______\_____|  |_|
#
#   _____ ____  _   _ ______ _____ _____
#  / ____/ __ \| \ | |  ____|_   _/ ____|
# | |   | |  | |  \| | |__    | || |  __
# | |   | |  | | . ` |  __|   | || | |_ |
# | |___| |__| | |\  | |     _| || |__| |
#  \_____\____/|_| \_|_|    |_____\_____|
#
#                     PROJECT CONFIGURATION FILE
#
#  ► Edit THIS file to customise your project.
#  ► Do NOT modify Makefile directly (unless you need new build rules).
#
#  All variables use ?= so they can always be overridden from the command line:
#      make build PYTHON_MAIN_PACKAGE=mypkg
#
#  Optional modules
#  ─────────────────────────────────────────────────────────────────────────────
#  Uncomment the include line at the bottom of this file to activate extra
#  make targets for specific technology stacks:
#    qt.mk  – PySide6/PyQt resource compilation  (gen-qt-res-py target)
#
# ==============================================================================


# ==============================================================================
#  1. PROJECT IDENTITY
#
#  The fundamental metadata that identifies your Python project.
# ==============================================================================

# Name of the importable Python package – the directory that contains
# __init__.py.  Must match the name declared in [project] > name in
# pyproject.toml (with hyphens replaced by underscores if needed).
PYTHON_MAIN_PACKAGE ?= myapp


# ==============================================================================
#  2. FILE PATHS
#
#  Locations of key files used by the build and generation targets.
# ==============================================================================

# Path to the pyproject.toml at the root of the repository.
FILE_PROJECT_TOML ?= pyproject.toml

# Destination path for the auto-generated Python module that mirrors the
# pyproject.toml metadata (name, version, authors, …) as Python constants.
# The gen-project-py target writes to this path at build time.
FILE_PROJECT_PY_GENERATED ?= $(PYTHON_MAIN_PACKAGE)/project.py


# ==============================================================================
#  3. RELEASE SETTINGS
#
#  Variables consumed by CI/CD workflows and the release helper targets.
# ==============================================================================

# Git branch that receives the updated CHANGELOG after each release run.
RELEASE_CHANGELOG_TARGET_BRANCH ?= main

# Set to 1 to enable the Windows installer step in CI, or 0 to skip it.
# When enabled, the workflow expects an Inno Setup script at INNO_SETUP_FILE.
ENABLE_WINDOWS_INSTALLER ?= 0

# Glob patterns for the files to attach to a GitHub Release as artefacts.
# Separate multiple patterns with spaces.
# Examples:
#   dist/*                                          – wheel + sdist only
#   dist/* Output/*.exe                             – wheel + sdist + installer
#   $(foreach a,$(APPS_LIST),dist/$($(a)_NAME)-*)  – per-app wheel globs
RELEASE_ARTIFACTS ?= dist/*


# ==============================================================================
#  4. WINDOWS INSTALLER SETTINGS  (only relevant when ENABLE_WINDOWS_INSTALLER=1)
#
#  These variables drive the `installer` and `build-installer` targets.
# ==============================================================================

# Path to the Inno Setup script (.iss) used to generate the Windows installer.
INNO_SETUP_FILE ?= installer.iss

# Name of the #define inside the .iss file that holds the application version
# string.  The release bump targets update this value automatically via sed.
INNO_SETUP_VERSION_VARIABLE ?= MyAppVersion


# ==============================================================================
#  5. EXECUTABLE APPLICATIONS LIST
#
#  Only required when building standalone binaries with PyInstaller.
#  Leave APPS_LIST empty (default) if you are distributing only a wheel.
# ==============================================================================

# Space-separated list of logical application identifiers to build.
# For each entry <id> you MUST define the four companion variables below.
#
# Leave empty to skip all PyInstaller targets.
APPS_LIST ?=

# ── Template – copy and fill in one block per entry in APPS_LIST ──────────────
#
# Replace <id> with the actual identifier (must match the entry in APPS_LIST).
#
#   <id>_NAME  := <id>                            # Output binary name (no extension)
#   <id>_MAIN  := $(PYTHON_MAIN_PACKAGE)/cli.py   # Entry-point script for PyInstaller
#   <id>_ICO   := resources/icon.ico              # Windows icon (.ico)
#   <id>_ICNS  := resources/icon.icns             # macOS  icon (.icns)
#
# Example (single CLI app):
#   APPS_LIST      := myapp
#   myapp_NAME     := myapp
#   myapp_MAIN     := myapp/__main__.py
#   myapp_ICO      := resources/icon.ico
#   myapp_ICNS     := resources/icon.icns


# ==============================================================================
#  6. OPTIONAL MODULES
#
#  Uncomment the relevant include line to pull in additional make targets.
#  Each .mk file is self-contained and documents its own variables.
# ==============================================================================

# ── Qt / PySide6 ─────────────────────────────────────────────────────────────
# Provides the `gen-qt-res-py` target for compiling .qrc resource files.
# Configure the variables in qt.mk before including it.
#
# include qt.mk
