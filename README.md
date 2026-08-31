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

Each coordinated Skulk release asks this tap to validate the public stable
manifest, push a deterministic cask branch, and run the tap's audit and style
checks. After that validation succeeds, the desktop release coordinator opens
a normal pull request with its narrowly scoped automation token. A scheduled
reconciler can stage and validate the same deterministic branch if the
release-triggered update is interrupted; a coordinator or maintainer must
still open the pull request. Neither path bypasses review.

## Uninstall Skulk

```bash
brew uninstall --cask skulk
```

For Ubuntu and Debian packages, headless Linux, source/development installs,
and forming a multi-node cluster, see the public
[Skulk installation guide](https://foxlight-foundation.github.io/Skulk/install/).

Release artifacts are hosted at
[releases.foxlight.ai](https://releases.foxlight.ai/desktop/macos/latest.json).
