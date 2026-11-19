"""Generate WinGet manifests for the verified Windows installer."""

import json
from collections.abc import Mapping
from hashlib import file_digest
from pathlib import Path


def quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def generate_manifests(version: str, settings: Mapping[str, str]) -> int:
    installer_file_name = settings["CI_WINGET_INSTALLER_FILE"]
    installer_path = Path(installer_file_name)
    if not installer_path.is_file():
        print(
            f"Error: installer not found at {installer_file_name}. "
            "Run make ci-build-winget-assets first."
        )
        return 1

    package_identifier = settings["CI_WINGET_PACKAGE_IDENTIFIER"]
    package_name = settings["CI_WINGET_PACKAGE_NAME"]
    publisher = settings["CI_WINGET_PUBLISHER"]
    package_locale = settings["CI_WINGET_PACKAGE_LOCALE"]
    short_description = settings["CI_WINGET_SHORT_DESCRIPTION"]
    license_name = settings["CI_WINGET_LICENSE"]
    license_url = settings["CI_WINGET_LICENSE_URL"]
    homepage = settings["CI_WINGET_HOMEPAGE"]
    installer_type = settings["CI_WINGET_INSTALLER_TYPE"]
    installer_arch = settings["CI_WINGET_INSTALLER_ARCHITECTURE"]
    manifest_version = settings["CI_WINGET_MANIFEST_VERSION"]
    tags = settings["CI_WINGET_TAGS"].split()
    installer_url = settings["CI_WINGET_INSTALLER_URL"].replace("{version}", version)

    publisher_from_id, application_from_id = package_identifier.split(".", 1)
    root = (
        Path("dist")
        / "winget"
        / "manifests"
        / publisher_from_id[0].lower()
        / publisher_from_id
        / application_from_id
        / version
    )
    root.mkdir(parents=True, exist_ok=True)
    with installer_path.open("rb") as installer_file:
        installer_sha = file_digest(installer_file, "sha256").hexdigest().upper()
    version_lines = [
        f"# yaml-language-server: $schema=https://aka.ms/winget-manifest.version.{manifest_version}.schema.json",
        f"PackageIdentifier: {quote(package_identifier)}",
        f"PackageVersion: {quote(version)}",
        f"DefaultLocale: {quote(package_locale)}",
        'ManifestType: "version"',
        f"ManifestVersion: {quote(manifest_version)}",
    ]
    default_locale_lines = [
        f"# yaml-language-server: $schema=https://aka.ms/winget-manifest.defaultLocale.{manifest_version}.schema.json",
        f"PackageIdentifier: {quote(package_identifier)}",
        f"PackageVersion: {quote(version)}",
        f"PackageLocale: {quote(package_locale)}",
        f"Publisher: {quote(publisher)}",
        f"PackageName: {quote(package_name)}",
        f"ShortDescription: {quote(short_description)}",
        f"License: {quote(license_name)}",
        f"LicenseUrl: {quote(license_url)}",
        f"PublisherUrl: {quote(homepage)}",
        f"PackageUrl: {quote(homepage)}",
    ]
    if tags:
        default_locale_lines.append("Tags:")
        default_locale_lines.extend(f"- {quote(tag)}" for tag in tags)
    default_locale_lines.extend(
        [
            'ManifestType: "defaultLocale"',
            f"ManifestVersion: {quote(manifest_version)}",
        ]
    )
    installer_lines = [
        f"# yaml-language-server: $schema=https://aka.ms/winget-manifest.installer.{manifest_version}.schema.json",
        f"PackageIdentifier: {quote(package_identifier)}",
        f"PackageVersion: {quote(version)}",
        "Installers:",
        f"- Architecture: {quote(installer_arch)}",
        f"  InstallerType: {quote(installer_type)}",
        f"  InstallerUrl: {quote(installer_url)}",
        f"  InstallerSha256: {quote(installer_sha)}",
        f"  InstallerLocale: {quote(package_locale)}",
        'ManifestType: "installer"',
        f"ManifestVersion: {quote(manifest_version)}",
    ]
    (root / f"{package_identifier}.yaml").write_text(
        "\n".join(version_lines) + "\n", encoding="utf-8"
    )
    (root / f"{package_identifier}.locale.{package_locale}.yaml").write_text(
        "\n".join(default_locale_lines) + "\n", encoding="utf-8"
    )
    (root / f"{package_identifier}.installer.yaml").write_text(
        "\n".join(installer_lines) + "\n", encoding="utf-8"
    )
    print(f"Generated WinGet manifests in {root}")
    return 0
