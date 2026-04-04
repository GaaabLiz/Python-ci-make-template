"""Entrypoint CLI minimale per i test PyInstaller."""

from myapp.core import add


def main() -> None:
    print(f"2 + 3 = {add(2, 3)}")


if __name__ == "__main__":
    main()
