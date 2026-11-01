---
proposed: {page: reference/keyboard-navigation.md, section: Input precedence}
nodes: [app/window/key-dispatch]
reason: 'Which surface gets a key, and what Ctrl+wheel and Ctrl+Shift+wheel do, is user-visible and no page names the node. "Closing dialogs and overlays" already states the modal-dialog and open-menu rules, and "Creating files and folders" the rename-field rule. Add the node to the page''s nodes in site/pagemap.yaml and merge only the missing text below into "Input precedence".'
release: v1.1.1
---

### Keys behind the shortcut reference

With the **F1** shortcut reference open, **F5**, **Ctrl+K**,
**Ctrl+Shift+K**, **Ctrl+Alt+T** and **Ctrl+\\** do nothing; **F5** does not
refresh the folder behind it, so the reference's search takes every key.

With a 10xer chord armed, **Ctrl+0** on a focused PDF drops the chord and then
resets the page zoom.

### Ctrl+wheel and Ctrl+Shift+wheel

- **Ctrl+wheel** changes the interface text size by 1 px per notch. Touchpad
  scrolling adds up to whole steps.
- **Ctrl+Alt+wheel** and **Ctrl+Super+wheel** leave the text size alone and
  scroll as a plain wheel does.
- Over a PDF preview, scrollbars included, **Ctrl+wheel** zooms the PDF and
  leaves the text size alone. Over the file listing it changes the text size,
  even while the PDF holds keyboard focus.
- **Ctrl+Shift+wheel** never changes the text size. In Icons it steps the
  thumbnail size one step per notch, up for larger and down for smaller, also
  when it arrives as horizontal scrolling. In Columns and List it resizes nothing
  and scrolls the view.
- **Ctrl+wheel** never changes the Icons thumbnail size.
- The system file chooser has no wheel zoom: **Ctrl+Shift+wheel** there does not
  step the thumbnail size.
