#!/usr/bin/env python3
"""Refresh the portable iTerm2 preferences from this Mac."""

import plistlib
from pathlib import Path


DOMAIN = Path.home() / "Library/Preferences/com.googlecode.iterm2.plist"
OUTPUT = Path(__file__).resolve().parent / "preferences.plist"

# Explicitly include user configuration. Omit NoSync*, NS*, SU*, the private
# preference domain, installation IDs, window geometry, and recent state.
KEYS = (
    "AIFeatureFunctionCalling",
    "AIFeatureHostedCodeInterpeter",
    "AIFeatureHostedFileSearch",
    "AIFeatureHostedWebSearch",
    "AIFeatureStreamingResponses",
    "AITermAPI",
    "AIVectorStore",
    "AiMaxTokens",
    "AiModel",
    "AiResponseMaxTokens",
    "AitermURL",
    "ApplePressAndHoldEnabled",
    "Custom Color Presets",
    "Default Bookmark Guid",
    "EnableDivisionView",
    "HapticFeedbackForEsc",
    "New Bookmarks",
    "PointerActions",
    "PreventEscapeSequenceFromClearingHistory",
    "ShowFullScreenTabBar",
    "SoundForEsc",
    "TabStyleWithAutomaticOption",
    "UseBorder",
    "VisualIndicatorForEsc",
)


def main():
    current = plistlib.loads(DOMAIN.read_bytes())
    settings = {key: current[key] for key in KEYS if key in current}
    for profile in settings.get("New Bookmarks", []):
        # iTerm ignores this field when Custom Directory is "No". A home path
        # from this machine would be wrong on a future laptop.
        if profile.get("Custom Directory") == "No":
            profile.pop("Working Directory", None)
    OUTPUT.write_bytes(plistlib.dumps(settings, fmt=plistlib.FMT_XML, sort_keys=True))
    print(f"Exported {len(settings)} preference keys to {OUTPUT}")


if __name__ == "__main__":
    main()
