# iTerm2 setup

This repository captures my portable iTerm2 preferences: the customized
Default profile, colors, keyboard mappings, pointer actions, appearance, and
other app settings. `preferences.plist` is an XML property list so it can be
reviewed and versioned in Git.

## Set up a new Mac

1. Install iTerm2 and launch it once.
2. Quit iTerm2, clone this repository, and run:

   ```sh
   cd iterm2-setup
   python3 restore.py --dry-run
   python3 restore.py
   ```

`restore.py` merges the tracked keys into the current preference domain with
macOS `defaults import`. It saves a one-time backup of existing preferences at
`~/Library/Preferences/com.googlecode.iterm2.plist.iterm2-setup.bak` before
importing. Quit iTerm2 first so it does not overwrite the restored settings
when it exits. The tracked Default profile replaces the destination's profile
list. To inspect the merged plist without importing, run
`python3 restore.py --output /tmp/iterm2-merged.plist`.

The profile uses MesloLGL Nerd Font at 14 points. Install that font separately
for the intended appearance. Its semantic history editor is VS Code, so
install VS Code to use that action.

## Refresh this repository

After changing iTerm2 preferences on this Mac, quit iTerm2 and run
`python3 export.py`. Review the resulting `preferences.plist` before committing.
The export includes an explicit list of preference keys and removes the
machine's home path from a profile that uses the default working directory.

The repo excludes `com.googlecode.iterm2.private.plist`, saved sessions,
window positions, recent history, installation identifiers, and other local
state. It does not include account credentials.
