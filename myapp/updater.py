"""Aggiornamenti verificati da release pubbliche GitHub."""

from __future__ import annotations

import fnmatch
import hashlib
import hmac
import importlib.util
import json
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from packaging.version import InvalidVersion, Version

from myapp import project

GITHUB_API_VERSION = "2026-03-10"
DEFAULT_TIMEOUT = 15.0
DEFAULT_INSTALLER_ARGS = (
    "/VERYSILENT",
    "/SUPPRESSMSGBOXES",
    "/NORESTART",
    "/SP-",
)
SUPPORTED_STRATEGIES = {"installer", "pip"}


class UpdateError(RuntimeError):
    """Errore atteso durante il controllo o l'installazione di un aggiornamento."""


class UpdateConfigurationError(UpdateError):
    """Configurazione dell'auto-update assente o non valida."""


class AutoUpdateDisabled(UpdateConfigurationError):
    """Auto-update disabilitato esplicitamente per il progetto."""


class RepositoryUnavailableError(UpdateError):
    """Repository pubblico o API GitHub non raggiungibile."""


class UpdateDownloadError(UpdateError):
    """Download dell'asset non riuscito."""


class UpdateIntegrityError(UpdateError):
    """Asset privo di digest valido o con contenuto alterato."""


class UpdateInstallationError(UpdateError):
    """Installazione dell'aggiornamento non riuscita."""


@dataclass(frozen=True, slots=True)
class ReleaseAsset:
    name: str
    download_url: str
    size: int
    digest: str | None


@dataclass(frozen=True, slots=True)
class GitHubRelease:
    repository: str
    tag_name: str
    version: Version
    page_url: str
    assets: tuple[ReleaseAsset, ...]


@dataclass(frozen=True, slots=True)
class AvailableUpdate:
    current_version: Version
    release: GitHubRelease
    asset: ReleaseAsset
    platform: str
    strategy: str
    installer_args: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class InstallResult:
    strategy: str
    restart_required: bool
    downloaded_path: Path | None = None


def parse_public_github_repository(repository_url: str) -> str:
    """Restituisce ``owner/repository`` solo per URL HTTPS github.com validi."""
    parsed = urlsplit(repository_url)
    try:
        port = parsed.port
    except ValueError as error:
        raise UpdateConfigurationError("Repository URL has an invalid port.") from error

    if (
        parsed.scheme != "https"
        or parsed.hostname is None
        or parsed.hostname.lower() != "github.com"
        or parsed.username is not None
        or parsed.password is not None
        or port is not None
        or parsed.query
        or parsed.fragment
    ):
        raise UpdateConfigurationError(
            "Auto-update requires a public https://github.com/<owner>/<repository> URL."
        )

    repository_path = parsed.path.removeprefix("/").removesuffix("/")
    owner_and_name = repository_path.split("/")
    if len(owner_and_name) != 2:
        raise UpdateConfigurationError(
            "Repository URL must contain exactly one owner and one repository name."
        )

    owner, repository = owner_and_name
    repository = repository.removesuffix(".git")
    valid_component = re.compile(r"[A-Za-z0-9_.-]+")
    if (
        not owner
        or not repository
        or not all(valid_component.fullmatch(component) for component in (owner, repository))
    ):
        raise UpdateConfigurationError("Repository URL contains unsupported characters.")

    return f"{owner}/{repository}"


def _open_url(request: Request, timeout: float):
    return urlopen(request, timeout=timeout)


