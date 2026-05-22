#!/usr/bin/env python3
"""
Download pinned cp313 wheels for TraitBlender extension builds.

Run on the target OS (Windows, macOS, or Linux) with Python 3.13:

  py -3.13 build_zips/download_wheels.py windows
  py -3.13 build_zips/download_wheels.py mac
  py -3.13 build_zips/download_wheels.py linux
  py -3.13 build_zips/download_wheels.py linux-headless

Then regenerate the manifest (or run build_extension.py, which does this):

  py -3.13 build_zips/generate_manifest.py traitblender/wheels --output traitblender/blender_manifest.toml
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

PLATFORM_DIRS: dict[str, Path] = {
    "windows": REPO_ROOT / "traitblender" / "wheels",
    "mac": REPO_ROOT / "wheels" / "mac",
    "linux": REPO_ROOT / "wheels" / "linux",
    "linux-headless": REPO_ROOT / "wheels" / "linux-headless",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Download TraitBlender wheels for one platform.")
    parser.add_argument(
        "platform",
        choices=sorted(PLATFORM_DIRS),
        help="Target platform folder to populate",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Use requirements-wheels-headless.txt (no dearpygui). "
        "Ignored when platform is linux-headless (always headless).",
    )
    args = parser.parse_args()

    wheels_dir = PLATFORM_DIRS[args.platform]
    wheels_dir.mkdir(parents=True, exist_ok=True)

    use_headless = args.platform == "linux-headless" or args.headless
    req_file = (
        REPO_ROOT / "requirements-wheels-headless.txt"
        if use_headless
        else REPO_ROOT / "requirements-wheels.txt"
    )

    for whl in wheels_dir.glob("*.whl"):
        whl.unlink()

    cmd = [
        sys.executable,
        "-m",
        "pip",
        "download",
        "--only-binary=:all:",
        "--no-deps",
        "-r",
        str(req_file),
        "-d",
        str(wheels_dir),
    ]
    print(f"Downloading wheels for {args.platform} into {wheels_dir} ...")
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    whls = sorted(wheels_dir.glob("*.whl"))
    print(f"Downloaded {len(whls)} wheel(s):")
    for whl in whls:
        print(f"  {whl.name}")

    if args.platform == "windows":
        gen = REPO_ROOT / "build_zips" / "generate_manifest.py"
        manifest = REPO_ROOT / "traitblender" / "blender_manifest.toml"
        subprocess.check_call([sys.executable, str(gen), str(wheels_dir), "--output", str(manifest)])
        print(f"Updated {manifest}")


if __name__ == "__main__":
    main()
