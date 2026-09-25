#!/usr/bin/env python3
"""Copy the tracked zsh configuration into a home directory."""

import argparse
import shutil
from pathlib import Path


SOURCE = Path(__file__).resolve().parent / "shell"
FILES = (".zprofile", ".zshrc", ".p10k.zsh")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="show changes without copying files")
    parser.add_argument("--home", type=Path, default=Path.home(), help="destination home directory")
    args = parser.parse_args()
    home = args.home.expanduser()
    if not home.is_dir():
        parser.error(f"home directory does not exist: {home}")

    for name in FILES:
        source = SOURCE / name
        destination = home / name
        if destination.exists() and destination.read_bytes() == source.read_bytes():
            print(f"unchanged {destination}")
            continue
        print(f"{'would copy' if args.dry_run else 'copying'} {source} -> {destination}")
        if args.dry_run:
            continue
        backup = home / f"{name}.iterm2-setup.bak"
        if destination.exists() and not backup.exists():
            shutil.copy2(destination, backup)
            print(f"backed up {destination} -> {backup}")
        shutil.copy2(source, destination)


if __name__ == "__main__":
    main()
