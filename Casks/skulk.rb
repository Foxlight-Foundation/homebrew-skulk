cask "skulk" do
  version "2.0.1"
  sha256 "462df7b35aa2c6d394919b34ada1e26b05443857c27b9f5fab2dab7da8488ba6"

  url "https://releases.foxlight.ai/desktop/macos/#{version}/7/Skulk-2.0.1-7-macOS-arm64.dmg"
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
