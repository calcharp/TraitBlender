#!/usr/bin/env python3
"""
Generate blender_manifest.toml from a template and wheels directory.

Usage:
  python build_zips/generate_manifest.py <wheels_dir> [--output <path>]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def package_name_from_wheel(filename: str) -> str:
    """Derive package name from wheel filename (e.g. numpy-2.2.6-cp313-... -> numpy)."""
    stem = Path(filename).stem
    m = re.match(r"^(.+?)-\d", stem)
    return m.group(1) if m else stem.split("-")[0]


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if args else 1)

    wheels_dir = Path(args[0]).resolve()
    if not wheels_dir.is_dir():
        print(f"Error: not a directory: {wheels_dir}", file=sys.stderr)
        sys.exit(1)

    output_path = wheels_dir.parent / "blender_manifest.toml"
    if "--output" in args:
        i = args.index("--output")
        if i + 1 < len(args):
            output_path = Path(args[i + 1]).resolve()
        args = args[:i] + args[i + 2 :]

    whl_files = sorted(wheels_dir.glob("*.whl"))
    if not whl_files:
        print(f"Error: no .whl files in {wheels_dir}", file=sys.stderr)
        sys.exit(1)

    prefix = "./wheels/"
    wheel_paths = [f"{prefix}{f.name}" for f in whl_files]
    dependencies = {package_name_from_wheel(f.name): f"{prefix}{f.name}" for f in whl_files}

    template_path = Path(__file__).resolve().parent / "blender_manifest.template.toml"
    template = template_path.read_text(encoding="utf-8")

    placeholder = "# --- wheels and [dependencies] are injected by generate_manifest.py ---"
    if placeholder not in template:
        print("Error: template missing placeholder line", file=sys.stderr)
        sys.exit(1)

    wheels_block = "wheels = [\n" + "".join(f'  "{p}",\n' for p in wheel_paths) + "]\n\n"
    deps_block = "[dependencies]\n" + "".join(f'{k} = "{v}"\n' for k, v in sorted(dependencies.items()))

    new_content = template.replace(placeholder, wheels_block + "\n" + deps_block)
    output_path.write_text(new_content, encoding="utf-8")
    print(f"Wrote {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

