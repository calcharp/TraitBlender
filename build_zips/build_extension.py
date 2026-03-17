#!/usr/bin/env python3
"""
Build TraitBlender extension zip(s) by calling Blender.

This script works both locally and in CI. It assembles a temporary extension source
directory that includes the addon files, the platform-specific wheels, and a generated
blender_manifest.toml, then runs:

  blender --command extension build --source-dir <temp_dir>
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def _copytree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def build_one(*, blender_exe: str, addon_src_dir: Path, wheels_dir: Path) -> Path:
    if not addon_src_dir.is_dir():
        raise RuntimeError(f"Addon source dir not found: {addon_src_dir}")
    if not wheels_dir.is_dir():
        raise RuntimeError(f"Wheels dir not found: {wheels_dir}")

    with tempfile.TemporaryDirectory(prefix="traitblender_build_") as tmp:
        tmp_root = Path(tmp).resolve()
        build_dir = tmp_root / "build_traitblender"
        _copytree(addon_src_dir, build_dir)

        build_wheels = build_dir / "wheels"
        build_wheels.mkdir(parents=True, exist_ok=True)
        whls = sorted(wheels_dir.glob("*.whl"))
        if not whls:
            raise RuntimeError(f"No wheels found in {wheels_dir}")
        for whl in whls:
            shutil.copy2(whl, build_wheels / whl.name)

        # Generate blender_manifest.toml into build_dir
        gen = Path(__file__).resolve().parent / "generate_manifest.py"
        subprocess.check_call([sys.executable, str(gen), str(build_wheels), "--output", str(build_dir / "blender_manifest.toml")])

        # Build extension zip using Blender
        subprocess.check_call([blender_exe, "--command", "extension", "build", "--source-dir", str(build_dir)])

        # Blender writes the zip into the working directory (or near it). Find the newest zip.
        zips = sorted(tmp_root.rglob("traitblender-*.zip"))
        if not zips:
            # Fallback: search from cwd
            zips = sorted(Path.cwd().rglob("traitblender-*.zip"))
        if not zips:
            raise RuntimeError("Could not find built traitblender-*.zip")

        # Blender writes the zip into cwd; only copy if it was created inside the temp dir.
        out_zip = Path.cwd() / zips[-1].name
        if zips[-1].resolve() != out_zip.resolve():
            shutil.copy2(zips[-1], out_zip)
        return out_zip


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--blender", default="blender", help="Blender executable (default: blender)")
    ap.add_argument("--addon-src", default="TraitBlender", help="Addon source folder to package (default: TraitBlender)")
    ap.add_argument("--wheels", required=True, help="Wheels folder for this OS (e.g. wheels, wheels/mac, wheels/linux)")
    args = ap.parse_args()

    out = build_one(
        blender_exe=args.blender,
        addon_src_dir=Path(args.addon_src).resolve(),
        wheels_dir=Path(args.wheels).resolve(),
    )
    print(out)


if __name__ == "__main__":
    main()

