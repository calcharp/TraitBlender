#!/usr/bin/env python3
"""
Generate blender_manifest.toml from the template and the wheels in a given directory.
Usage: python generate_manifest.py <wheels_dir> [--output <path>]
  wheels_dir: directory containing .whl files (e.g. build_dir/wheels)
  --output: where to write the manifest (default: wheels_dir/../blender_manifest.toml)
"""
import re
import sys
from pathlib import Path


def package_name_from_wheel(filename: str) -> str:
    """Derive PEP 503 package name from wheel filename (e.g. numpy-2.2.6-cp311-... -> numpy)."""
    stem = Path(filename).stem
    # Version starts at first -<digit>; name is everything before that.
    m = re.match(r"^(.+?)-\d", stem)
    return m.group(1) if m else stem.split("-")[0]


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if not args else 1)

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

    # Paths relative to the manifest (same dir as wheels/ = parent of wheels_dir)
    prefix = "./wheels/"
    wheel_paths = [f"{prefix}{f.name}" for f in whl_files]
    dependencies = {
        package_name_from_wheel(f.name): f"{prefix}{f.name}" for f in whl_files
    }

    template_path = Path(__file__).resolve().parent / "blender_manifest.template.toml"
    template = template_path.read_text()

    # Find insertion point: after website line, before [permissions]
    placeholder = "# --- wheels and [dependencies] are injected by generate_manifest.py ---"
    if placeholder not in template:
        print("Error: template missing placeholder line", file=sys.stderr)
        sys.exit(1)

    wheels_block = "wheels = [\n"
    wheels_block += "".join(f'  "{p}",\n' for p in wheel_paths)
    wheels_block += "]\n\n"
    deps_block = "[dependencies]\n"
    deps_block += "".join(f'{k} = "{v}"\n' for k, v in sorted(dependencies.items()))

    new_content = template.replace(
        placeholder,
        wheels_block + "\n" + deps_block,
    )

    output_path.write_text(new_content, encoding="utf-8")
    print(f"Wrote {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
