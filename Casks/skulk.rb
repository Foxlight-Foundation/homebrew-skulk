cask "skulk" do
  version "1.5.0"
  sha256 "0f13bdf10c3ea00e9e7f795af988731d5f0f484178968aad5cb3df57f94a2f96"

  url "https://releases.foxlight.ai/desktop/macos/#{version}/2/Skulk-1.5.0-2-macOS-arm64.dmg"
  name "Skulk"
  desc "Desktop operator for Skulk clusters"
  homepage "https://github.com/Foxlight-Foundation/Skulk"

  depends_on arch: :arm64
  depends_on macos: :sequoia

  app "Skulk.app"
end
