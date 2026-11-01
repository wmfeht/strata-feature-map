---
proposed: {page: reference/preview-sandbox.md, section: Browser worker pool}
nodes: [browser/thumbnails/cache]
reason: 'The Preview sandbox page names the shared thumbnails/large cache only for rendered STL thumbnails ("Model thumbnails"). It does not say that every local thumbnail is saved there and read back, that other applications'' entries are used, or how cached files are validated. "Browser worker pool" describes thumbnail rendering; add the node to the page''s nodes in site/pagemap.yaml, drop it from site/unguided.yaml, and merge the text below as a `###` subsection.'
release: v1.1.1
---

### Disk cache

After rendering a thumbnail for a local file, Strata saves a 256 px PNG to the
freedesktop shared cache, `$XDG_CACHE_HOME/thumbnails/large/` (or
`~/.cache/thumbnails/large/`), named by the MD5 of the file's URI. Revisiting the
folder, even after a restart, shows thumbnails from the cache without rendering
again. Rendering an image or page 1 of a PDF in the preview also saves one.

Entries written by other applications are used when their URI and modification
time match the file. A RAW thumbnail Strata writes carries its own tag; a RAW
entry without it, from an older Strata or another application, is rendered again
and replaced.

Strata treats cached files as untrusted. An entry that is a symlink, larger than
2 MiB, over 512 px, or not a PNG is ignored. Failed renders and camera files are
never cached. The `large` folder is kept at mode 0700 and entries are written
with mode 0600.
