"""Entrypoint CLI minimale con supporto agli aggiornamenti."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from myapp.core import add
from myapp.project import version
from myapp.updater import UpdateError, check_configured_update, install_update


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=version)
    subparsers = parser.add_subparsers(dest="command")
    update_parser = subparsers.add_parser("update", help="Check the latest public GitHub release.")
    update_parser.add_argument(
        "--install",
        action="store_true",
        help="Download, verify, and install the available update.",
    )
    return parser


def _run_update(should_install: bool) -> int:
    try:
        available = check_configured_update()
        if available is None:
            print(f"Already up to date ({version}).")
            return 0

        print(
            f"Update {available.current_version} -> {available.release.version}: "
            f"{available.release.page_url}"
        )
        if not should_install:
            print("Run again with --install to install it.")
            return 0

        result = install_update(available)
        print(f"Update installed with {result.strategy}; restart the application.")
        return 0
    except UpdateError as error:
        print(f"Update failed: {error}", file=sys.stderr)
        return 2


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.command == "update":
        return _run_update(args.install)
    print(f"2 + 3 = {add(2, 3)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
