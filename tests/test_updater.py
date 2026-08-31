import hashlib
import io
import subprocess
from pathlib import Path

import pytest

from myapp import updater

REPOSITORY_URL = "https://github.com/acme/example"
ASSET_CONTENT = b"wheel-content"


def _asset(name: str = "example-1.2.0-py3-none-any.whl") -> dict[str, object]:
    return {
        "name": name,
        "browser_download_url": (
            f"https://github.com/acme/example/releases/download/v1.2.0/{name}"
        ),
        "size": len(ASSET_CONTENT),
        "digest": f"sha256:{hashlib.sha256(ASSET_CONTENT).hexdigest()}",
    }


def _release_payload(
    *,
    tag: str = "v1.2.0",
    assets: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "tag_name": tag,
        "html_url": f"https://github.com/acme/example/releases/tag/{tag}",
        "assets": [_asset()] if assets is None else assets,
    }


def _config() -> dict[str, object]:
    return {
        "strategies": {"default": "pip"},
        "asset-patterns": {"default": "example-*.whl"},
    }


def test_parse_public_github_repository() -> None:
    assert updater.parse_public_github_repository(f"{REPOSITORY_URL}.git/") == "acme/example"


@pytest.mark.parametrize(
    "repository_url",
    [
        "http://github.com/acme/example",
        "https://gitlab.com/acme/example",
        "https://github.com/acme/example/releases",
        "git@github.com:acme/example.git",
    ],
)
def test_rejects_non_public_github_url(repository_url: str) -> None:
    with pytest.raises(updater.UpdateConfigurationError):
        updater.parse_public_github_repository(repository_url)


def test_check_for_update_selects_configured_asset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(updater, "_request_json", lambda _url, _timeout: _release_payload())

    available = updater.check_for_update(
        REPOSITORY_URL,
        "1.1.0",
        _config(),
        platform_name="linux",
    )

    assert available is not None
    assert str(available.release.version) == "1.2.0"
    assert available.asset.name == "example-1.2.0-py3-none-any.whl"
    assert available.strategy == "pip"


def test_check_for_update_returns_none_for_current_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        updater,
        "_request_json",
        lambda _url, _timeout: _release_payload(assets=[]),
    )

    assert (
        updater.check_for_update(
            REPOSITORY_URL,
            "1.2.0",
            _config(),
            platform_name="linux",
        )
        is None
    )


def test_check_for_update_rejects_ambiguous_assets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        updater,
        "_request_json",
        lambda _url, _timeout: _release_payload(assets=[_asset(), _asset()]),
    )

    with pytest.raises(updater.UpdateConfigurationError, match="matched 2 assets"):
        updater.check_for_update(
            REPOSITORY_URL,
            "1.1.0",
            _config(),
            platform_name="linux",
        )


def test_download_update_verifies_digest(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(updater, "_request_json", lambda _url, _timeout: _release_payload())
    monkeypatch.setattr(
        updater,
        "_open_url",
        lambda _request, _timeout: io.BytesIO(ASSET_CONTENT),
    )
    available = updater.check_for_update(
        REPOSITORY_URL,
        "1.1.0",
        _config(),
        platform_name="linux",
    )
    assert available is not None

    downloaded = updater.download_update(available, tmp_path)

    assert downloaded.read_bytes() == ASSET_CONTENT


def test_download_update_rejects_digest_mismatch(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    bad_asset = _asset()
    bad_asset["digest"] = f"sha256:{'0' * 64}"
    monkeypatch.setattr(
        updater,
        "_request_json",
        lambda _url, _timeout: _release_payload(assets=[bad_asset]),
    )
    monkeypatch.setattr(
        updater,
        "_open_url",
        lambda _request, _timeout: io.BytesIO(ASSET_CONTENT),
    )
    available = updater.check_for_update(
        REPOSITORY_URL,
        "1.1.0",
        _config(),
        platform_name="linux",
    )
    assert available is not None

    with pytest.raises(updater.UpdateIntegrityError, match="SHA-256"):
        updater.download_update(available, tmp_path)


def test_install_update_runs_package_installer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(updater, "_request_json", lambda _url, _timeout: _release_payload())
    available = updater.check_for_update(
        REPOSITORY_URL,
        "1.1.0",
        _config(),
        platform_name="linux",
    )
    assert available is not None
    commands: list[list[str]] = []

    def fake_download(update, destination: Path, *, timeout: float) -> Path:
        return destination / update.asset.name

    def fake_run(command: list[str], *, check: bool) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(updater, "download_update", fake_download)
    monkeypatch.setattr(
        updater,
        "_pip_install_command",
        lambda wheel_path: ["package-installer", str(wheel_path)],
    )
    monkeypatch.setattr(updater.subprocess, "run", fake_run)

    result = updater.install_update(available)

    assert result == updater.InstallResult("pip", restart_required=True)
    assert commands[0][0] == "package-installer"
    assert commands[0][1].endswith(available.asset.name)


def test_install_update_launches_windows_installer(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    installer_asset = _asset("example-setup.exe")
    monkeypatch.setattr(
        updater,
        "_request_json",
        lambda _url, _timeout: _release_payload(assets=[installer_asset]),
    )
    config = {
        "strategies": {"windows": "installer"},
        "asset-patterns": {"windows": "example-setup.exe"},
    }
    available = updater.check_for_update(
        REPOSITORY_URL,
        "1.1.0",
        config,
        platform_name="win32",
    )
    assert available is not None
    installer_path = tmp_path / "example-setup.exe"
    commands: list[list[str]] = []

    monkeypatch.setattr(
        updater,
        "download_update",
        lambda _update, _destination, *, timeout: installer_path,
    )

    def fake_popen(command: list[str], *, close_fds: bool) -> None:
        commands.append(command)

    monkeypatch.setattr(updater.subprocess, "Popen", fake_popen)

    result = updater.install_update(available)

    assert result.downloaded_path == installer_path
    assert commands == [[str(installer_path), *updater.DEFAULT_INSTALLER_ARGS]]
