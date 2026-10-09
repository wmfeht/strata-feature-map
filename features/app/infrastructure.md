---
title: Shared location model and listing adapter
status: shipped
origin: {issue: lgse/strata#14, pr: lgse/strata#27}
branch: null
reviewed_at: aee71335dfecd059b9af23efeac2ed52c43e3b19
review: draft
code: [src/model/mod.rs, src/adapters/local_files.rs, src/ui/mod.rs]
tests: [src/adapters/local_files/tests.rs, src/adapters/local_files/tests/browse.rs]
docs: [docs/performance-baseline.md]
related: [remote/file-providers/network-locations, operations/trash, browser/navigation/location-bar, browser/directory-monitoring]
---

## Summary

The location model, URI display and diagnostic rules, and the directory-listing adapter that every feature shares, plus the UI module root. This node owns those shared modules as a fallback: it takes a change only when no feature node's code is touched.

## Behavior

### URI display

- The location field and Properties show a URI location decoded only when its whole path is valid UTF-8 and has no `%2F`. lgse/strata#1424, lgse/strata#1533
- Otherwise the whole path shows percent-encoded, such as `sftp://host/share/%FF%20name` or `trash:///caf%E9.txt`. lgse/strata#1424, lgse/strata#1533

### Listing

- A URI listing, such as Trash or an SMB share, skips an entry whose URI cannot be converted to a location. lgse/strata#1424, lgse/strata#1533 (unverified)
- Each skipped entry logs a warning with only the request id and backend name; the folder and entry name appear only at DEBUG. lgse/strata#1424, lgse/strata#1533

### Log privacy

- At the default log level, a directory load logs its request id and backend name, never the browsed path or URI. lgse/strata#27
- With `RUST_LOG=strata=debug`, a directory load also logs its location, including the full native path. lgse/strata#27
- Logged URI locations omit user info, authentication parameters, query, and fragment at every log level. lgse/strata#27

## Design

[docs/performance-baseline.md](https://github.com/lgse/strata/blob/aee71335dfecd059b9af23efeac2ed52c43e3b19/docs/performance-baseline.md) states the log privacy levels: default logs carry request ids, backend names, counts, and timings only.

- Desktop logs and journals can retain usernames, project names, and mounted locations, so browsed locations need an explicit diagnostic opt-in (lgse/strata#14, lgse/strata#27).
- `Location` display and diagnostic paths once parsed strictly and showed `<invalid-uri>` for non-UTF-8 names in the path bar and Properties. They now share the GIO conversion's parse flags (lgse/strata#1424, lgse/strata#1533).
- Display tries the decoded form first, so valid names such as `smb://host/café` still display decoded (lgse/strata#1533).
- The directory loader dropped unconvertible entries without a trace. Logging each skip keeps a future conversion failure visible (lgse/strata#1424, lgse/strata#1533).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-09 | lgse/strata#1533 | fix | Parsed GIO URIs with encoded path flags, displayed non-UTF-8 locations percent-encoded, and logged skipped listing entries. |
| 2026-08-30 | lgse/strata#27 | fix | Removed browsed locations from default logs and redacted URI credentials from diagnostic ones. |

## Known gaps

None known.
