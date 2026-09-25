#!/usr/bin/env python3
"""Merge this repository's iTerm2 preferences into the local preference domain."""

import argparse
import plistlib
import subprocess
import tempfile
from pathlib import Path


DOMAIN = "com.googlecode.iterm2"
SOURCE = Path(__file__).resolve().parent / "preferences.plist"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="report the import without changing preferences")
    parser.add_argument("--output", type=Path, help="write the merged plist here instead of importing it")
    args = parser.parse_args()

    tracked = plistlib.loads(SOURCE.read_bytes())
    result = subprocess.run(["defaults", "export", DOMAIN, "-"], capture_output=True)
    if result.returncode:
        current = {}
    else:
        current = plistlib.loads(result.stdout)
    merged = {**current, **tracked}
    data = plistlib.dumps(merged, fmt=plistlib.FMT_XML, sort_keys=True)
    print(f"Current keys: {len(current)}; tracked keys: {len(tracked)}; merged keys: {len(merged)}")
    print(f"Profiles to restore: {', '.join(p.get('Name', '<unnamed>') for p in tracked.get('New Bookmarks', []))}")

    if args.dry_run:
        return
    if args.output:
        args.output.write_bytes(data)
        print(f"Wrote {args.output}")
        return

    if current:
        backup = Path.home() / "Library/Preferences/com.googlecode.iterm2.plist.iterm2-setup.bak"
        if not backup.exists():
            backup.write_bytes(plistlib.dumps(current, fmt=plistlib.FMT_XML, sort_keys=True))
            print(f"Backed up existing preferences to {backup}")
    with tempfile.TemporaryDirectory() as directory:
        merged_file = Path(directory) / "com.googlecode.iterm2.plist"
        merged_file.write_bytes(data)
        subprocess.run(["defaults", "import", DOMAIN, str(merged_file)], check=True)
    print("Preferences imported. Launch iTerm2 to use them.")


if __name__ == "__main__":
    main()
