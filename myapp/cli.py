"""Minimal command-line entry point for the sample application."""

import argparse

from myapp.core import add
from myapp.project import version


def main() -> None:
    parser = argparse.ArgumentParser(description="Small example application for the template.")
    parser.add_argument("--version", action="version", version=version)
    parser.parse_args()
    print(f"2 + 3 = {add(2, 3)}")


if __name__ == "__main__":
    main()
