#!/usr/bin/env python3
"""Update the Skulk cask from the signed-release publication manifest."""

from __future__ import annotations

import argparse
import json
import re
import urllib.request
from pathlib import Path
from typing import Any

CANONICAL_RELEASE_ROOT = "https://releases.foxlight.ai/desktop/macos"
DEFAULT_MANIFEST_URL = f"{CANONICAL_RELEASE_ROOT}/latest.json"
FULL_COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
STABLE_VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def _read_manifest(manifest_file: Path | None, manifest_url: str) -> dict[str, Any]:
    """Load one release manifest from a local test fixture or public HTTPS."""
    if manifest_file is not None:
        raw_manifest = manifest_file.read_bytes()
    else:
        request = urllib.request.Request(
            manifest_url,
            headers={"User-Agent": "Foxlight-Homebrew-Cask-Updater/1"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
            raw_manifest = response.read()
    parsed = json.loads(raw_manifest)
    if not isinstance(parsed, dict):
        raise ValueError("The release manifest must be a JSON object.")
    return parsed


def _required_string(manifest: dict[str, Any], key: str) -> str:
    """Return a required non-empty string from a release manifest."""
    value = manifest.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Manifest field {key!r} must be a non-empty string.")
    return value


def _validated_release(manifest: dict[str, Any]) -> tuple[str, int, str, str, str]:
    """Validate stable-release identity and return cask rendering inputs."""
    if manifest.get("schema_version") != 1 or manifest.get("channel") != "stable":
        raise ValueError("The cask can only follow a schema-v1 stable release.")

    version = _required_string(manifest, "version")
    if STABLE_VERSION_PATTERN.fullmatch(version) is None:
        raise ValueError("The release version must be stable X.Y.Z.")

    bundle_version = manifest.get("bundle_version")
    if not isinstance(bundle_version, int) or isinstance(bundle_version, bool) or bundle_version < 1:
        raise ValueError("The bundle version must be a positive integer.")

    desktop_commit = _required_string(manifest, "desktop_commit")
    skulk_commit = _required_string(manifest, "skulk_commit")
    if FULL_COMMIT_PATTERN.fullmatch(desktop_commit) is None:
        raise ValueError("The desktop commit must be a full lowercase Git commit.")
    if FULL_COMMIT_PATTERN.fullmatch(skulk_commit) is None:
        raise ValueError("The Skulk commit must be a full lowercase Git commit.")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("The release manifest must contain an artifacts list.")
    disk_images = [
        artifact
        for artifact in artifacts
        if isinstance(artifact, dict)
        and artifact.get("kind") == "dmg"
        and artifact.get("architecture") == "arm64"
    ]
    if len(disk_images) != 1:
        raise ValueError("The release must contain exactly one arm64 disk image.")

    disk_image = disk_images[0]
    sha256 = disk_image.get("sha256")
    if not isinstance(sha256, str) or re.fullmatch(r"[0-9a-f]{64}", sha256) is None:
        raise ValueError("The disk image must have a lowercase SHA-256 digest.")
    filename = f"Skulk-{version}-{bundle_version}-macOS-arm64.dmg"
    expected_url = f"{CANONICAL_RELEASE_ROOT}/{version}/{bundle_version}/{filename}"
    if disk_image.get("filename") != filename or disk_image.get("url") != expected_url:
        raise ValueError("The disk-image identity does not match the canonical release path.")
    expected_cask_url = (
        f"{CANONICAL_RELEASE_ROOT}/{version}/{bundle_version}/homebrew/Casks/skulk.rb"
    )
    if manifest.get("homebrew_cask_url") != expected_cask_url:
        raise ValueError("The release manifest has a non-canonical cask URL.")

    return version, bundle_version, sha256, desktop_commit, skulk_commit


def _render_cask(version: str, bundle_version: int, sha256: str) -> str:
    """Render the canonical first-party Skulk cask."""
    return f'''cask "skulk" do
  version "{version}"
  sha256 "{sha256}"

  url "https://releases.foxlight.ai/desktop/macos/#{{version}}/{bundle_version}/Skulk-{version}-{bundle_version}-macOS-arm64.dmg",
      verified: "releases.foxlight.ai/"
  name "Skulk"
  desc "Desktop operator for Skulk clusters"
  homepage "https://github.com/Foxlight-Foundation/Skulk"

  depends_on arch: :arm64
  depends_on macos: :sequoia

  app "Skulk.app"
end
'''


def main() -> int:
    """Validate a public release manifest and reconcile the checked-in cask."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-url", default=DEFAULT_MANIFEST_URL)
    parser.add_argument("--manifest-file", type=Path)
    parser.add_argument("--cask", type=Path, default=Path("Casks/skulk.rb"))
    parser.add_argument("--expected-version")
    parser.add_argument("--expected-bundle-version", type=int)
    parser.add_argument("--expected-skulk-commit")
    parser.add_argument("--expected-desktop-commit")
    parser.add_argument("--github-output", type=Path)
    arguments = parser.parse_args()

    manifest = _read_manifest(arguments.manifest_file, arguments.manifest_url)
    version, bundle_version, sha256, desktop_commit, skulk_commit = _validated_release(manifest)
    expectations = (
        ("version", arguments.expected_version, version),
        ("bundle version", arguments.expected_bundle_version, bundle_version),
        ("Skulk commit", arguments.expected_skulk_commit, skulk_commit),
        ("desktop commit", arguments.expected_desktop_commit, desktop_commit),
    )
    for label, expected, actual in expectations:
        if expected is not None and expected != actual:
            raise ValueError(f"The expected {label} does not match the release manifest.")

    rendered_cask = _render_cask(version, bundle_version, sha256)
    current_cask = arguments.cask.read_text(encoding="utf-8") if arguments.cask.exists() else ""
    changed = current_cask != rendered_cask
    if changed:
        arguments.cask.parent.mkdir(parents=True, exist_ok=True)
        arguments.cask.write_text(rendered_cask, encoding="utf-8")

    if arguments.github_output is not None:
        with arguments.github_output.open("a", encoding="utf-8") as output:
            output.write(f"version={version}\n")
            output.write(f"bundle_version={bundle_version}\n")
            output.write(f"desktop_commit={desktop_commit}\n")
            output.write(f"skulk_commit={skulk_commit}\n")
            output.write(f"changed={'true' if changed else 'false'}\n")
    print(f"Skulk cask {version} ({bundle_version}) is {'updated' if changed else 'current'}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
