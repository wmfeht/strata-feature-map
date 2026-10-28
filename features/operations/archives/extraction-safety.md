---
title: Extraction safety
status: shipped
origin: {issue: lgse/strata#109, pr: lgse/strata#116}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: [src/adapters/local_operations/archive/destination.rs]
tests: [src/adapters/local_operations/archive/destination/tests.rs]
related: [operations/filesystem-compatibility]
---

## Summary

How extraction writes untrusted archive members into the destination folder: member path sanitizing, confinement to the destination, link members, metadata, and names the destination cannot store. Member path rules apply to every decoder, RAR included. RAR link members extract as regular files (`operations/archives/rar`).

## Behavior

### Destination

- Extracting into a folder reached through a symlink writes into the resolved folder. lgse/strata#678
- Extract to… accepts a write-only drop box, such as a mode `0733` folder owned by another user, then fails with "Could not open extraction destination: Permission denied". lgse/strata#1729

### Member paths

- A member named `../report.txt` or `folder/../report.txt` extracts as `report.txt` inside the destination, and later members still extract. lgse/strata#1191
- Two members that resolve to `report.txt` extract as `report.txt` and `report (2).txt`. lgse/strata#116, lgse/strata#1191
- An absolute member path or a member written through an existing symlink fails the extraction without writing outside the destination. lgse/strata#116, lgse/strata#1478
- A ZIP, 7Z, or TAR directory entry named `.`, `./`, or `././`, or a ZIP one named `.\`, is skipped. The other members extract instead of failing. lgse/strata#494, lgse/strata#1814
- TAR and 7Z `.\` directory entries, and a RAR directory entry naming only the root, are skipped the same way. lgse/strata#1814 (unverified)
- A ZIP whose only member is a file or link named `.`, or a directory `../` or `foo/../`, fails and writes nothing. The error is "Refusing empty archive path: <name>". lgse/strata#1814
- A ZIP with members `before.txt`, `names/c:notes`, and `after.txt` extracts all three onto a destination that allows `:`, such as ext4, with `c:notes` inside `names/`. lgse/strata#1855, lgse/strata#1872
- A member path whose first component is a drive prefix, after `.` is skipped and `..` resolved, fails the extraction. Examples are `C:marker`, `./c:notes`, and `safe/../c:notes`. The error starts with "Refusing unsafe archive path: <name>". lgse/strata#1855, lgse/strata#1872

### Links

- Symlink members are recreated with their stored targets, including absolute ones. lgse/strata#1478
- A TAR hard link links to the earlier member of that name; a hard link to a member not extracted fails the extraction. lgse/strata#1478
- A TAR hard link whose target is `names/c:notes` links to that extracted member. lgse/strata#1872
- On vfat, exFAT, exfat-fuse, or an SMB mount without hard links, a TAR hard link to an extracted file becomes a copy of it. Later members still extract. lgse/strata#1848, lgse/strata#1870
- That copy takes space of its own and gets the member's stored mode and modification time. lgse/strata#1870
- A hard link the mount refuses for another reason, such as no space or an I/O error, still fails. The error reads "Could not link “<member>” to “<target>”: <reason>". lgse/strata#1870
- The mount may hold no hard links while the target cannot be reopened for the copy. The error then gives the reopen failure after "Could not link". lgse/strata#1870
- Links the destination cannot hold, and hard links to them, are left out and reported, and the extraction finishes. lgse/strata#1615

### Metadata and names

- Each member gets its stored mode, masked by the umask with setuid, setgid, and sticky removed, and its stored modification time. lgse/strata#1478
- On FAT and exFAT, modes and times are skipped without error. lgse/strata#1478
- Extracted symlink times are not set on FUSE mounts. lgse/strata#1615
- Extracting where member names cannot be stored fixes them by the destination's rules, retrying refused names under stricter rules, and reports each change. lgse/strata#1615
- Folders whose fixed names became one stay apart, such as `10_00 (2)/`. lgse/strata#1615

## Design

- Member paths are untrusted. Writes go through one pinned destination descriptor with `openat2` and per-component `NOFOLLOW`, so traversal names and swapped symlinks cannot escape (lgse/strata#109, lgse/strata#116).
- The destination itself may be reached through ordinary symlinks; it is resolved with `RESOLVE_IN_ROOT` and pinned, as copy and compress already did (lgse/strata#644, lgse/strata#678).
- `..` components are clamped at the destination instead of aborting the whole archive (lgse/strata#1189, lgse/strata#1191).
- A drive prefix is refused only as the first component left after `.` is skipped and `..` popped, so `safe/../c:notes` stays refused. A colon in a later component is an ordinary name (lgse/strata#1855, lgse/strata#1872).
- Directory members that name only the archive root are skipped in `ExtractionSession::extract_member`, so every decoder shares one check. File members with the same spelling still reach empty-path validation (lgse/strata#1801, lgse/strata#1814).
- Metadata restoration matches `tar` and `unzip` for a normal user: no owner, group, xattrs, or ACLs; folder metadata applies only on completion so partial output stays writable (lgse/strata#1422).
- A hard link the mount cannot hold degrades to a copy, as symbolic links degrade to being left out. `EPERM`, `ENOSYS`, and `EOPNOTSUPP` mean no hard links, matching the copy engine's placement probe (lgse/strata#1848, lgse/strata#1870).
- The copy is re-dispatched through the regular file path, so declared size, free space, and cancellation apply. A taken name is not treated as missing support (lgse/strata#1870).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

- A hard link to an extracted symlink fails the extraction where the mount holds symlinks but not hard links. sshfs without its hardlink extension is one such mount. lgse/strata#1870
