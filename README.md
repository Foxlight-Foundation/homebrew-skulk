# Foxlight Homebrew tap

This is the official Homebrew tap for the Skulk desktop application and the
recommended Skulk installation path on supported Macs.

## Install Skulk

```bash
brew install --cask Foxlight-Foundation/skulk/skulk
```

The cask installs the signed and notarized Skulk app on Apple Silicon Macs
running macOS 15 or newer. The application includes the exact coordinated
Skulk runtime, dashboard, and native components for its release, so a separate
Skulk source checkout, Python environment, or Node.js installation is not
required.

Open **Skulk** from Applications and select **Start Skulk**. The menu-bar app
shows runtime readiness and provides controls for the dashboard, logs, node
lifecycle, and an optional custom cluster namespace.

## Upgrade Skulk

```bash
brew upgrade --cask Foxlight-Foundation/skulk/skulk
```

Homebrew is the update channel for the current app. In-app update notification
can be added later; the app does not presently update itself.

Each coordinated Skulk release validates the public stable manifest and opens
a cask update pull request in this tap. Tap CI audits and styles the proposed
cask before it is merged. A scheduled reconciler provides a fallback if the
release-triggered update is interrupted; neither path bypasses review.

## Uninstall Skulk

```bash
brew uninstall --cask skulk
```

For Ubuntu and Debian packages, headless Linux, source/development installs,
and forming a multi-node cluster, see the public
[Skulk installation guide](https://foxlight-foundation.github.io/Skulk/install/).

Release artifacts are hosted at
[releases.foxlight.ai](https://releases.foxlight.ai/desktop/macos/latest.json).
