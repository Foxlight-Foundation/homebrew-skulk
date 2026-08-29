"""Contract tests for release-manifest-driven cask updates."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


class UpdateCaskTests(unittest.TestCase):
    """Exercise the updater without contacting the public release host."""

    def _manifest(self) -> dict[str, object]:
        version = "1.6.0"
        bundle_version = 3
        release_root = f"https://releases.foxlight.ai/desktop/macos/{version}/{bundle_version}"
        return {
            "schema_version": 1,
            "channel": "stable",
            "version": version,
            "bundle_version": bundle_version,
            "desktop_commit": "a" * 40,
            "skulk_commit": "b" * 40,
            "homebrew_cask_url": f"{release_root}/homebrew/Casks/skulk.rb",
            "artifacts": [
                {
                    "kind": "dmg",
                    "architecture": "arm64",
                    "filename": "Skulk-1.6.0-3-macOS-arm64.dmg",
                    "sha256": "c" * 64,
                    "url": f"{release_root}/Skulk-1.6.0-3-macOS-arm64.dmg",
                }
            ],
        }

    def _run(self, manifest: dict[str, object], *extra_arguments: str) -> subprocess.CompletedProcess[str]:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            manifest_path = temporary_root / "latest.json"
            cask_path = temporary_root / "skulk.rb"
            output_path = temporary_root / "github-output"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = subprocess.run(
                [
                    "python3",
                    str(root / "scripts/update_cask.py"),
                    "--manifest-file",
                    str(manifest_path),
                    "--cask",
                    str(cask_path),
                    "--github-output",
                    str(output_path),
                    *extra_arguments,
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            result.cask = cask_path.read_text(encoding="utf-8") if cask_path.exists() else ""  # type: ignore[attr-defined]
            result.workflow_output = output_path.read_text(encoding="utf-8") if output_path.exists() else ""  # type: ignore[attr-defined]
            return result

    def test_renders_verified_cask_from_exact_release_identity(self) -> None:
        """A valid manifest must produce a pinned, verified cask and outputs."""
        result = self._run(
            self._manifest(),
            "--expected-version",
            "1.6.0",
            "--expected-bundle-version",
            "3",
            "--expected-skulk-commit",
            "b" * 40,
            "--expected-desktop-commit",
            "a" * 40,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('version "1.6.0"', result.cask)  # type: ignore[attr-defined]
        self.assertIn('sha256 "' + ("c" * 64) + '"', result.cask)  # type: ignore[attr-defined]
        self.assertIn('verified: "releases.foxlight.ai/"', result.cask)  # type: ignore[attr-defined]
        self.assertIn("bundle_version=3", result.workflow_output)  # type: ignore[attr-defined]
        self.assertIn("changed=true", result.workflow_output)  # type: ignore[attr-defined]

    def test_rejects_noncanonical_artifact_url(self) -> None:
        """An attacker-controlled or malformed disk-image URL must fail closed."""
        manifest = self._manifest()
        artifacts = manifest["artifacts"]
        assert isinstance(artifacts, list)
        assert isinstance(artifacts[0], dict)
        artifacts[0]["url"] = "https://example.invalid/Skulk.dmg"
        result = self._run(manifest)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("canonical release path", result.stderr)

    def test_rejects_release_expectation_mismatch(self) -> None:
        """A coordinator pin that differs from the manifest must fail closed."""
        result = self._run(self._manifest(), "--expected-version", "1.6.1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected version", result.stderr)


if __name__ == "__main__":
    unittest.main()