def _request_json(url: str, timeout: float) -> Mapping[str, object]:
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": GITHUB_API_VERSION,
            "User-Agent": "python-ci-make-template-auto-updater",
        },
    )
    try:
        with _open_url(request, timeout) as response:
            payload: object = json.load(response)
    except HTTPError as error:
        if error.code == 404:
            raise RepositoryUnavailableError(
                "GitHub repository or release not found. The repository must be public."
            ) from error
        if error.code == 403:
            raise RepositoryUnavailableError(
                "GitHub API refused the anonymous request, possibly due to rate limiting."
            ) from error
        raise RepositoryUnavailableError(f"GitHub API returned HTTP {error.code}.") from error
    except (OSError, URLError, json.JSONDecodeError) as error:
        raise RepositoryUnavailableError(f"Cannot read the GitHub API response: {error}") from error

    if not isinstance(payload, dict) or not all(isinstance(key, str) for key in payload):
        raise RepositoryUnavailableError("GitHub API returned an unexpected response.")
    return cast("dict[str, object]", payload)


def _required_string(data: Mapping[str, object], key: str, context: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise RepositoryUnavailableError(f"GitHub {context} has no valid {key!r} field.")
    return value


def _parse_release(payload: Mapping[str, object], repository: str) -> GitHubRelease:
    tag_name = _required_string(payload, "tag_name", "release")
    page_url = _required_string(payload, "html_url", "release")
    try:
        release_version = Version(tag_name)
    except InvalidVersion as error:
        raise RepositoryUnavailableError(
            f"GitHub release tag {tag_name!r} is not a valid Python version."
        ) from error

    raw_assets = payload.get("assets")
    if not isinstance(raw_assets, list):
        raise RepositoryUnavailableError("GitHub release has no valid 'assets' collection.")

    owner, repository_name = repository.split("/", maxsplit=1)
    expected_path_prefix = f"/{owner}/{repository_name}/releases/download/"
    assets: list[ReleaseAsset] = []
    for raw_asset in raw_assets:
        if not isinstance(raw_asset, dict) or not all(isinstance(key, str) for key in raw_asset):
            raise RepositoryUnavailableError("GitHub release contains an invalid asset.")
        asset_data = cast("dict[str, object]", raw_asset)
        name = _required_string(asset_data, "name", "asset")
        download_url = _required_string(asset_data, "browser_download_url", "asset")
        parsed_download_url = urlsplit(download_url)
        if (
            parsed_download_url.scheme != "https"
            or parsed_download_url.hostname != "github.com"
            or not parsed_download_url.path.casefold().startswith(expected_path_prefix.casefold())
        ):
            raise RepositoryUnavailableError(f"GitHub asset {name!r} has an unsafe download URL.")

        size = asset_data.get("size")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise RepositoryUnavailableError(f"GitHub asset {name!r} has an invalid size.")
        digest = asset_data.get("digest")
        if digest is not None and not isinstance(digest, str):
            raise RepositoryUnavailableError(f"GitHub asset {name!r} has an invalid digest.")
        assets.append(ReleaseAsset(name, download_url, size, digest))

    return GitHubRelease(repository, tag_name, release_version, page_url, tuple(assets))


def fetch_latest_release(repository_url: str, timeout: float = DEFAULT_TIMEOUT) -> GitHubRelease:
    """Recupera l'ultima release stabile tramite API anonima di GitHub."""
    repository = parse_public_github_repository(repository_url)
    api_url = f"https://api.github.com/repos/{repository}/releases/latest"
    return _parse_release(_request_json(api_url, timeout), repository)


def _platform_key(platform_name: str | None) -> str:
    value = platform_name or sys.platform
    if value.startswith("win"):
        return "windows"
    if value == "darwin" or value == "macos":
        return "macos"
    if value.startswith("linux"):
        return "linux"
    raise UpdateConfigurationError(f"Unsupported update platform: {value!r}.")


def _platform_setting(config: Mapping[str, object], key: str, platform_key: str) -> str:
    values = config.get(key)
    if not isinstance(values, Mapping):
        raise UpdateConfigurationError(f"Auto-update setting {key!r} must be a table.")
    platform_values = cast("Mapping[str, object]", values)
    value = platform_values.get(platform_key)
    if value is None:
        value = platform_values.get("default")
    if not isinstance(value, str) or not value:
        raise UpdateConfigurationError(
            f"Auto-update setting {key!r} has no value for {platform_key!r} or 'default'."
        )
    return value


def _installer_args(config: Mapping[str, object], strategy: str) -> tuple[str, ...]:
    if strategy != "installer":
        return ()
    raw_args = config.get("installer-args", DEFAULT_INSTALLER_ARGS)
    if (
        not isinstance(raw_args, Sequence)
        or isinstance(raw_args, str)
        or not all(isinstance(argument, str) for argument in raw_args)
    ):
        raise UpdateConfigurationError("Auto-update 'installer-args' must be an array of strings.")
    return tuple(cast(str, argument) for argument in raw_args)


def check_for_update(
    repository_url: str,
    current_version: str,
    config: Mapping[str, object],
    *,
    platform_name: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> AvailableUpdate | None:
    """Controlla l'ultima release e seleziona l'asset configurato, senza installarlo."""
    platform_key = _platform_key(platform_name)
    strategy = _platform_setting(config, "strategies", platform_key)
    if strategy not in SUPPORTED_STRATEGIES:
        raise UpdateConfigurationError(f"Unsupported update strategy: {strategy!r}.")
    pattern_template = _platform_setting(config, "asset-patterns", platform_key)
    installer_args = _installer_args(config, strategy)

    try:
        installed_version = Version(current_version)
    except InvalidVersion as error:
        raise UpdateConfigurationError(
            f"Installed version {current_version!r} is not a valid Python version."
        ) from error

    release = fetch_latest_release(repository_url, timeout)
    if release.version <= installed_version:
        return None

    try:
        asset_pattern = pattern_template.format(
            version=release.version,
            tag=release.tag_name,
            platform=platform_key,
            machine=platform.machine().lower() or "unknown",
        )
    except (KeyError, ValueError) as error:
        raise UpdateConfigurationError(f"Invalid asset pattern {pattern_template!r}.") from error

    matching_assets = [
        asset for asset in release.assets if fnmatch.fnmatchcase(asset.name, asset_pattern)
    ]
    if len(matching_assets) != 1:
        names = ", ".join(asset.name for asset in release.assets) or "<none>"
        raise UpdateConfigurationError(
            f"Asset pattern {asset_pattern!r} matched {len(matching_assets)} assets; "
            f"release assets: {names}."
        )

    return AvailableUpdate(
        installed_version,
        release,
        matching_assets[0],
        platform_key,
        strategy,
        installer_args,
    )


def check_configured_update(
    *, platform_name: str | None = None, timeout: float = DEFAULT_TIMEOUT
) -> AvailableUpdate | None:
    """Controlla gli aggiornamenti usando i metadati generati da ``pyproject.toml``."""
    config = project.auto_update
    if not isinstance(config, Mapping):
        raise UpdateConfigurationError("Generated auto-update configuration is invalid.")
    if config.get("enabled") is not True:
        raise AutoUpdateDisabled("Auto-update is disabled in pyproject.toml.")
    if not isinstance(project.repository_url, str) or not project.repository_url:
        raise UpdateConfigurationError("No project.urls.Repository URL is configured.")
    return check_for_update(
        project.repository_url,
        project.version,
        config,
        platform_name=platform_name,
        timeout=timeout,
    )


def _expected_sha256(asset: ReleaseAsset) -> str:
    digest = asset.digest
    if digest is None or not digest.startswith("sha256:"):
        raise UpdateIntegrityError(
            f"GitHub asset {asset.name!r} has no SHA-256 digest; refusing to install it."
        )
    expected_hash = digest.removeprefix("sha256:").lower()
    if re.fullmatch(r"[0-9a-f]{64}", expected_hash) is None:
        raise UpdateIntegrityError(f"GitHub asset {asset.name!r} has an invalid SHA-256 digest.")
    return expected_hash


def download_update(
    update: AvailableUpdate,
    destination: Path,
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> Path:
    """Scarica l'asset in modo atomico e ne verifica dimensione e SHA-256."""
    if Path(update.asset.name).name != update.asset.name:
        raise UpdateIntegrityError("GitHub asset name is not a safe file name.")
    expected_hash = _expected_sha256(update.asset)
    target = destination / update.asset.name
    partial = target.with_name(f"{target.name}.part")
    request = Request(
        update.asset.download_url,
        headers={"Accept": "application/octet-stream", "User-Agent": "python-auto-updater"},
    )
    actual_hash = hashlib.sha256()
    downloaded_size = 0
    try:
        destination.mkdir(parents=True, exist_ok=True)
        with _open_url(request, timeout) as response, partial.open("wb") as file_handle:
            while chunk := response.read(1024 * 1024):
                file_handle.write(chunk)
                actual_hash.update(chunk)
                downloaded_size += len(chunk)
        if downloaded_size != update.asset.size:
            raise UpdateIntegrityError(
                f"Downloaded size is {downloaded_size}, expected {update.asset.size}."
            )
        if not hmac.compare_digest(actual_hash.hexdigest(), expected_hash):
            raise UpdateIntegrityError("Downloaded asset does not match GitHub's SHA-256 digest.")
        partial.replace(target)
    except UpdateError:
        partial.unlink(missing_ok=True)
        raise
    except (HTTPError, OSError, URLError) as error:
        partial.unlink(missing_ok=True)
        raise UpdateDownloadError(f"Cannot download {update.asset.name!r}: {error}") from error
    return target


def _pip_install_command(wheel_path: Path) -> list[str]:
    if wheel_path.suffix != ".whl":
        raise UpdateConfigurationError("The 'pip' strategy requires a wheel asset.")
    if getattr(sys, "frozen", False):
        raise UpdateInstallationError("The 'pip' strategy cannot update a frozen executable.")
    if importlib.util.find_spec("pip") is not None:
        return [sys.executable, "-m", "pip", "install", "--upgrade", str(wheel_path)]
    uv_executable = shutil.which("uv")
    if uv_executable is not None:
        return [
            uv_executable,
            "pip",
            "install",
            "--python",
            sys.executable,
            "--upgrade",
            str(wheel_path),
        ]
    raise UpdateInstallationError("Neither pip nor uv is available to install the wheel.")


def install_update(update: AvailableUpdate, *, timeout: float = DEFAULT_TIMEOUT) -> InstallResult:
    """Installa un aggiornamento già selezionato secondo la strategia configurata."""
    if update.strategy == "pip":
        with tempfile.TemporaryDirectory(prefix="python-update-") as temporary_directory:
            wheel_path = download_update(update, Path(temporary_directory), timeout=timeout)
            command = _pip_install_command(wheel_path)
            try:
                completed = subprocess.run(command, check=False)
            except OSError as error:
                raise UpdateInstallationError(f"Cannot start package installer: {error}") from error
        if completed.returncode != 0:
            raise UpdateInstallationError(
                f"Package installer exited with status {completed.returncode}."
            )
        return InstallResult("pip", restart_required=True)

    if update.strategy == "installer":
        if update.platform != "windows" or not update.asset.name.lower().endswith(".exe"):
            raise UpdateConfigurationError(
                "The 'installer' strategy supports Windows .exe installers only."
            )
        update_directory = (
            Path(tempfile.gettempdir())
            / "python-app-updates"
            / update.release.repository.replace("/", "-")
            / str(update.release.version)
        )
        installer_path = download_update(update, update_directory, timeout=timeout)
        try:
            subprocess.Popen([str(installer_path), *update.installer_args], close_fds=True)
        except OSError as error:
            raise UpdateInstallationError(f"Cannot start installer: {error}") from error
        return InstallResult("installer", restart_required=True, downloaded_path=installer_path)

    raise UpdateConfigurationError(f"Unsupported update strategy: {update.strategy!r}.")
