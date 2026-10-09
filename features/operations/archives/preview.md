---
title: Archive preview
status: shipped
origin: {issue: lgse/strata#1151, pr: lgse/strata#1090}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: draft
code: [src/ui/preview/archive.rs, src/adapters/local_operations/archive/listing.rs]
tests: [src/adapters/local_operations/archive/listing/tests.rs, tests/e2e/scenarios/test_archive_preview.py]
docs: [docs/keyboard-navigation.md]
related: [preview/preview-panel, preview/preview-panel/sandbox, preview/quick-preview, integration/10xer-mode]
---

## Summary

Browsing a local ZIP, 7z, TAR, or TAR.GZ archive's member tree in the preview, like a read-only folder, without extracting anything. Listing runs in the preview sandbox and reads metadata only.

## Behavior

### Listing

- Previewing a `.zip`, `.7z`, `.tar`, `.tar.gz`, or `.tgz` shows its members as a folder tree starting at "Contents", with folder names ending in `/`. lgse/strata#1090 (unverified)
- Each folder lists its subfolders first, then its files, each in case-insensitive name order. lgse/strata#1090 (unverified)
- File rows show their size; folder rows show a chevron and open on a single click. lgse/strata#1090 (unverified)
- A breadcrumb row starts at "Contents"; clicking a crumb, or the back arrow "Go up one level", returns to that level. lgse/strata#1090 (unverified)
- An empty archive folder shows "This folder is empty". lgse/strata#1090 (unverified)
- Previewing an archive never writes files to disk or opens member files. lgse/strata#1090, lgse/strata#1343
- An encrypted ZIP or a 7z with encrypted headers shows "Password-protected archive" with a password field and Unlock button. lgse/strata#1090
- A wrong password keeps the prompt open with "The password is incorrect."; the correct password shows the member tree. lgse/strata#1090
- A 7z with readable headers and encrypted contents lists its members without a password. lgse/strata#1090
- A malformed or truncated archive shows "Preview unavailable" with "This file is not a valid archive or is damaged." lgse/strata#1090 (unverified)
- A ZIP with duplicate member names shows "This archive format is not supported for preview." instead of a partial tree. lgse/strata#1090
- An archive with more than 20,000 entries, or a TAR.GZ over 1 GiB compressed or decompressed, shows "Archive too large to preview." lgse/strata#1090 (unverified)
- A member name over 16 KiB or 4,096 path levels also shows "Archive too large to preview." lgse/strata#1090 (unverified)

### Keyboard

- With the preview closed, Space on an archive opens it with the first member highlighted and focused. lgse/strata#1192
- Inside the preview, Up/Down move the highlight, Right and Enter open a folder, and Left goes to the parent. lgse/strata#1192
- With Type to search off, h, j, k, and l act as Left, Down, Up, and Right inside the preview. lgse/strata#1192 (unverified)
- Right or Enter on a member file does nothing. lgse/strata#1343
- Space inside the archive tree closes the preview. lgse/strata#1192 (unverified)
- Keyboard movement never reaches the Close Preview button or F1, and only the current member is outlined. lgse/strata#1203
- In List and Columns, Right from the listing enters an open archive preview. lgse/strata#1343
- Left at the archive root returns focus to the listing without closing the preview; Up/Down then move through listing items. lgse/strata#1343
- In Columns, another Left from the listing moves to the parent column. lgse/strata#1343
- While the preview owns focus, its header shows the accent top border instead of the Miller column. lgse/strata#1343
- In Columns, moving onto an archive shows its contents with no member selected, and Up/Down keep moving through the column. lgse/strata#1371
- In Columns, Right, Enter, or Space on the archive enters the preview and selects its first member, even with automatic previews off. lgse/strata#1371
- Escape from an entered archive preview in Columns closes the preview and returns focus to the archive in the parent column. lgse/strata#1371
- Closing the preview leaves the archive selected in the listing. lgse/strata#1192

## Design

Quick Look reads metadata only, so it needs neither extraction to a temporary folder nor an external archive manager (lgse/strata#1151).

- Listing parses untrusted input inside the preview sandbox, with cancellation. Passwords stay out of paths, arguments, and diagnostics (lgse/strata#1151, lgse/strata#1090).
- Entry count, name length, path depth, and total name bytes are bounded on both sides of the sandbox. Entry counts alone do not bound the memory of synthesized parent folders (lgse/strata#1090).
- The `zip` crate silently collapses duplicate names, so such ZIPs are refused rather than shown incomplete (lgse/strata#1151).
- Rows are virtualized, since eager widgets stalled large archives (lgse/strata#1090).
- In Columns, an archive preview stays passive until entered. Taking the arrow keys on selection interrupted column navigation (lgse/strata#1369, lgse/strata#1371).
- Left at the root follows 10xer's existing `h` behavior instead of being swallowed (lgse/strata#1334).
- RAR is not listed: UnRAR runs only for explicit extraction (lgse/strata#1046).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-02 | lgse/strata#1371 | fix | Kept Columns archive previews passive until entered with Right, Enter, or Space. |
| 2026-10-01 | lgse/strata#1343 | fix | Returned Left at the archive root to the listing and routed arrows by pane focus. |
| 2026-09-23 | lgse/strata#1203 | fix | Fixed stale highlights and stopped keyboard movement reaching Close Preview or F1. |
| 2026-09-23 | lgse/strata#1192 | feat | Added arrow and h/j/k/l navigation inside the archive preview. |
| 2026-09-19 | lgse/strata#1090 | feat | Added a sandboxed, metadata-only archive tree preview for ZIP, 7z, TAR, and TAR.GZ. |

## Known gaps

None known.
