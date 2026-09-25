# iTerm2 setup

This repository captures my portable iTerm2 preferences and zsh setup: the
customized Default profile, colors, keyboard mappings, pointer actions,
`.zshrc`, `.zprofile`, and the Powerlevel10k prompt settings. The XML property
list and shell files can be reviewed and versioned in Git.

## Set up a new Mac

1. Install iTerm2 and launch it once.
2. Quit iTerm2, clone this repository, and run:

   ```sh
   cd iterm2-setup
   python3 restore.py --dry-run
   python3 restore.py
   python3 restore-shell.py --dry-run
   python3 restore-shell.py
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

The shell restore copies the three files in `shell/` to your home directory.
It saves a one-time `.iterm2-setup.bak` copy of any existing dotfile before
replacing it. To test against another directory, use `--home /path/to/home`.
Install Homebrew, Oh My Zsh, Powerlevel10k, `zsh-autosuggestions`, and
`zsh-syntax-highlighting` before opening a new shell. The current shell files
also reference Java 24, asdf, and Homebrew packages under `/opt/homebrew`;
adjust those paths if the new Mac uses a different setup.

## Refresh this repository

After changing iTerm2 preferences on this Mac, quit iTerm2 and run
`python3 export.py`. Review the resulting `preferences.plist` before committing.
The export includes an explicit list of preference keys and removes the
machine's home path from a profile that uses the default working directory.
After changing a shell dotfile, copy its new version into `shell/` and review
the diff before committing.

The repo excludes `com.googlecode.iterm2.private.plist`, saved sessions,
window positions, recent history, installation identifiers, and other local
state. It does not include account credentials.
