---
title: Interface language
status: shipped
origin: {issue: lgse/strata#1517, pr: lgse/strata#1519}
branch: null
reviewed_at: b8938864dc95d2e041a0a442b3b7a63755681f4e
review: reviewed
code: [src/i18n.rs]
tests: [src/i18n/tests.rs, src/i18n/catalog_tests.rs, src/ui/settings/tests/general.rs]
docs: [docs/internationalization.md]
related: []
---

## Summary

The Language setting and the compiled-in translations behind it. Strata's own interface is available in ten languages, chosen automatically from the desktop locale or set manually, and applied on restart.

## Behavior

### Language setting

- General → Language offers Auto-detect, the default, and English, Français, Deutsch, Español, 日本語, Português (Brasil), 한국어, Tiếng Việt, Italiano, and Русский. lgse/strata#1519
- A manual choice is saved as `language = "fr"`, for example, and Auto-detect as `language = "auto"`. lgse/strata#1519
- A missing or unknown saved language loads as Auto-detect. lgse/strata#1519
- After a change, the running interface and newly opened windows keep the startup language until Strata restarts. lgse/strata#1519
- Restart now appears only when the chosen language resolves to a different locale than the startup one; the choice and button stay in step across Settings windows. lgse/strata#1519
- Restart now is blocked by the normal close warning while a guarded file operation runs. lgse/strata#1519

### Detection

- Auto-detect takes the first supported entry of the colon-separated `LANGUAGE` list, then the first non-empty `LC_ALL`, `LC_MESSAGES`, or `LANG`. lgse/strata#1519
- A message locale of `C` or `POSIX` selects English and ignores `LANGUAGE`. lgse/strata#1519
- With `LC_ALL`, `LC_MESSAGES`, and `LANG` all empty, Auto-detect selects English and ignores `LANGUAGE`; `C.UTF-8` does not suppress `LANGUAGE`. lgse/strata#1519 (unverified)
- Encoding and modifier suffixes are ignored, regional variants use their base language, and every Portuguese variant uses Brazilian Portuguese. lgse/strata#1519
- An unsupported locale falls back to English. lgse/strata#1519

### Translated text

- A message missing from a catalog shows its English text. lgse/strata#1519
- Filenames, paths, user-defined names, and protocol identifiers are shown untranslated. lgse/strata#1519
- Counts use each language's plural forms: Russian one, few, and many; French and Brazilian Portuguese singular for zero and one; Japanese, Korean, and Vietnamese one form. lgse/strata#1519
- Numbers, file sizes, and durations use the language's digit grouping, decimal separator, and unit symbols. lgse/strata#1519
- Programs launched from Strata keep the user's locale environment. lgse/strata#1519

## Design

[docs/internationalization.md](https://github.com/lgse/strata/blob/b8938864dc95d2e041a0a442b3b7a63755681f4e/docs/internationalization.md) carries the catalog layout and the rules for adding text.

- Changes apply on restart, approved by the owner instead of live relocalization (lgse/strata#1517, lgse/strata#1519). A language change never rebuilds an active browser or resets its navigation, selection, filters, or operations (docs/preferences.md).
- Catalogs are compiled into the binary by `build.rs` with `rust-i18n`, so no system locale packages are needed. Japanese and Korean still need installed CJK fonts (lgse/strata#1519).
- `build.rs` embeds the catalogs as static tables behind the `i18n::Catalogs` backend. The `i18n!` loader's per-message initializer overflowed 2 MiB thread stacks in unoptimized builds (lgse/strata#1519).
- Strata never rewrites the process locale. GTK-owned controls, GIO type descriptions, and system errors can therefore stay in the system language (lgse/strata#1519).
- English is the source of truth. Terms follow GNOME, KDE, and Microsoft usage for each language (lgse/strata#1541).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-08 | lgse/strata#1542 | fix | Reviewed every catalog against English and fixed mistranslations and inconsistent terms. |
| 2026-10-08 | lgse/strata#1519 | feat | Added ten compiled-in languages, locale detection, and a restart-to-apply Language setting. |

## Known gaps

- Update-check failure reasons, such as "GitHub API rate limit reached", are translated lowercase in some languages because they normally follow a colon. lgse/strata#1542
- Some progress messages, such as "%{items} deleted", lack count-aware forms for French and Brazilian Portuguese. lgse/strata#1542
