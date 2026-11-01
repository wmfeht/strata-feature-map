---
nodes: [operations/archives, operations/archives/rar, operations/progress, operations/progress/dock, integration/10xer-mode/file-verbs, devices/volumes/drive-dialogs]
reviewed_at: be3343a5992a2a5497b1a2ee7faa525be18e988f
---

# Archives

## Extraction safety

<!-- node: operations/archives -->

Archive member paths are untrusted metadata. If an extractor joined a selected
folder with `../report.txt` unchanged, the filesystem would resolve the result
beside that folder instead of inside it. This archive path-traversal pattern is
also known as Zip Slip.

Strata resolves parent components without allowing them to walk above the
selected destination. For example, both `../report.txt` and
`folder/../report.txt` become `report.txt`. Extraction then continues with later
members instead of aborting the entire operation. Backslashes count as path
separators, so `..\report.txt` also becomes `report.txt`.

A directory entry that names only the archive root, such as `.`, `./`,
`././`, or `.\`, is skipped in every format, RAR included, and the other
members extract. An empty or absolute path fails the extraction with
"Refusing unsafe archive path: \<name>", and nothing is written outside the
destination. So does a drive prefix, a letter and a colon such as `C:`, as the
first component left after `.` is skipped and `..` resolved: `C:marker`,
`./c:notes`, and `safe/../c:notes` are all refused. A colon in a later
component is an ordinary name, so a ZIP holding `before.txt`, `names/c:notes`,
and `after.txt` extracts all three onto a destination that allows `:`, such as
ext4. Any other path that resolves to nothing fails the extraction with
"Refusing empty archive path: \<name>". Examples are a file
or link named `.`, and a directory named `../` or `folder/..`.

The sanitized path still passes through the descriptor-relative destination
writer, which refuses symlink traversal. Normal conflict renaming also applies,
so two members that sanitize to `report.txt` become `report.txt` and
`report (2).txt` rather than overwriting one another.

### Names the destination cannot store

Member names follow the rules of the destination's mount, as the names a copy
brings there do. On a FAT or exFAT drive, for example, characters it cannot
store become `_`, trailing dots and spaces are dropped, device names Windows
reserves get `_`, and names too long for it are shortened. The folder named
after the archive follows the same rules. A member whose name the destination
still refuses, a symbolic link included, is retried under stricter rules. A
member gets the next number when an earlier member's fixed name took its name,
so `10_00/` after `10:00/` on a USB stick becomes `10_00 (2)/`, and different
folders of the archive never merge. Numbers follow archive order, and each
member lands in the folder its own folder became.

When the extraction ends, a report lists every name the destination changed,
grouped by cause, such as "The destination doesn’t allow these names", each as
"“\<name>” was saved as “\<new name>”". It also lists every symbolic link left
out. After a failure or cancellation, it lists those inside the folder that
keeps the output.

### Destination folder

A destination reached through a symlink receives the output in the resolved
folder. **Extract to…** checks the chosen folder off the interface thread and,
like **Copy to…** and **Move to…**, accepts a folder you may write into but not
list, such as a mode `0733` drop box owned by another user. Extracting into one
fails with "Could not open extraction destination: Permission denied", because
the extractor reads the names the destination already holds.

## Extraction output

<!-- node: operations/archives, Extraction output -->
<!-- node: operations/archives, Passwords -->
<!-- node: operations/archives, Errors and limits -->
<!-- node: operations/archives, Extracting -->

Strata writes members into a hidden `.strata-extraction-<id>` folder inside the
destination, created when the first member is written. It is visible during
extraction only when hidden files are shown. A crash or an unplugged device can
leave it behind. It holds nothing the archive does not, and the folder's
**Items left by an interrupted operation** header button offers to delete it.
When the archive has been read, Strata publishes the folder:

- A single top-level entry is moved up into the destination under its own
  name. It is numbered only if the destination already has an entry with that
  name, including a symlink or special file, which is never followed or
  replaced. A folder takes the number after its whole name, so
  `strata-1.0.0` becomes `strata-1.0.0 (2)`. A file or symlink takes it before
  its extension, `readme (2).txt`, and `readme.` becomes `readme. (2)`.
- Several top-level entries stay together in a folder named after the archive
  without its extension, such as `photos/` for `photos.zip`. If that name is
  taken, the folder becomes `photos (1)/`, `photos (2)/` and so on. Entries
  inside the folder keep the archive's names, even when the destination
  already has an entry with the same name; only duplicates within the archive,
  and names the destination cannot store, are renamed.
- If extraction fails or is cancelled after writing a file, everything written
  so far stays in the archive-named folder, even if it is a single entry. The
  error message ends with `Extracted entries remain in “<folder>”.`, and the
  "Operation cancelled" dialog counts the entries completed, failed, and not
  attempted.
  If no file was written, any folders created along the way are removed and
  nothing is left behind.
- If extraction stops because a password is missing or incorrect, everything
  written so far is discarded, including members that were not encrypted.
  The password prompt extracts the whole archive again, so the retry lands
  under the archive's own name instead of `photos (1)/`. Damage in a member
  that is not encrypted is reported as damage, even when a password was
  given. If the output cannot be removed, the failure is reported like any
  other, with the reason and the folder that keeps the output, and no password
  prompt opens.

Publication never replaces an existing entry. On a filesystem without atomic
no-replace renames, such as an ntfs-3g mount, the result is the same: a single
root folder publishes as `name`, then `name (2)` when taken, and several
top-level entries publish in `photos/`, then `photos (1)/`. There a file is
published through a hard link, and a folder is moved whole over an empty
placeholder Strata has just created. Where a file cannot be hard-linked, as on
sshfs and vboxsf, it is renamed over an empty file Strata has just created and
checked. Where hard links are unusable, a folder that cannot be moved over a
placeholder is renamed once its name is found free, as is a folder whose name
ntfs-3g would cut. Symlinks keep their stored targets, and a read-only folder
such as mode `0555` keeps its mode and modification time. The existing
same-named folder is untouched, and no `.strata-extraction-<id>` folder
remains. Where none of these steps can place an entry, extraction fails, the
members stay in the staging folder, and the error ends with
`Extracted entries remain in “.strata-extraction-<id>”.`

Partial output from any other failed attempt stays in its own folder, so a
retry never merges into it. An archive with several top-level entries is
extracted into the next numbered folder; a single entry lands in the
destination under its own name, as usual.

`.tar.gz` archives are read to the end of the gzip stream, including every
member of a multi-member file such as concatenated `.gz` output, so each
member's CRC32 and length trailer is verified. A mismatch or a truncated trailer is
reported as a damaged archive. Zero bytes after the last member, as tape
blocking or `dd` leave them, are padding rather than damage; any other
trailing bytes are reported as a damaged archive. Members already written are
kept as described above, but their contents are unverified.

A `./` root entry is skipped (see [Extraction safety](#extraction-safety)). A
`git archive` or GitHub tarball extracts without a `pax_global_header` file.
Every member of a solid 7Z archive is extracted.

### Damaged and oversized archives

A text file renamed to `.zip`, or a malformed or truncated archive, fails with
"This file is not a valid archive or is damaged." A ZIP or 7Z whose declared
total size exceeds the destination's free space fails before any member is
written. A member that produces more or fewer bytes than its header declares
fails the extraction and is not kept. There is no compression-ratio or
entry-count cap: a highly compressible archive with truthful headers extracts
in full.

### Undo

Ctrl+Z after a completed extraction, whether it started from **Extract here**,
**Extract to…**, Enter, double-click, or a password retry, moves the published
output to Trash: the single top-level file or folder, or the one archive-named
folder such as `photos/`. Only what the extraction published goes: if
`readme.txt` was published as `readme (2).txt` beside an existing one, only
`readme (2).txt` is trashed. Ctrl+Shift+Z after that undo restores the output
from Trash. An extraction that published nothing, failed, or was cancelled
records no undo entry, so Ctrl+Z undoes the operation before it and leaves any
kept partial output in place.

## Links, permissions and times

<!-- node: operations/archives -->
<!-- node: operations/archives/rar -->

Symbolic links are recreated with their stored targets, including absolute
targets and targets outside the archive, and are never followed by later
members: a member under a link name fails instead of writing through the link.
TAR names and hard-link targets retain their native bytes where the destination
stores them. Hard links become links to the member of that name extracted
earlier from the same archive, following any conflict rename or fixed name, so
a hard link to `names/c:notes` links to that extracted member. A hard link to a
member that was not extracted, or that appears later, fails the extraction. A TAR FIFO or
device member fails the extraction with "Archive member “\<name>” is a FIFO and
cannot be extracted" or "… is a device and cannot be extracted". An existing symlink at a member's name, such as an
earlier link member with the same name, is skipped like a file: the member is
renamed to `name (2)`.

Each member gets its stored permission bits, masked by the umask, with setuid,
setgid and sticky bits removed, and its stored modification time. ZIP times
come from the Info-ZIP extended timestamp, then the NTFS field, then the DOS
time read as local time. Members without a stored mode keep the default
permissions. Folder permissions and times are applied only when extraction
completes, so partial output from a failed or cancelled extraction stays
writable. A folder listed more than once in the archive is restored once:
each of its permissions and time comes from the last entry that stores it.
Folders created only as parents of other members keep default
permissions. Owner, group, access times, extended attributes and ACLs are not
restored. RAR archives restore permissions and times, but a member archived
without Unix mode bits, such as one made on Windows, keeps the default
permissions, and link members still extract as regular files.

On filesystems that cannot store Unix permissions or times, such as FAT and
exFAT, those are skipped without an error, as `tar` and `unzip` do. A symbolic
link's own time is best effort, and is never set on FUSE mounts, where daemons
such as sshfs apply it to the target.

Symbolic links the destination cannot hold, and hard links to them, are left
out and listed in the report, and the extraction goes on. A TAR hard link the
destination cannot hold, as on vfat, exFAT, exfat-fuse, or an SMB mount without
hard links, becomes a copy of its target, and later members still extract. The
copy takes space of its own and gets the member's stored mode and modification
time. A hard link the mount refuses for another reason, such as no space or an
I/O error, still fails the extraction with "Could not link “\<member>” to
“\<target>”: \<reason>". So does a mount without hard links where the target
cannot be reopened for the copy; the reason is then the reopen failure. Where
the mount holds symbolic links but not hard links, such as sshfs without its
hardlink extension, a hard link to an extracted symbolic link fails the
extraction.

## Extraction targets

<!-- node: operations/archives, Extracting -->
<!-- node: operations/archives, Activation -->
<!-- node: operations/archives, Passwords -->
<!-- node: operations/archives, Errors and limits -->
<!-- node: integration/10xer-mode/file-verbs -->
<!-- node: operations/archives/rar -->

**Extract here** and **Extract to…** in the item context menu, the 10xer `; e`
and `; E` chords, and extraction on Enter or double-click apply only to a
regular file, or a symlink to one, with a local path and a `.zip`, `.7z`,
`.tar`, `.tar.gz`, `.tgz`, or `.rar` extension, in any letter case. A folder
named `photos.zip` opens like any other folder and offers no Extract actions.
FIFOs, sockets, devices, and broken links named like archives are not
extracted either. In Icons and List views, Enter or double-click opens them
externally. In Columns, Enter opens the preview for one with a ZIP, 7Z, TAR,
or TAR.GZ name, and double-click opens it externally. The chords report "Not
an archive".

If the item changes between opening the menu and running the action, the
operation layer checks the path again. A path that exists but is not a regular
file fails with `Not an archive: “<name>”` before any destination folder is
created.

### Extract here and Extract to…

**Extract here** extracts beside the archive and selects the result; the
folder is reloaded only when Strata cannot watch it for changes. The selected
result keeps keyboard focus after the progress dialog closes, including in
Columns. **Extract to…** opens a floating folder chooser titled "Extract to",
with an **Extract here** button and **New Folder**. After extraction, the
window navigates to the chosen folder and selects the result. Cancelling the
chooser starts no extraction. After **Extract to…** fails, such as into a
read-only folder, the next **Extract here** stays in the current folder and
selects its output. So does one run after cancelling a foreground
**Move to…**.

### Enter and double-click

In Icons and List views, Enter or double-click on an archive extracts it as
**Extract here** does, instead of opening an external application. In Columns,
Enter on a ZIP, 7Z, TAR, or TAR.GZ archive opens its preview; Enter on a RAR
archive extracts it, and double-click extracts any archive. In the
file chooser, activating an archive selects it as a file. Activating the same
archive again never writes into an earlier extraction.

### 10xer mode

In 10xer mode, `; c` opens the Compress dialog for the targets. If any target
has no local path, it flashes "Can’t compress these items", and an empty folder
flashes "Nothing to compress". `; e` extracts
one archive beside itself and selects the result, and `; E` extracts it to a
folder typed at the `extract to ›` prompt. Unlike **Extract to…**, `; E`
leaves the window in the current folder. The prompt chooses and checks a
folder as `move to ›` and `copy to ›` do; see [Files](10xer-mode.md#files) and
[Folder picker](10xer-mode.md#folder-picker) in 10xer mode. With several targets, `; e` and
`; E` flash "Extract one archive at a time". With one target that is not an
archive, such as `notes.txt` or a folder named `photos.zip`, they flash "Not an
archive". With no target, as in an empty folder, they flash "Nothing to
extract".

### Passwords

Extracting a password-protected ZIP, 7Z, or RAR first runs without a password,
then opens a password dialog titled **Extract** with the archive's name.
Submitting an empty password keeps the dialog open with "Enter a password". A
wrong password reopens it with "Invalid password", including for plain-header
7Z and ZipCrypto archives. After **Extract to…**, a retry that succeeds still
navigates to the chosen folder. Cancelling the dialog after **Extract to…** leaves
nothing in the chosen folder, and the next extraction does not navigate there.
Closing the dialog with Cancel or Escape leaves keyboard focus in the file
list. A click outside the dialog closes it like Cancel only while the password
field is empty; once you have typed a password, a click outside leaves it open.

Only a failure that the decoder reports as a missing or incorrect password
opens the password prompt, with "Invalid password" for an incorrect one. The
wording of an error message never decides it, so a member or archive name
containing "password" cannot open the prompt.

### RAR

RAR archives extract like the other formats, with the same output and
conflict rules. Encrypted contents or encrypted headers open the password
dialog, and a damaged unencrypted RAR fails with "This file is not a valid
archive or is damaged." without a prompt. Cancelling a RAR extraction stops it
at once and reports it as cancelled. Extraction fails if the decoder sends no
data for 30 seconds, if a member continues into another volume of a
multi-volume RAR ("The next RAR volume is missing"), or if the archive's
dictionary exceeds the decoder's memory limit ("RAR dictionary exceeds the
decoder's memory limit"). Official release builds and AUR builds include RAR extraction. A build made without RAR support shows no Extract actions for
`.rar` files, and Enter or double-click opens them externally.

## Archive creation

<!-- node: operations/archives, Compressing -->
<!-- node: operations/archives/rar -->

**Compress…** appears in the item menu only when every selected item has a
local path. The Compress dialog offers ZIP, 7Z, TAR.GZ, and TAR, with ZIP
selected and the name prefilled with the item's name, or `archive` for several
items. Typing the selected format's extension, such as `backup.zip` with ZIP,
creates `backup.zip`, not `backup.zip.zip`. A name such as `../outside` is
rejected in the dialog, and nothing is written outside the shown folder. A name
the location would store as another, such as `a:b.zip` on vfat, is refused
before anything is written. The dialog's subtitle reads "N files" when every
item is a file or a link to one, "N folders" when every item is a real folder,
and "N items" otherwise, so a single symlink to a folder reads "1 item".
**Protection** (No password / Password protected) shows only for ZIP and 7Z;
switching to TAR or TAR.GZ hides it and resets it to No password. Password
protected with an empty password shows "Password required", and fields that
differ show "Passwords do not match"; no archive is written. The fields are
labelled, for screen readers too, "Archive name" and, with Password protected
chosen, "Password" and "Confirm password".

The new archive appears only when encoding finishes. If you have not navigated
away from the folder where you started and no other operation has started
since, it is then selected and scrolled into view in every view mode. Ctrl+Z after compression moves the new
archive to Trash. Closing the Compress dialog opened from the item menu with
Escape or Cancel returns focus to the cursor row. A click outside closes it the
same way only while the name is still the default and both password fields are
empty; otherwise a click outside leaves the dialog open.

Strata chooses compression according to the output container, not just the
selected filename extension.

| Output | Payload encoding | Password support |
| --- | --- | --- |
| ZIP | Stored for known already-compressed members; DEFLATE level 6 for other files | AES-256 for either method; filenames remain visible |
| 7Z | Copy for known already-compressed members; LZMA2 level 6 for other files | AES-256 for both methods, plus encrypted headers |
| TAR | No compression | None |
| TAR.GZ | One gzip member containing the entire TAR stream; stored DEFLATE blocks when all regular-file payloads are known already-compressed, otherwise default gzip compression | None |
| RAR | Extraction only | No RAR creation |

A password-protected 7Z is compressed before it is encrypted, so it is about as
small as an unprotected one, and it lists no member names without the password.

ZIP and 7Z can mix methods in one archive. 7Z currently writes independent,
non-solid members: one file cannot borrow another file's compression dictionary.
LZMA2 streams on the compression worker rather than buffering 64 MiB jobs for
additional codec threads. Its dictionary is capped at the member's size (minimum
4 KiB, maximum the level-6 default of 8 MiB). This avoids oversized per-file setup
and keeps worker lifetime tied to the operation. It does not parallelize large
individual members.

Gzip has no per-file method field. A mixed TAR.GZ therefore compresses *all* TAR
bytes, including any already-compressed members. The all-compressed fast path
still emits a valid gzip header, DEFLATE stream, checksum and trailer, not raw
TAR or concatenated per-file gzip streams. It trades a little size overhead,
including uncompressed TAR metadata/padding, for avoiding recompression. TAR
keeps its symlink handling but stores sparse files in full, so small files on
ntfs3, which report no allocated blocks, keep their contents instead of
becoming zeros. Choose ZIP or 7Z when per-member compression selection matters
for mixed inputs.

The new archive is built in a hidden `.strata-copy-<id>` stage beside its
target and published only when encoding finishes. A cancelled or failed
compression removes the stage, including on SMB mounts without server inode
numbers. A crash can leave it behind, like any incomplete copy, and the
folder's **Items left by an interrupted operation** button offers to delete it.

## Classification and limits

<!-- node: operations/archives, Compressing -->

Strata decides by file extension, ignoring case, whether a member is already
compressed. The list covers common compressed
media, compressed archives and compressed document/package formats. Compound
names such as `.tar.gz` and aliases such as `.tgz` are recognized. Raw containers
such as `.tar`, `.bmp`, `.wav`, `.avi` and `.iso`, extensionless files and unknown
extensions retain compression.

Extensions are hints, not content validation: an MP4/MOV/MKV container can contain
uncompressed streams, a PDF can contain plain data, and even a ZIP can contain
stored members. Such exceptions may yield a larger output. Strata does not read
all payloads to estimate compressibility. The existing preflight walk opens
entries to count members and classify names; payloads are streamed once during
encoding. Directory recursion remains descriptor-relative and symlinks are not
followed. Sources are reopened for encoding, so concurrent source edits can
change the usefulness of the preflight gzip choice, but not the output format.

ZIP preserves UTF-8 symlink targets; TAR preserves native symlink targets.
Neither stores the target's contents. 7Z creation rejects symlinks with
`7z compression does not support symbolic links: <path>. Use ZIP or TAR instead.`
and leaves no archive. A file whose name is not valid UTF-8 fails ZIP and 7Z
with an error that names it and suggests TAR; TAR stores the original name
bytes.
Every format records each member's modification time and Unix mode. ZIP stores
the time as local DOS time, clamped to 1980–2107, plus an Info-ZIP extended
timestamp when the time falls between 1970 and January 2038; TAR records symlink times too; 7Z uses the p7zip Unix-mode
attribute and also stores each member's creation and access times when the
source filesystem reports them.

## Existing archive names

<!-- node: operations/archives, Archive name conflicts -->

When the requested archive already exists, a **File already exists** prompt
offers Cancel, Keep Both, and Replace, with Replace focused. Enter activates
the focused button. Escape, Cancel, or X leaves the existing archive unchanged
and returns focus to the listed item that was focused before the prompt.

Keep Both publishes the next available numbered name,
such as `archive (1).zip` or `archive (1).tar.gz`, and selects that new archive.
It skips existing files, directories, and symlinks, including names that appear
while encoding is running, and tries every number, so it succeeds when only the
last one is free. A long name is cut so the number fits the location's name
limit. The completed staging file is retried at each name at publication,
never replacing anything; the sources are not compressed again for each
collision.

Replace moves the existing archive to Trash before publishing the new one, and
the new archive keeps the replaced archive's permission bits. Ctrl+Z brings the
old archive back. Where the location has no Trash, the existing archive goes
into a hidden `.strata-originals-<id>` folder beside it under its own name,
swapped there atomically with the new archive where the filesystem supports
that, and is deleted once the new archive is flushed to the drive. Such a
replacement records no undo entry, so Ctrl+Z then has nothing to undo. If the
original cannot be deleted then, compression still completes and reports the
folder that keeps it. When no safe strategy exists at the location, Replace is
refused before encoding. If another item takes the name during the
replacement, nothing is replaced and the original stays set aside. Cancelling,
or an encoding failure, during Replace leaves the existing archive in place. If
publishing fails after the old archive went to Trash, the error says the
original is in Trash.

## Feedback and cancellation

<!-- node: operations/progress/dock, Docked operations -->
<!-- node: operations/progress/dock, Cancellation -->
<!-- node: operations/progress/dock, Completion -->
<!-- node: operations/progress/dock, Notices -->
<!-- node: operations/progress, Progress dialog -->
<!-- node: operations/progress, Transfer progress -->
<!-- node: operations/progress, Cancellation -->
<!-- node: devices/volumes/drive-dialogs, Format -->
<!-- node: operations/archives, Compressing -->
<!-- node: operations/archives, Extracting -->
<!-- node: operations/archives/rar -->

Compression shows `Preparing…` while counting members, then `Compressing…` and
a count such as `1 / 2 files`. Extraction opens a foreground dialog titled
`Processing archive…`. A ZIP shows `Processing archive…`, then a count such as
`3 / 12 files`; TAR, TAR.GZ, 7Z, and RAR show `Preparing…` until the first
member is written, then a running count such as `3 files` with no total. After
Cancel, the count stops updating, the title changes to `Cancelling operation…`,
and the bar pulses. A large member can take time before the completed count
advances. The activity indicator continues animating during that work and finalization; it is not a
byte-level progress estimate.

### Progress dialog

Moves, extraction, restore, emptying Trash, and undo/redo keep the foreground
progress dialog. An operation on fewer than 16 items shows no dialog for its
first 350 ms, and none at all if it finishes sooner; an operation on 16 or more
items, or with an unknown item count such as an extraction, shows it at once.
Its subtitle reads "Cancelling will not undo completed changes", except when
emptying Trash, which reads "This may take a moment". Clicking outside the
dialog leaves it, its progress, and Cancel visible, and Escape acts as Cancel.
When the dialog closes, keyboard focus goes to the file list's cursor row. If
an error dialog opens as it closes, that dialog keeps focus, with Close
focused.

While a transfer's item total is not yet known, such as a paste into a
destination slow to answer, it shows "Preparing items…" with Cancel and no
count: a move in the dialog, a copy in its card. Cancel there abandons the
transfer with no prompt.

During a move, the dialog shows the percentage, transferred and total bytes,
"N of M files" with the current file name, and the speed with time left
("Calculating speed…" until a speed is measured). The bar advances as bytes
are written, not only after each item. When everything being transferred is
empty files or folders, the bar advances by item count instead and reaches 100%
only when every item is done; a copy card does the same. With an unknown byte
total the bar pulses and reads "Preparing…" until bytes move, then
"Transferring…". A move, or an undo or redo that moves items, onto removable
media shows "Writing to device…" and is not reported done until the filesystem
flush returns. A move that has to copy, such as one to another drive, shows
"Writing to device…" during its final flush on internal disks too, except onto
SMB.

Cancel during a move, or during an undo or redo that moves items, retitles the
dialog "Cancelling transfer…", says "Waiting for the active write to stop. The
device may still be writing.", and disables the button as "Cancellation
requested". If the move has not stopped 8 seconds later, the title becomes
"Device not responding" and the subtitle warns not to unplug the device. While
a move or docked copy is still stopping, starting another file operation shows
"Transfer cancellation pending" and nothing starts. Cancel on any other
operation, such as an extraction, retitles the dialog "Cancelling operation…"
and disables Cancel.

### Progress cards

Copying, compression, deletion, and drive formatting use independent progress
cards at the bottom right, without a progress modal or a restore action. Browsing
continues while the jobs run. Cards show the full filename/status and destination
(or the drive being formatted), wrapping long text instead of truncating it.
A card also shows its title, a progress bar, and its percentage once, at the
right of its footer. The footer's left label shows a copy's speed, or a
compression's count such as `1 / 2 files`; during a deletion it is empty.
After X, a copy's label reads "Waiting for device…" and a compression's count
stops updating. A docked copy also shows files done of total. A copy onto
removable media shows "Writing to device…" in its footer and is not reported
complete until the filesystem flush returns. A compression card names the
archive instead of the first item. The
destination reads "→ \<path>" for a folder, "→ Trash" for Move to Trash, and
"Permanent deletion" for permanent deletion, or "Deletion without Trash" when
every deleted item is on a network location. Several cards stack and update
independently; the stack scrolls once it reaches 320 px. A card never blurs
or unblurs the window, even while another dialog is open.

The dock also shows brief notices, such as "Copied to \<device>" when a Send to
finishes before its progress appears. A notice is a row with a check icon
before its text and no controls; clicking it does nothing. A size notice, such
as "Text size: 16px", has no check icon and no minimum width. Notices and
progress cards stack in the order they appear. A new notice in the same window
replaces any notice still visible, but progress cards stay. Notice text, not
its heading, wraps and is cut to three lines with an ellipsis. When a notice
expires and the dock holds nothing else, the dock closes.

A docked transfer reports its renamed and left-out items once, after it ends,
such as names the destination could not store. That report joins the dock
without removing notices already visible.

The X cancels only its own copying, compression, or deletion job; other cards
and the foreground operation continue. Once requested, the card retitles to
"Cancelling transfer…" for a copy or "Cancelling operation…" otherwise, and X
is disabled while the worker stops. A cancelled copy shows "Device may still
be writing. Do not unplug until the operation stops." inside that card, without
a separate banner or a Return to browser action. Do not unplug a drive while
cancellation or writes are pending. Normal progress and pending cancellation
use neutral styling, not error borders or text. When a docked operation is
cancelled, its card closes and the "Operation cancelled" dialog described
under [Cancellation](#cancellation) opens. When one fails, its card closes
and an "Unable to complete operation" dialog shows the error. If a docked
deletion partly fails and you choose Delete Permanently while another
operation runs, "Another operation is active" appears and nothing more is
deleted.

Formatting cannot be cancelled: its card reads "Formatting drive" and "Do not
unplug until formatting finishes." and has no X while formatting runs. On
success it reads "Format complete" and "The drive was formatted successfully."
and behaves like any completed card. On failure the card closes and an error
dialog opens.

A finished copy, compression, or deletion retitles its card "Copy complete",
"Compression complete", or "Deletion complete", with a check icon, a clickable
**Complete** button, and `100%`. Its bar becomes a five-second auto-dismiss
countdown, with "closing in" text; formatting completes the same way. Hovering
or focusing a card pauses the remaining time and shows "paused"; leaving
resumes it rather than restarting the countdown. The pin button, **Keep
notification**, keeps a completed card until dismissed and shows "pinned".
**Complete** or X dismisses only that notification, never another operation.
If another operation starts before a docked copy or compression finishes, the
finished one does not select or reveal its result.

Finish or cancel running operations before closing their window. Closing a tab
with a docked operation running, or the window while any tab has one, shows
"File operations are still active" and closes nothing; closing the window while
a drive is formatting shows "Drive formatting is still active". Completed
cards are notifications, not active jobs, and do not block window closure.

### Cancellation

After a cancelled operation, an "Operation cancelled" dialog gives the counts
of items completed, failed, and not attempted, then "Completed changes were not
reverted." Every affected source and destination folder refreshes to its
on-disk state. An item that finishes copying as Cancel arrives counts as
completed, not cancelled. An item the cancel cut off and rolled back counts as
not attempted, not failed, in local transfers, Trash deletes, restores, and
merge undos. In merges, permanent deletes, and remote locations, a cut-off item
still counts as failed.

Cancellation is cooperative. Encoded output and TAR's input-to-encoder writes
check cancellation, as do 7Z source reads and existing ZIP copy chunks. Errors
from these checks become cancellation results, not corruption/password errors.
The UI waits for the worker to return before removing progress and showing the
cancellation summary. Compression staging is discarded rather than published,
and replacing an existing archive leaves that archive intact on cancellation.
Cancelled extraction keeps the members already written inside the
archive-named folder described in [Extraction output](#extraction-output).
Individual blocking filesystem calls and codec calls still have to return;
cancellation is not an immediate thread kill. RAR extraction is the exception:
its decoder runs in a separate process, which cancellation stops at once.
