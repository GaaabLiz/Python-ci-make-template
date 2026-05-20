#!/usr/bin/env python
from __future__ import annotations

import argparse
import io
import struct
import sys
import tomllib
from pathlib import Path

PNG_SIZES = [16, 32, 48, 64, 128, 256, 512, 1024]
JPG_SIZES = [64, 128, 256, 512, 1024]
ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]
ICNS_SIZES = [16, 32, 64, 128, 256, 512, 1024]

ICNS_TYPES: dict[int, bytes] = {
    16: b"icp4",
    32: b"icp5",
    64: b"icp6",
    128: b"ic07",
    256: b"ic08",
    512: b"ic09",
    1024: b"ic10",
}


def generate_project_module(pyproject_path: Path, py_file: Path) -> int:
    try:
        if not pyproject_path.exists():
            raise FileNotFoundError(f"File {pyproject_path} does not exist.")

        with pyproject_path.open("rb") as file_handle:
            data = tomllib.load(file_handle)

        project = data.get("project", {})
        raw_authors = project.get("authors", [])
        authors: list[tuple[str | None, str | None]] = []
        for entry in raw_authors:
            name = entry.get("name")
            email = entry.get("email")
            if name or email:
                authors.append((name, email))

        info = {
            "name": project.get("name"),
            "version": project.get("version"),
            "description": project.get("description"),
            "requires_python": project.get("requires-python"),
            "authors": authors,
        }

        authors_repr = (
            "["
            + ", ".join(f"({repr(name)}, {repr(email)})" for name, email in info["authors"])
            + "]"
        )

        lines = [
            "# fmt: off",
            "name = " + repr(info["name"]),
            "version = " + repr(info["version"]),
            "description = " + repr(info["description"]),
            "requires_python = " + repr(info["requires_python"]),
            "authors = " + authors_repr,
            "# fmt: on",
        ]

        py_file.parent.mkdir(parents=True, exist_ok=True)
        with py_file.open("w", encoding="utf-8") as file_handle:
            file_handle.write("\n".join(lines) + "\n")

        print(f"Generated: {py_file}")
        return 0
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


def _render_svg(svg_path: Path, size: int) -> bytes:
    import skia  # type: ignore[import-untyped]

    svg_bytes = svg_path.read_bytes()
    stream = skia.MemoryStream(svg_bytes)
    svg_dom = skia.SVGDOM.MakeFromStream(stream)
    if svg_dom is None:
        raise RuntimeError(f"Skia could not parse SVG: {svg_path}")

    surface = skia.Surface(size, size)
    with surface as canvas:
        canvas.clear(skia.ColorTRANSPARENT)
        svg_dom.setContainerSize(skia.Size.Make(size, size))
        svg_dom.render(canvas)

    image = surface.makeImageSnapshot()
    png_data = image.encodeToData()
    return bytes(png_data)


def _open_rgba(png_bytes: bytes):
    from PIL import Image  # type: ignore[import-untyped]

    return Image.open(io.BytesIO(png_bytes)).convert("RGBA")


def _resize(base_img, size: int):
    from PIL import Image  # type: ignore[import-untyped]

    return base_img.resize((size, size), Image.LANCZOS)


def _to_png_bytes(img) -> bytes:
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def _build_icns(png_map: dict[int, bytes]) -> bytes:
    body = b""
    for size in sorted(png_map):
        ostype = ICNS_TYPES.get(size)
        if ostype is None:
            continue
        data = png_map[size]
        body += ostype + struct.pack(">I", 8 + len(data)) + data
    return b"icns" + struct.pack(">I", 8 + len(body)) + body


def convert_logo(svg_path: Path) -> int:
    if not svg_path.exists():
        print(f"ERROR: file not found: {svg_path}", file=sys.stderr)
        return 1
    if svg_path.suffix.lower() != ".svg":
        print(f"ERROR: expected a .svg file, got: {svg_path}", file=sys.stderr)
        return 1

    out_dir = svg_path.parent
    stem = svg_path.stem

    print(f"Source : {svg_path}")
    print(f"Output : {out_dir}/")
    print()

    max_size = max(PNG_SIZES + ICNS_SIZES)
    print(f"Rendering SVG at {max_size}x{max_size} px (skia-python) ...")
    base_img = _open_rgba(_render_svg(svg_path, max_size))
    print()

    from PIL import Image as pil_image  # type: ignore[import-untyped]

    print("PNG files:")
    for size in PNG_SIZES:
        img = _resize(base_img, size)
        out_path = out_dir / f"{stem}-{size}x{size}.png"
        img.save(out_path, format="PNG", optimize=True)
        print(f"  {out_path}")
    print()

    print("JPG files:")
    for size in JPG_SIZES:
        rgba = _resize(base_img, size)
        background = pil_image.new("RGB", (size, size), (255, 255, 255))
        background.paste(rgba, mask=rgba.split()[3])
        out_path = out_dir / f"{stem}-{size}x{size}.jpg"
        background.save(out_path, format="JPEG", quality=95, optimize=True)
        print(f"  {out_path}")
    print()

    print("ICO file:")
    ico_images = [_resize(base_img, size) for size in ICO_SIZES]
    ico_path = out_dir / f"{stem}.ico"
    ico_images[0].save(
        ico_path,
        format="ICO",
        sizes=[(size, size) for size in ICO_SIZES],
        append_images=ico_images[1:],
    )
    print(f"  {ico_path}")
    print()

    print("ICNS file:")
    icns_png_map = {size: _to_png_bytes(_resize(base_img, size)) for size in ICNS_SIZES}
    icns_path = out_dir / f"{stem}.icns"
    icns_path.write_bytes(_build_icns(icns_png_map))
    print(f"  {icns_path}")
    print()

    print("Done.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Utility entrypoint for template helper scripts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen_project_py_parser = subparsers.add_parser(
        "gen-project-module",
        help="Generate a Python module from pyproject.toml metadata.",
    )
    gen_project_py_parser.add_argument("pyproject_toml", type=Path)
    gen_project_py_parser.add_argument("output_py", type=Path)
    gen_project_py_parser.set_defaults(
        handler=lambda args: generate_project_module(args.pyproject_toml, args.output_py)
    )

    convert_logo_parser = subparsers.add_parser(
        "convert-logo",
        help="Convert an SVG logo into PNG, JPG, ICO, and ICNS assets.",
    )
    convert_logo_parser.add_argument("svg_path", type=Path)
    convert_logo_parser.set_defaults(handler=lambda args: convert_logo(args.svg_path))

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
