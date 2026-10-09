cask "skulk" do
  version "2.0.2"
  sha256 "fc2426e8b804bded12303e52e8c25795336d7713c4113382af7f11f283f6070e"

  url "https://releases.foxlight.ai/desktop/macos/#{version}/1/Skulk-2.0.2-1-macOS-arm64.dmg"
  name "Skulk"
  desc "Desktop operator for Skulk clusters"
  homepage "https://github.com/Foxlight-Foundation/Skulk"

  depends_on arch: :arm64
  depends_on macos: :sequoia

  app "Skulk.app"

  # The plugin service Skulk registers for the user would otherwise keep
  # retrying a binary that no longer exists after the app is removed.
  uninstall launchctl: "foundation.foxlight.skulk.plugins",
            delete:    "~/Library/LaunchAgents/foundation.foxlight.skulk.plugins.plist"

  zap trash: [
    "~/Library/Application Support/Skulk",
    "~/Library/Logs/Skulk",
  ]
end
