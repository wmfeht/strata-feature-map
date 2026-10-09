---
title: RAR extraction
status: shipped
origin: {issue: lgse/strata#816, pr: lgse/strata#832}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/adapters/local_operations/archive/decoders/rar.rs, src/rar_extraction.rs, src/sandbox/archive.rs, src/sandbox_helper/archive_rar.rs]
tests: [src/adapters/local_operations/archive/decoders/rar/tests.rs, src/rar_extraction/tests.rs, src/sandbox/archive/tests.rs, src/sandbox_helper/archive_rar/tests.rs, tests/fixtures/rar/**]
related: [browser/thumbnails, preview/preview-panel/sandbox]
---

## Summary

Extraction-only support for `.rar` archives through UnRAR, run in a sandboxed helper process. It is an optional `rar` build feature, enabled by default, so packagers can ship Strata without the non-free UnRAR code.

## Behavior

- In a default build, a `.rar` file shows Extract here and Extract to…, and Enter or double-click extracts it. lgse/strata#832
- RAR output follows the same single-root, bundled-folder, and conflict rules as other formats. lgse/strata#1160, lgse/strata#1478
- A RAR with encrypted contents or encrypted headers opens the Extract password dialog; a wrong password reopens it with "Invalid password". lgse/strata#832, lgse/strata#1499
- A corrupt RAR fails with an error and does not open the password dialog. lgse/strata#832 (unverified)
- RAR members get their stored mode and modification time. lgse/strata#1478
- RAR symlink and hard-link members extract as regular files. lgse/strata#1478
- The Compress dialog offers no RAR format. lgse/strata#832
- Cancelling a RAR extraction kills the helper process and reports the operation as cancelled. lgse/strata#1229
- A helper that sends no data for 30 seconds fails the extraction. lgse/strata#1229 (unverified)
- In a build without the `rar` feature, `.rar` files show no Extract actions and activation opens them externally. lgse/strata#1344 (unverified)

## Design

UnRAR's C parser handles attacker-controlled bytes, so it runs outside the main process (lgse/strata#1046, lgse/strata#1229).

- The parent runs `strata --preview-helper extract-rar` in bubblewrap with the archive bound read-only and no writable mount. `prlimit --fsize=0` blocks file writes. Bytes leave only through the child's stdout.
- Members travel over a framed wire protocol, now `STRRAR03`: a header, the declared byte count, then a per-member result. The protocol carries structured password failures and member metadata (lgse/strata#1478, lgse/strata#1499).
- The parent feeds members to the shared extraction session, so destination confinement is the same code as ZIP, TAR, and 7z (lgse/strata#1229).
- UnRAR is called with `RAR_TEST` and null destinations, so it never writes files itself (lgse/strata#1046).
- The child gets a 120 s CPU limit instead of the 10 s preview limit, since bulk extraction is larger than a thumbnail (lgse/strata#1229).
- The child cannot see the cancellation flag, so the parent kills it (lgse/strata#1229).
- The sandbox runs in UTC, so RAR 1.5–4 DOS times are converted in the parent's time zone. `unrar_sys` 0.5.8 misaligns `HeaderDataEx`, so the helper reads mtimes at UnRAR's real offsets behind a compile-time assert (lgse/strata#1478).
- RAR support is a default-on Cargo feature. Distros such as nixpkgs and Debian cannot ship UnRAR as free software; calling an external `unrar` binary was rejected because it complicates the sandbox (lgse/strata#1327, lgse/strata#1344).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-01 | lgse/strata#1344 | feat | Made RAR support an optional, default-on build feature so distros can ship a free build. |
| 2026-09-26 | lgse/strata#1229 | fix | Moved UnRAR decoding into a read-only bubblewrap helper that streams members to the parent. |
| 2026-09-12 | lgse/strata#832 | feat | Added RAR extraction through UnRAR, with password retry and no RAR creation. |

## Known gaps

- RAR symlinks and hard links extract as regular files; the link follow-up from the link extraction work is not done. lgse/strata#1421
