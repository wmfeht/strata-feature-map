---
title: In-place update install
status: shipped
origin: {issue: lgse/strata#24, pr: lgse/strata#26}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/services/update_install.rs, src/services/update_install/**, data/update-keys.json, scripts/sign_update_manifest.py]
tests: [src/services/update_install/tests.rs, src/services/update_install/review_tests.rs, src/services/update_install/archive/tests.rs, src/services/update_install/command/tests.rs, src/services/update_install/download/tests.rs, src/services/update_install/manifest/tests.rs, src/ui/settings/tests/update_dialog.rs, scripts/test_sign_update_manifest.py]
docs: [docs/signed-updates.md]
related: [integration/portal-file-chooser]
---

## Summary

Downloading a release, authenticating it against a signed manifest, replacing the running executable, and restarting into it. Applies only to self-managed installs such as `~/.local/bin/strata`; package-managed installs defer to their package manager.

## Behavior

### Starting

- Install update on the Updates row, or Download update in the update dialog, starts the install without a further prompt. lgse/strata#26, lgse/strata#51
- Only one install runs per process; starting another shows "Another install is already running — try again shortly." and leaves its button usable. lgse/strata#97, lgse/strata#1499
- A download location other than `https://github.com/lgse/strata/releases/download/<tag>/strata-<version>-<arch>-unknown-linux-gnu.tar.gz` is refused. lgse/strata#506

### Progress and cancellation

- The row reads "Downloading update… N%", then "Verifying update…", "Installing update…", and "Finalizing update…", with its button reading Cancel. lgse/strata#26, lgse/strata#1499
- Cancel during a download stops it within about a second, shows "Update cancelled", and leaves the installed binary unchanged. lgse/strata#506, lgse/strata#1499
- In the dialog, Cancel, the close button, Escape, and a backdrop click each cancel a running download and close the dialog. lgse/strata#1499
- Once replacement is committed, the dialog shows "Finalizing update…" and cannot be dismissed until the install ends. lgse/strata#1499
- After a failure, cancellation, or completed install, every dialog dismisser closes the dialog. lgse/strata#1499
- A failed install shows "Couldn’t install update:" with the reason, and the dialog's button becomes Close. lgse/strata#506 (unverified)

### Download limits

- A download fails as stalled after 30 seconds to connect, 60 seconds without a response, or 30 seconds without bytes; there is no total time limit. lgse/strata#1499
- An archive larger than its signed size stops with "The update is larger than expected and was not installed"; signed sizes are capped at 128 MiB. lgse/strata#506

### Signed manifest

- Before requesting the archive, Strata downloads the release's `strata-update-manifest.json` and `strata-update-manifest.signatures.json`. lgse/strata#506
- A release without them is refused with "This release has no signed update manifest. Choose a newer release or download it manually." lgse/strata#506
- A manifest with no valid Ed25519 signature from a key embedded in Strata fails with "No trusted release key signed this update manifest". lgse/strata#506
- A manifest over 32 KiB or a signatures file over 8 KiB fails with "The signed update metadata is too large". lgse/strata#506
- A manifest naming another repository or tag, an unknown field, or no artifact for this architecture is refused. lgse/strata#506
- An archive whose size or SHA-256 differs from the manifest is refused before extraction. lgse/strata#506
- A packaged `SOURCE_COMMIT` that differs from the manifest's `source_commit` is refused. lgse/strata#506

### Extraction and replacement

- Archives with links, devices, absolute or `..` paths, over 512 entries, or a second top-level directory are rejected. lgse/strata#506
- The extracted package directory must match the selected asset name, and must contain `strata` and `SOURCE_COMMIT`. lgse/strata#506
- A staged binary failing a 2-second headless probe run fails with "The downloaded update does not run on this system". lgse/strata#506 (unverified)
- The previous binary is kept as `.strata-update-rollback` beside it and restored if the replaced binary fails the same probe. lgse/strata#506
- An install run from an instance whose binary was already replaced writes the install path, not a file named `strata (deleted)`. lgse/strata#1330

### After replacement

- An installed `~/.local/share/applications/io.github.lgse.Strata.desktop` and icon are rewritten from the archive; absent ones are not created. lgse/strata#182
- The rewritten `Exec=` points at the install path, quotes reserved characters, doubles `%`, and keeps the `%U` field code. lgse/strata#182, lgse/strata#672
- When Strata is the opted-in file chooser, its portal is refreshed so the next dialog runs the new binary. lgse/strata#475
- Other Strata windows and chooser processes running the old binary for the same user receive SIGTERM, then SIGKILL after 5 seconds. lgse/strata#1201
- Preview helpers and Strata binaries from other install paths are left running. lgse/strata#1201
- On success the status reads "Update installed — restart to apply", and Strata closes its windows and relaunches the new binary. lgse/strata#26, lgse/strata#1201
- A running file operation that guards closing blocks the restart and shows its close warning. lgse/strata#1519
- If the relaunched binary exits with an error within 20 seconds, the previous binary is restored and launched. lgse/strata#506
- The preserved previous binary is deleted 60 seconds after Strata starts. lgse/strata#506

## Design

[docs/signed-updates.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/signed-updates.md) carries the trust store, manifest format, release signing, key rotation, and limitations.

- A checksum downloaded beside the archive gives integrity, not authenticity (lgse/strata#148). Ed25519 manifests signed in an approval-protected release job replaced it, needing no `gh`, account, or token (lgse/strata#506).
- The signature covers `strata-update-manifest-v1`, a NUL byte, and the exact published bytes; the JSON is never reserialized. Multiple signatures allow overlapping keys during rotation.
- Metadata is authenticated before the archive is requested, and the archive is capped at its signed size. Unsigned releases are refused with no checksum-only or `gh` fallback (lgse/strata#506).
- Extraction runs in process and rejects entry types rather than allowlisting names, so later releases may add files without stranding older updaters (lgse/strata#148).
- Cancellation and commitment settle one atomic state. A cancel that loses the race switches the dialog to Finalizing instead of closing it (lgse/strata#1499).
- A fixed 120-second download limit failed slow but live downloads. Per-wait idle limits replaced it, and cancellation is checked about every second (lgse/strata#1499).
- Every install writes the same executable, so one guard spans all windows. Staging paths are also unique per install against leftovers from a killed process (lgse/strata#97).
- Old instances are found through `/proc` and signalled through a pidfd, so a reused PID is never signalled (lgse/strata#1201).
- Desktop metadata is only refreshed, never created, so an update does not add a launcher the user never installed (lgse/strata#182).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-06 | lgse/strata#1499 | fix | Added the Finalizing phase, dismiss-to-cancel in the dialog, and stall-based download timeouts. |
| 2026-10-05 | lgse/strata#506 | feat | Authenticated updates with signed manifests, bounded extraction, and added cancellation and rollback recovery. |
| 2026-09-29 | lgse/strata#1330 | fix | Resolved a replaced executable's ` (deleted)` path back to its install path before updating. |
| 2026-09-09 | lgse/strata#672 | fix | Escaped the install path in the rewritten desktop `Exec=` line. |
| 2026-09-06 | lgse/strata#475 | fix | Refreshed an opted-in file chooser portal after an in-place update. |
| 2026-08-30 | lgse/strata#26 | feat | Added in-place installation of an available release with checksum verification and restart. |

## Known gaps

None known.
