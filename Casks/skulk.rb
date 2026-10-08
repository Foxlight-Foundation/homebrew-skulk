cask "skulk" do
  version "2.0.0"
  sha256 "9006e3b5b305a4603c9b9a5af5db098d4cdb9a0a8f784a5dbd7a36634e9a04ad"

  url "https://releases.foxlight.ai/desktop/macos/#{version}/1/Skulk-2.0.0-1-macOS-arm64.dmg"
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
