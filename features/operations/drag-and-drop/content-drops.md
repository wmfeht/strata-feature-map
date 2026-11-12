---
title: Content drops from other applications
status: shipped
origin: {issue: lgse/strata#1545, pr: lgse/strata#1547}
branch: null
reviewed_at: 5f17c9fdc8967e1b4ba8aaf8de113b46d824b0dd
review: reviewed
code: [src/ui/browser/content_drop.rs, crates/strata-fs/src/services/dropped_content.rs]
tests: [src/ui/browser/content_drop/tests.rs, crates/strata-fs/src/services/dropped_content/tests.rs, tests/qa/scenarios/content_drops]
docs: [docs/content-drops.md]
related: [integration/open-with, operations/clipboard, operations/trash, browser/tabs]
---

## Summary

Saving an image, selected text, or a web address dragged from another application as a new file. The file goes in the local folder that takes the drop. It works on folder rows, pane backgrounds, breadcrumbs, sidebar folders, and tabs, in every view. Files dragged from another application still transfer through the parent's path.

## Behavior

### What is saved

- Image data dropped from Firefox on a local folder saves as the PNG `image.png`. lgse/strata#1547
- An image's file contents offered by a Chromium-based browser save as the original bytes under the browser's name. lgse/strata#1547
- That file takes the extension of the detected format (PNG, JPEG, GIF, WebP, AVIF, BMP, TIFF, or ICO), whatever the supplied name says. lgse/strata#1547
- Dropped selected text saves as the UTF-8 file `dropped text.txt`. lgse/strata#1547
- Saved names follow the interface language, such as `image.png` and `dropped text.txt` in English. lgse/strata#1547
- A dropped HTTP or HTTPS address saves as `<host>.desktop`, such as `example.com.desktop`. lgse/strata#1547
- A leading `www.` is dropped from the host, so `https://www.example.com/` also saves as `example.com.desktop`. lgse/strata#1547 (unverified)
- That file is a `Type=Link` desktop entry with the address and no `Exec` key, and it is not executable. lgse/strata#1547
- An address offered in two formats at once saves one link. lgse/strata#1547
- Dropped text that is exactly one credential-free HTTP or HTTPS address saves as a link, not as text. lgse/strata#1547 (unverified)
- A URI list of several web addresses saves one `.desktop` file per address. lgse/strata#1547 (unverified)
- Dropping an address never contacts it, and an image address is not downloaded. lgse/strata#1547

### Choosing between offers

- A drag offering real files with image data, such as from a screenshot tool, copies the files and saves no image. lgse/strata#1547
- An image offered with web addresses only saves the image. lgse/strata#1547
- When that image cannot be read or is not a recognized format, the offered address or text is saved instead. lgse/strata#1547
- An image dropped with a web address before Strata has read the hovered address list saves the address's `.desktop` link instead of the image. lgse/strata#1547 (unverified)
- An address with credentials, another scheme, or over 16 KiB is no link. lgse/strata#1547
- A URI list holding at least one HTTP or HTTPS address is refused whole when any entry cannot become a link. lgse/strata#1547
- A URI list with no web address transfers as files. lgse/strata#1547
- Strata's own tab and sidebar reorder drags are never saved as text. lgse/strata#1547

### Where it saves

- Folder rows in Columns, List, and Icons, pane backgrounds, parent breadcrumbs, sidebar folders, and tabs accept content drops. lgse/strata#1547
- An image, text, or web-link drag highlights rows, spring-loads folders, and auto-scrolls the view as a file drag does. lgse/strata#1547
- Remote folders, Trash, and Recent accept no content drops. lgse/strata#1547
- A repeated drop gets a numbered name, such as `dropped text (1).txt`. lgse/strata#1547
- No existing entry is replaced, including a dangling symlink. lgse/strata#1547
- A saved file appears only once complete. lgse/strata#1547
- Some filesystems, such as some FUSE mounts, can neither rename without replacing nor make hard links. There the file is written in place, and removed if writing fails. lgse/strata#1547
- Pasting a clipboard image saves through the same path, so the pasted file also appears only once complete. lgse/strata#1547
- With Open folder after dropping files on, the saved file is selected in the destination, unless the user navigated away meanwhile. lgse/strata#1547

### Failures

- A drop on a read-only folder writes nothing and shows "Unable to save dropped content". lgse/strata#1547
- An image that cannot be read, is no recognized format, or exceeds 64 MiB shows the same dialog with the reason. This holds when nothing else was offered. lgse/strata#1547
- The reasons read "Unsupported image format" and "The dropped content is too large". lgse/strata#1547
- When one link of a multi-address drop fails, earlier saved links stay and the error is shown. lgse/strata#1547 (unverified)

## Design

[docs/content-drops.md](https://github.com/lgse/strata/blob/0f9bb00f02d3923ba009f53e0dbaecb840ee524c/docs/content-drops.md) describes what each dropped content saves as and how web links open.

- The issue asked for Finder parity, so a browser image need not be saved and then moved (lgse/strata#1545).
- Dropped addresses are never fetched, as in Finder, Dolphin, and Nautilus; a stray drop must not reach the network. Probing image URLs was removed in review (lgse/strata#1547).
- The link entry has no `Exec` and is not executable, so opening it cannot run a program (lgse/strata#1547).
- Each target pairs a `gtk::DropTarget` for file lists, textures, and strings with a `DropTargetAsync` companion. The companion reads images at drop time, since `DropTarget` finishes when its handler returns and cannot read browser file contents (lgse/strata#1547).
- File lists are read while hovering, to choose copy or move; images and text are read only on drop (lgse/strata#1547).
- The content decision runs before file classification, because classifying files may query volumes, which a web address must never reach (lgse/strata#1547).
- New content goes only to local folders, because Trash, Recent, and remote locations are URIs (lgse/strata#1547).
- The 64 MiB cap bounds the memory a browser can make Strata hold (lgse/strata#1547).
- Saves write a temporary `.strata-drop-*` file and publish it with a no-replace rename, falling back to an exclusive in-place write where unsupported (lgse/strata#1547).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
