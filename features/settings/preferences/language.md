---
title: Interface language
status: shipped
origin: {issue: lgse/strata#1517, pr: lgse/strata#1519}
branch: null
reviewed_at: 6e654a7b68fdfeb0a6eec8239a95b16ccfb1cea8
review: draft
code: [src/i18n.rs, data/locales/counts.json]
tests: [src/i18n/tests.rs, src/i18n/catalog_tests.rs]
docs: [docs/internationalization.md]
related: []
---

## Summary

The Language setting and the compiled-in translations behind it. Strata's own interface is available in eleven languages, chosen automatically from the desktop locale or set manually, and applied on restart.

## Behavior

### Language setting

- General → Language offers Auto-detect, the default, and English, Français, Deutsch, Español, 日本語, Português (Brasil), 한국어, Tiếng Việt, Italiano, Русский, and 简体中文. lgse/strata#1519, lgse/strata#1583
- A manual choice is saved as `language = "fr"`, for example, and Auto-detect as `language = "auto"`. lgse/strata#1519
- Choosing 简体中文 saves `language = "zh-CN"`. lgse/strata#1583
- A missing or unknown saved language loads as Auto-detect. lgse/strata#1519
- After a change, the running interface and newly opened windows keep the startup language until Strata restarts. lgse/strata#1519
- Restart now appears only when the chosen language resolves to a different locale than the startup one; the choice and button stay in step across Settings windows. lgse/strata#1519
- Restart now is blocked by the normal close warning while a guarded file operation runs. lgse/strata#1519

### Detection

- Auto-detect takes the first supported entry of the colon-separated `LANGUAGE` list, then the first non-empty `LC_ALL`, `LC_MESSAGES`, or `LANG`. lgse/strata#1519
- A message locale of `C` or `POSIX` selects English and ignores `LANGUAGE`. lgse/strata#1519
- With `LC_ALL`, `LC_MESSAGES`, and `LANG` all empty, Auto-detect selects English and ignores `LANGUAGE`; `C.UTF-8` does not suppress `LANGUAGE`. lgse/strata#1519 (unverified)
- Encoding and modifier suffixes are ignored, regional variants use their base language, and every Portuguese variant uses Brazilian Portuguese. lgse/strata#1519
- Auto-detect selects 简体中文 for every Chinese locale, including Traditional ones such as `zh_TW.UTF-8`, `zh_HK.UTF-8`, and `LANGUAGE=zh-Hant`. lgse/strata#1582, lgse/strata#1583
- An unsupported locale falls back to English. lgse/strata#1519

### Translated text

- A message missing from a catalog shows its English text. lgse/strata#1519
- Filenames, paths, user-defined names, and protocol identifiers are shown untranslated. lgse/strata#1519
- Counts use each language's plural forms: Russian one, few, and many; French and Brazilian Portuguese singular for zero and one; Chinese, Japanese, Korean, and Vietnamese one form, such as `3 个项目`. lgse/strata#1519, lgse/strata#1583
- Numbers, file sizes, and durations use the language's digit grouping, decimal separator, and unit symbols. lgse/strata#1519
- Under 简体中文, numbers read `1,234,567.3`, durations read `45秒`, `2分5秒`, and `1小时2分`, and lists join with `、`. lgse/strata#1583
- Under 简体中文 or 日本語, a sentence ending in `。`, `！`, or `？` gets no space before the next. This applies to archive extraction errors, FAT32 copy failures, transfer flush errors, and package-managed update text. lgse/strata#1583 (unverified)
- In those messages, a first sentence without a stop, such as a bare system error, gets the language's full stop. That stop is `。` in Chinese and Japanese and `. ` elsewhere. lgse/strata#1583 (unverified)
- Programs launched from Strata keep the user's locale environment. lgse/strata#1519

## Design

[docs/internationalization.md](https://github.com/lgse/strata/blob/0562724ad97c8e83a4c81b85e556bf275be3b025/docs/internationalization.md) carries the catalog layout and the rules for adding text.

- Changes apply on restart, approved by the owner instead of live relocalization (lgse/strata#1517, lgse/strata#1519). A language change never rebuilds an active browser or resets its navigation, selection, filters, or operations (docs/preferences.md).
- Catalogs are compiled into the binary by `build.rs` with `rust-i18n`, so no system locale packages are needed. Japanese and Korean still need installed CJK fonts (lgse/strata#1519). Simplified Chinese needs a CJK font with Simplified glyphs, such as Noto Sans CJK SC (lgse/strata#1582, lgse/strata#1583).
- `build.rs` embeds the catalogs as static tables behind the `i18n::Catalogs` backend. The `i18n!` loader's per-message initializer overflowed 2 MiB thread stacks in unoptimized builds (lgse/strata#1519).
- Strata never rewrites the process locale. GTK-owned controls, GIO type descriptions, and system errors can therefore stay in the system language (lgse/strata#1519).
- `rust-i18n` moved from 3.1.5 to 4.2.4 because cargo-deny rejects `unsafe-libyaml` (RUSTSEC-2024-0449). `i18n::Catalogs` follows the 4.0 `Backend` trait; the compiled tables are unchanged (lgse/strata#1583).
- One Chinese catalog serves every Chinese locale, as Brazilian Portuguese serves every Portuguese one. The owner rejected an English fallback for Traditional locales (lgse/strata#1582).
- Two shared helpers were extended instead of adding zh-only paths: `i18n::join_sentences`, replacing an archive-only `。` case, and Settings search (lgse/strata#1583).
- Setting `PANGO_LANGUAGE` from Strata was rejected: it must be set before threads start and scrubbed from every launched program (lgse/strata#1583).
- English is the source of truth. Terms follow GNOME, KDE, and Microsoft usage for each language (lgse/strata#1541).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-13 | lgse/strata#1625 | fix | Reworded zh-CN strings so Compact sidebar no longer reads as Hide, and the password choices use the label's verb 保存. |
| 2026-10-12 | lgse/strata#1583 | feat | Added Simplified Chinese as the eleventh language, auto-detected for every Chinese locale, with a shared sentence joiner and Han/kana Settings search matching. |
| 2026-10-08 | lgse/strata#1542 | fix | Reviewed every catalog against English and fixed mistranslations and inconsistent terms. |
| 2026-10-08 | lgse/strata#1519 | feat | Added ten compiled-in languages, locale detection, and a restart-to-apply Language setting. |

## Known gaps

- Update-check failure reasons, such as "GitHub API rate limit reached", are translated lowercase in some languages because they normally follow a colon. lgse/strata#1542
- Some progress messages, such as "%{items} deleted", lack count-aware forms for French and Brazilian Portuguese. lgse/strata#1542
- Han glyph forms follow the process locale or `PANGO_LANGUAGE`, so choosing 简体中文 on an `en_US` system can show another region's glyph forms. lgse/strata#1583
- There is no Traditional Chinese catalog; Traditional locales get Simplified Chinese. lgse/strata#1582
