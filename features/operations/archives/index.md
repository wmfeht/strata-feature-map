---
title: Archives
status: shipped
origin: {issue: null, pr: lgse/strata#81}
branch: null
reviewed_at: c94eeb0020fa1154e11c741888f1b56d92ce70d6
review: draft
code: [src/ui/browser/archive.rs, src/adapters/local_operations/archive.rs, src/adapters/local_operations/archive/compression.rs, src/adapters/local_operations/archive/decoders.rs, src/adapters/local_operations/archive/destination.rs, src/adapters/local_operations/archive/extraction.rs]
tests: [src/ui/browser/archive/tests.rs, src/adapters/local_operations/archive/tests.rs, src/adapters/local_operations/archive/fixtures.rs, src/adapters/local_operations/archive/compression/**, src/adapters/local_operations/archive/decoders/tests.rs, src/adapters/local_operations/archive/decoders/fixtures/**, src/adapters/local_operations/archive/destination/tests.rs, src/adapters/local_operations/archive/extraction/tests.rs, src/app/browser/tests/archive_activation.rs, tests/qa/scenarios/archive_activation, tests/qa/scenarios/archive_conflicts, tests/qa/scenarios/archive_errors, tests/qa/scenarios/archive_reveal, tests/qa/fixtures/content-encrypted.7z]
docs: [site/src/reference/archives.md, site/src/reference/keyboard-navigation.md, docs/archives.md]
related: [integration/10xer-mode, operations/progress, operations/trash, operations/filesystem-compatibility]
---

## Summary

Creating ZIP, 7Z, TAR, and TAR.GZ archives from local items, and extracting local archives with Extract here, Extract to…, or by activating them. Covers passwords, name conflicts, extraction safety, and error reporting. Children: `operations/archives/rar` (RAR extraction) and `operations/archives/preview` (browsing an archive's members in the preview).

## Behavior

### Compressing

- Compress… appears in the item menu only when every selected item has a local path. lgse/strata#81 (unverified)
- The Compress dialog subtitle reads "N files" when every item is a file or file link, and "N folders" when every item is a real folder. lgse/strata#81, lgse/strata#1627 (unverified)
- Any other selection, such as a single symlink to a folder, gives the subtitle "N items". lgse/strata#81, lgse/strata#1627 (unverified)
- The Compress dialog offers ZIP, 7Z, TAR.GZ, and TAR, with ZIP selected and the name prefilled with the item's name, or `archive` for several items. lgse/strata#81 (unverified)
- Typing the selected format's extension, such as `backup.zip` with ZIP, creates `backup.zip`, not `backup.zip.zip`. lgse/strata#81 (unverified)
- A name such as `../outside` is rejected in the dialog and nothing is written outside the shown folder. lgse/strata#147
- An archive name the location would store as another, such as `a:b.zip` on vfat, is refused before anything is written. lgse/strata#1615
- Protection (No password / Password protected) shows only for ZIP and 7Z; switching to TAR or TAR.GZ hides it and resets it to No password. lgse/strata#81, lgse/strata#745
- Password protected with an empty password shows "Password required"; differing fields show "Passwords do not match"; no archive is written. lgse/strata#81, lgse/strata#745
- A password-protected 7Z of 4 MiB of zeros packs to hundreds of bytes, like the unprotected one, and lists no member names without the password. lgse/strata#745
- Compressing a symlink stores the link in ZIP and TAR without the target's contents. lgse/strata#407
- Compressing a symlink to 7Z fails with "7z compression does not support symbolic links: <path>. Use ZIP or TAR instead." and leaves no archive. lgse/strata#407
- A file whose name is not valid UTF-8 fails ZIP and 7Z with an error naming it and suggesting TAR; TAR stores the original bytes. lgse/strata#679
- ZIP members store each source's modification time and Unix mode. lgse/strata#1478
- TAR and TAR.GZ store small files from ntfs3, which reports zero blocks for them, in full instead of as zeros. lgse/strata#1615
- 7Z members store each source's Unix mode and its modification, creation, and access times. lgse/strata#1478 (unverified)
- The new archive appears only when encoding finishes, then is selected and scrolled into view in every view mode. lgse/strata#147, lgse/strata#616
- Compression runs as a progress card at the bottom right showing Preparing…, then Compressing… with file counts, and browsing stays available. lgse/strata#981, lgse/strata#1393
- Cancelling compression stops within the current member, then shows the cancellation summary; no partial archive or staging file remains. lgse/strata#410, lgse/strata#981
- The new archive is built in a hidden `.strata-copy-<id>` stage; on SMB without server inode numbers, a cancelled or failed compression removes it too. lgse/strata#1729
- Ctrl+Z after compression moves the new archive to Trash. lgse/strata#1097
- Closing the Compress dialog opened from the item menu with Escape, Cancel, or a backdrop click returns focus to the cursor row. lgse/strata#1533

### Archive name conflicts

- When the archive name exists, a "File already exists" prompt offers Cancel, Keep Both, and Replace, with Replace focused. lgse/strata#147, lgse/strata#986
- Enter activates the focused button; Escape and Cancel leave the existing archive unchanged. lgse/strata#986
- Escape, Cancel, or X on the "File already exists" prompt returns focus to the listed item that was focused before it. lgse/strata#1533
- Keep Both creates the next free numbered name, such as `archive (1).zip` or `archive (1).tar.gz`, and selects it. lgse/strata#986
- Keep Both tries every numbered name, so it succeeds when only the last one is free. lgse/strata#1729
- A long archive name numbered by Keep Both is cut so the number fits the name limit. lgse/strata#1615
- Replace moves the existing archive to Trash before publishing; Ctrl+Z returns it. lgse/strata#1097
- Without Trash, Replace moves the existing archive into a hidden `.strata-originals-<id>` folder, by exchange where supported. It deletes it after the new archive is flushed. lgse/strata#1615, lgse/strata#1729
- Ctrl+Z then has nothing to undo. lgse/strata#1615
- When that original cannot be deleted, compression still completes and reports the folder that keeps it. lgse/strata#1729
- Replace is refused before encoding when no strategy is safe there, and a name taken during replacement keeps the original aside. lgse/strata#1615
- Replace keeps the replaced archive's permission bits on the new archive. lgse/strata#410
- Cancelling, or an encoding failure, during Replace leaves the existing archive in place. lgse/strata#147, lgse/strata#981
- If publishing fails after Replace moved the existing archive, the error says the original is in Trash. lgse/strata#1097 (unverified)

### Extracting

- Extract here and Extract to… appear only for a regular file, or a symlink to one, with a local path and a `.zip`, `.7z`, `.tar`, `.tar.gz`, or `.tgz` extension. lgse/strata#81, lgse/strata#1478
- A folder named `photos.zip` shows no Extract actions and opens like any folder. lgse/strata#1478
- Extract here extracts beside the archive and selects the result; only a folder without a monitor is reloaded for it. lgse/strata#81, lgse/strata#494, lgse/strata#1615
- The extracted result that the browser selects keeps keyboard focus after the progress dialog closes, including in Columns. lgse/strata#1533
- Extract to… opens the floating folder chooser, titled "Extract to", with an "Extract here" button and New Folder. After extraction, the window navigates to the chosen folder and selects the result. lgse/strata#81, lgse/strata#1384
- Cancelling the Extract to… chooser starts no extraction. lgse/strata#1384
- Extracting into a folder reached through a symlink writes into the resolved folder. lgse/strata#678
- Extraction shows Processing archive… with completed-file counts in a foreground progress dialog. lgse/strata#81, lgse/strata#1393 (unverified)
- Ctrl+Z after Extract here or Extract to… completes moves the extracted top-level file or folder to Trash. lgse/strata#1552, lgse/strata#1548
- When extraction published `readme.txt` as `readme (2).txt` beside an existing one, Ctrl+Z trashes only `readme (2).txt`. lgse/strata#1552
- Ctrl+Z after a multi-root extraction moves the one archive-named folder, such as `photos/`, to Trash. lgse/strata#1552
- An extraction that published nothing records no undo entry, so Ctrl+Z undoes the operation before it. lgse/strata#1552
- Ctrl+Z after an extraction started by Enter, double-click, or a password retry also moves its output to Trash. lgse/strata#1552 (unverified)
- Ctrl+Shift+Z after undoing an extraction restores its output from Trash. lgse/strata#1552 (unverified)
- A cancelled or failed extraction records no undo entry, so Ctrl+Z leaves its kept partial output in place. lgse/strata#1552 (unverified)

### Activation

- Enter or double-click on an archive in Icons or List view extracts it as Extract here does, instead of opening an external application. lgse/strata#818, lgse/strata#1160
- In Columns view, Enter on an archive opens its preview; double-click still extracts. lgse/strata#1371
- In the file chooser, activating an archive selects it as a file. lgse/strata#818
- Activating an archive several times creates `stem`, `stem (1)`, `stem (2)` for multi-root archives and never writes into an earlier extraction. lgse/strata#981, lgse/strata#1160

### Extraction output

- A single top-level entry lands in the destination under its own name, or `name (2)`, `name (3)` when that name is taken. lgse/strata#1160, lgse/strata#1478
- A taken single top-level folder such as `strata-1.0.0` publishes as `strata-1.0.0 (2)`; a file or symlink gets the suffix before its extension, `readme (2).txt`. lgse/strata#1617
- An extracted `readme.` beside a taken one becomes `readme. (2)`, not `readme (2).`. lgse/strata#1729
- Several top-level entries land in a folder named after the archive without its extension, such as `photos/` for `photos.zip`, or `photos (1)/` when taken. lgse/strata#1160, lgse/strata#1478
- Entries inside that new folder keep their archive names even when the destination has same-named entries. lgse/strata#1478
- An existing symlink, device, or socket at a top-level name is never followed or replaced; the entry gets a numbered name. lgse/strata#1478
- Members are written into a hidden `.strata-extraction-<id>` folder that shows only when hidden files are shown. lgse/strata#1478
- A failed or cancelled extraction that wrote a file keeps the output in the archive-named folder, and the error ends "Extracted entries remain in “<folder>”." lgse/strata#1478
- A failed extraction that wrote no file leaves nothing behind. lgse/strata#1136, lgse/strata#1478
- On a filesystem without `RENAME_NOREPLACE`, such as an ntfs-3g mount, an extracted single root folder publishes as `name`, then `name (2)` when taken. lgse/strata#1585, lgse/strata#1586
- On such a filesystem, several top-level entries publish in `stem/`, then `stem (1)/` when taken. lgse/strata#1585, lgse/strata#1586
- After such a publication, no `.strata-extraction-<id>` folder remains and the existing same-named folder is untouched. lgse/strata#1585, lgse/strata#1586
- On such a filesystem, a nested read-only folder, such as mode `0555`, publishes with its mode and modification time kept. lgse/strata#1586
- On such a filesystem, a symlink member publishes as a symlink with its stored target. lgse/strata#1586
- Where no placement step can place the output, extraction fails and the members stay in the staging folder. lgse/strata#1615 (unverified)
- The error then ends "Extracted entries remain in “.strata-extraction-<id>”." lgse/strata#1586, lgse/strata#1615 (unverified)
- Cancelling extraction writes no further members, keeps the written ones, and the summary lists completed and pending entries. lgse/strata#410, lgse/strata#1478
- A ZIP, 7Z, or TAR directory entry named `.`, `./`, or `././` is skipped, and the other members extract instead of failing. lgse/strata#494, lgse/strata#1814
- A ZIP directory entry named `.\` is skipped the same way. lgse/strata#1814
- A TAR directory entry named `.\` is skipped the same way. lgse/strata#1814 (unverified)
- A RAR directory entry that names only the archive root is skipped the same way. lgse/strata#1814 (unverified)
- A file member named `.`, or a directory member `../` or `foo/../`, fails with "Refusing empty archive path: <name>" and writes nothing. lgse/strata#1814
- A `git archive` or GitHub tarball extracts without a `pax_global_header` file. lgse/strata#677
- Every member of a solid 7Z archive is extracted. lgse/strata#406

### Member paths, links, and metadata

- A member named `../report.txt` or `folder/../report.txt` extracts as `report.txt` inside the destination, and later members still extract. lgse/strata#1191
- Two members that resolve to `report.txt` extract as `report.txt` and `report (2).txt`. lgse/strata#116, lgse/strata#1191
- An absolute member path or a member written through an existing symlink fails the extraction without writing outside the destination. lgse/strata#116, lgse/strata#1478
- Symlink members are recreated with their stored targets, including absolute ones. lgse/strata#1478
- A TAR hard link links to the earlier member of that name; a hard link to a member not extracted fails the extraction. lgse/strata#1478
- A TAR FIFO or device member fails the extraction with a message naming the member. lgse/strata#1478
- Each member gets its stored mode, masked by the umask with setuid, setgid, and sticky removed, and its stored modification time. lgse/strata#1478
- On FAT and exFAT, modes and times are skipped without error. lgse/strata#1478
- Extracting where member names cannot be stored fixes them by the destination's rules, retrying refused names under stricter rules, and reports each change. lgse/strata#1615
- Folders whose fixed names became one stay apart, such as `10_00 (2)/`. lgse/strata#1615
- Links the destination cannot hold, and hard links to them, are left out and reported, and the extraction finishes. lgse/strata#1615
- Extracted symlink times are not set on FUSE mounts. lgse/strata#1615

### Passwords

- Extracting a password-protected ZIP or 7Z first runs without a password, then opens the Extract password dialog. lgse/strata#81, lgse/strata#1499
- Submitting an empty password keeps the dialog open with "Enter a password". lgse/strata#793
- A wrong password reopens the dialog with "Invalid password", including for plain-header 7Z and ZipCrypto archives whose wrong password fails a checksum. lgse/strata#751, lgse/strata#793, lgse/strata#798
- Cancelling the password dialog after Extract to… leaves nothing in the chosen folder and does not redirect the next completion. lgse/strata#827, lgse/strata#1499
- A wrong password after Extract to… still navigates to the chosen folder once the retried extraction succeeds. lgse/strata#827, lgse/strata#1605
- A password failure discards everything written, so the retry publishes under the archive's plain name instead of `stem (1)`. lgse/strata#1499
- An error that quotes a member name such as `passwords.txt` shows the error dialog, not the password prompt. lgse/strata#750, lgse/strata#1499
- Damage in an unencrypted member is reported as damage even when a password was given. lgse/strata#1499
- Closing the Extract password dialog with Cancel or Escape leaves keyboard focus in the file list. lgse/strata#1533 (unverified)

### Errors and limits

- A text file renamed to `.zip`, or a malformed or truncated archive, fails with "This file is not a valid archive or is damaged." lgse/strata#638
- A `.tar.gz` with a bad CRC32 or length trailer, or non-zero bytes after the last gzip member, fails as damaged; zero padding after it is accepted. lgse/strata#1478, lgse/strata#1499
- A ZIP or 7Z whose declared total exceeds free space at the destination fails before any member is written. lgse/strata#605
- A member that produces more or fewer bytes than its header declares fails the extraction and is not kept. lgse/strata#605
- A highly compressible archive with truthful headers extracts in full; there is no ratio or entry-count cap. lgse/strata#605
- If the item stopped being a regular file after the menu opened, extraction fails with "Not an archive: “<name>”" before creating anything. lgse/strata#1478
- Extract to… accepts a write-only folder, such as mode `0733`, then fails with "Could not open extraction destination: Permission denied". lgse/strata#1729
- After Extract to… fails, such as into a read-only folder, the next Extract here stays in the current folder and selects its output. lgse/strata#864, lgse/strata#1605

## Design

[docs/archives.md](https://github.com/lgse/strata/blob/c94eeb0020fa1154e11c741888f1b56d92ce70d6/docs/archives.md) carries the extraction safety model, output rules, metadata handling, compression policy per format, and cancellation.

- Member paths are untrusted. Writes go through one pinned destination descriptor with `openat2` and per-component `NOFOLLOW`, so traversal names and swapped symlinks cannot escape (lgse/strata#109, lgse/strata#116).
- The destination itself may be reached through ordinary symlinks; it is resolved with `RESOLVE_IN_ROOT` and pinned, as copy and compress already did (lgse/strata#644, lgse/strata#678).
- `..` components are clamped at the destination instead of aborting the whole archive (lgse/strata#1189, lgse/strata#1191).
- Root markers such as `./` are skipped once, in `ExtractionSession::extract_member`, for every decoder; TAR's own check was removed. The skip covers directory members only, so empty-path validation still refuses a file named `.` (lgse/strata#1801, lgse/strata#1814).
- All decoders feed one `ExtractionSession` that owns conflicts, progress, cancellation, and cleanup (lgse/strata#557, lgse/strata#562).
- Extraction stages into a hidden folder and decides single-root or bundled publication after decoding. Bundling after writing into the parent renamed members against the wrong folder and could not clean up failures (lgse/strata#1419, lgse/strata#1471).
- Partial output is kept, not deleted: removing it would mean undoing conflict renames, and the cancel summary already says completed changes stay (lgse/strata#1419).
- Extraction records its undo like compression: one copy entry for the published top-level item under its final name. Undo therefore never trashes a file that was already there (lgse/strata#1548, lgse/strata#1552).
- Every caller extracts into an existing folder, so undo leaves no empty destination behind (lgse/strata#1552).
- Multi-root archives are bundled like Finder. Always wrapping on activation produced `foo/foo/` for tidy archives and was replaced (lgse/strata#894, lgse/strata#1159, lgse/strata#1160).
- Zip bombs are bounded by free space and declared sizes only. Other file managers rely on cancellation, so ratio and entry-count caps were rejected (lgse/strata#479, lgse/strata#605).
- Password retries depend on a structured `PasswordFailure` kind from the decoders, never on message text, which can contain member names (lgse/strata#691, lgse/strata#1499).
- Metadata restoration matches `tar` and `unzip` for a normal user: no owner, group, xattrs, or ACLs; folder metadata applies only on completion so partial output stays writable (lgse/strata#1422).
- Extraction and compression publish through the placement ladder of `operations/filesystem-compatibility`, and compression publishes off the UI thread (lgse/strata#1615).
- Before that, without `RENAME_NOREPLACE`, a folder published by an exclusive `mkdirat` of the name, so `EEXIST` drove the numbering, and files were hard-linked in (lgse/strata#1585, lgse/strata#1586). Staging removal first restores owner access so `0555` folders cannot block it (lgse/strata#1586).
- A single-root conflict name places the suffix as Paste's Keep Both does: a folder takes ` (n)` after its whole name, a file before its extension. The root's type is read without following symlinks, so a symlink is numbered like a file (lgse/strata#1616, lgse/strata#1617).
- Compression writes a mode-0600 staging file beside the target and publishes it atomically without replacing anything; Keep Both retries the finished staging file under new names (lgse/strata#110, lgse/strata#404, lgse/strata#986).
- Payload encoding is chosen per container. Known compressed inputs are stored in ZIP and copied in 7Z; TAR.GZ compresses the whole stream unless every payload is already compressed (lgse/strata#978, lgse/strata#981).
- Compression never follows symlinks, so a selected folder cannot leak files from outside it (lgse/strata#402, lgse/strata#407).
- Cancellation is cooperative inside members. The UI waits for the worker before cleanup, because dropping the GIO task detached it (lgse/strata#403, lgse/strata#413).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-22 | lgse/strata#1814 | fix | Skipped root directory markers such as ZIP's `./` for every decoder, so those archives extract instead of failing. |
| 2026-10-20 | lgse/strata#1729 | fix | Tried every Keep Both number, set replaced archives aside in an originals folder, and removed SMB stages on cancel. |
| 2026-10-15 | lgse/strata#1605 | fix | Dropped the pending navigation when Extract to… fails, so the next extraction stays put. |
| 2026-10-14 | lgse/strata#1617 | fix | Numbered a taken single-root folder after its whole name, so `strata-1.0.0` becomes `strata-1.0.0 (2)`, not `strata-1.0 (2).0`. |
| 2026-10-12 | lgse/strata#1586 | fix | Published extracted folders on filesystems without `RENAME_NOREPLACE`, such as ntfs-3g, instead of leaving them in staging. |
| 2026-10-11 | lgse/strata#1552 | fix | Recorded the published extraction output for undo, so Ctrl+Z trashes it and never a pre-existing file. |
| 2026-10-09 | lgse/strata#1533 | fix | Returned focus to the opener after the Compress, Extract password, and archive conflict dialogs close, including on Escape. |
| 2026-10-05 | lgse/strata#1478 | fix | Staged extraction, kept partial output in the archive folder, restored links and metadata, and gated Extract on regular files. |
| 2026-09-23 | lgse/strata#1160 | feat | Bundled multi-root extractions under the archive stem for every entry point, like Finder. |
| 2026-09-23 | lgse/strata#1136 | fix | Removed the empty subfolder left by a failed activation extraction. |
| 2026-09-23 | lgse/strata#1191 | fix | Clamped `..` member paths inside the destination instead of aborting extraction. |
| 2026-09-14 | lgse/strata#986 | feat | Added Keep Both to archive name conflicts. |
| 2026-09-14 | lgse/strata#981 | perf | Chose compression per container, showed Preparing…, and cancelled compression inside members. |
| 2026-09-12 | lgse/strata#897 | fix | Extracted activated archives into a subfolder named after the archive. |
| 2026-09-11 | lgse/strata#750 | fix | Stopped member names containing "password" from opening the password prompt. |
| 2026-09-11 | lgse/strata#827 | fix | Dropped the pending navigation and empty folder when the Extract to… password prompt is cancelled. |
| 2026-09-11 | lgse/strata#818 | feat | Extracted archives on Enter and double-click instead of opening them externally. |
| 2026-09-11 | lgse/strata#798 | fix | Treated ZipCrypto checksum failures after a supplied password as a wrong password. |
| 2026-09-10 | lgse/strata#793 | fix | Kept the extract password dialog open on empty input and reopened it on a wrong password. |
| 2026-09-10 | lgse/strata#783 | fix | Replaced raw 7z password error names with sentences and re-armed the password retry. |
| 2026-09-10 | lgse/strata#751 | fix | Treated a wrong password on content-encrypted 7z as retryable instead of damage. |
| 2026-09-10 | lgse/strata#745 | fix | Compressed before encrypting in password-protected 7z archives. |
| 2026-09-09 | lgse/strata#616 | fix | Scrolled the new archive into view after compression in every view mode. |
| 2026-09-09 | lgse/strata#679 | fix | Refused non-UTF-8 names in ZIP and 7z instead of mangling them. |
| 2026-09-09 | lgse/strata#677 | fix | Skipped pax global headers when extracting TAR. |
| 2026-09-09 | lgse/strata#678 | fix | Allowed extracting into a folder reached through a symlink. |
| 2026-09-09 | lgse/strata#638 | fix | Replaced raw decoder errors with "not a valid archive or is damaged". |
| 2026-09-09 | lgse/strata#605 | fix | Bounded extraction by destination free space and declared member sizes. |
| 2026-09-07 | lgse/strata#562 | refactor | Shared one extraction session across the ZIP, TAR, and 7z decoders. |
| 2026-09-07 | lgse/strata#547 | refactor | Moved archive operations and dialogs into their own modules. |
| 2026-09-07 | lgse/strata#494 | fix | Skipped the `./` root entry when extracting TAR. |
| 2026-09-06 | lgse/strata#410 | fix | Made compression staging private and extraction cancellable. |
| 2026-09-06 | lgse/strata#407 | fix | Stopped following symlinks during compression. |
| 2026-09-06 | lgse/strata#406 | fix | Extracted every member of solid 7z archives. |
| 2026-09-01 | lgse/strata#147 | fix | Validated archive names and published compression output atomically after a Replace prompt. |
| 2026-09-01 | lgse/strata#116 | fix | Confined extraction to the destination with descriptor-relative writes. |
| 2026-09-01 | lgse/strata#81 | feat | Added compression to ZIP, 7z, TAR.GZ, and TAR and extraction with Extract here and Extract to…. |

## Known gaps

- There is no option to delete the archive after a successful extraction. lgse/strata#759
