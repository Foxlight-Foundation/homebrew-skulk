cask "skulk" do
  version "1.5.1"
  sha256 "ca707109e83ca229146a02652cfc96c8ea5831a835d811ba008b470eb9b01aa0"

  url "https://releases.foxlight.ai/desktop/macos/#{version}/3/Skulk-1.5.1-3-macOS-arm64.dmg",
      verified: "releases.foxlight.ai/"
  name "Skulk"
  desc "Desktop operator for Skulk clusters"
  homepage "https://github.com/Foxlight-Foundation/Skulk"

  depends_on arch: :arm64
  depends_on macos: :sequoia

  app "Skulk.app"
end
