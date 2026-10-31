---
title: Interface language
status: shipped
origin: {issue: lgse/strata#1517, pr: lgse/strata#1519}
branch: null
reviewed_at: 965bd7ec74400734dbd0a5311ceefa05bea8dd63
review: draft
code: [src/i18n.rs, data/locales/counts.json]
tests: [src/i18n/tests.rs, src/i18n/catalog_tests.rs]
docs: [docs/internationalization.md]
related: []
---

## Summary

The Language setting and the compiled-in translations behind it. Strata's own interface is available in thirteen languages, chosen automatically from the desktop locale or set manually, and applied on restart.

## Behavior

### Language setting

- General → Language offers Auto-detect, the default, and English, Français, Magyar, Deutsch, Español, 日本語, Português (Brasil), 한국어, Tiếng Việt, Italiano, Русский, 简体中文, and 正體中文, in that order. lgse/strata#1519, lgse/strata#1583, lgse/strata#1745, lgse/strata#1918
- A manual choice is saved as `language = "fr"`, for example, and Auto-detect as `language = "auto"`. lgse/strata#1519
- Choosing 简体中文 saves `language = "zh-CN"`. lgse/strata#1583
- Choosing Magyar saves `language = "hu"`, and after a restart the interface reads in Hungarian. lgse/strata#1918
- Choosing 正體中文 saves `language = "zh-TW"`, and after a restart the interface reads in Traditional Chinese. lgse/strata#1745
- A saved `language = "zh-tw"`, in lowercase, loads as Auto-detect. lgse/strata#1745 (unverified)
- A missing or unknown saved language loads as Auto-detect. lgse/strata#1519
- After a change, the running interface and newly opened windows keep the startup language until Strata restarts. lgse/strata#1519
- Restart now appears only when the chosen language resolves to a different locale than the startup one; the choice and button stay in step across Settings windows. lgse/strata#1519
- Restart now is blocked by the normal close warning while a guarded file operation runs. lgse/strata#1519

### Detection

- Auto-detect takes the first supported entry of the colon-separated `LANGUAGE` list, then the first non-empty `LC_ALL`, `LC_MESSAGES`, or `LANG`. lgse/strata#1519
- A message locale of `C` or `POSIX` selects English and ignores `LANGUAGE`. lgse/strata#1519
- With `LC_ALL`, `LC_MESSAGES`, and `LANG` all empty, Auto-detect selects English and ignores `LANGUAGE`; `C.UTF-8` does not suppress `LANGUAGE`. lgse/strata#1519 (unverified)
- Encoding and modifier suffixes are ignored, regional variants use their base language, and every Portuguese variant uses Brazilian Portuguese. lgse/strata#1519
- Auto-detect selects Magyar for `LANG=hu_HU.UTF-8`, and for `LANGUAGE=xx:hu_HU:fr` with `LANG=de_DE`. lgse/strata#1918
- Auto-detect selects 正體中文 for `zh_TW.UTF-8`, `zh_HK.UTF-8`, `zh_MO`, and a `LANGUAGE` entry such as `zh-Hant`. lgse/strata#1745
- Auto-detect selects 简体中文 for `zh_CN`, `zh_SG`, `zh-Hans`, bare `zh`, and any other Chinese region, such as `zh_MY.UTF-8`. lgse/strata#1583, lgse/strata#1745
- Chinese routing reads only the second subtag, so `zh-Hans-TW` selects 简体中文 and `zh-Hant-HK` selects 正體中文. lgse/strata#1745 (unverified)
- An unsupported locale falls back to English. lgse/strata#1519

### Translated text

- A message missing from a catalog shows its English text. lgse/strata#1519
- Filenames, paths, user-defined names, and protocol identifiers are shown untranslated. lgse/strata#1519
- Counts use each language's plural forms: Russian one, few, and many; French and Brazilian Portuguese singular for zero and one; Chinese, Japanese, Korean, and Vietnamese one form, such as `3 个项目`. lgse/strata#1519, lgse/strata#1583
- Numbers, file sizes, and durations use the language's digit grouping, decimal separator, and unit symbols. lgse/strata#1519
- A 999,950-byte file's size reads "1 MB", not "1000 kB", in the views and the preview; 999,950,000 bytes reads "1 GB". lgse/strata#698
- Under 简体中文, numbers read `1,234,567.3`, durations read `45秒`, `2分5秒`, and `1小时2分`, and lists join with `、`. lgse/strata#1583
- Under 正體中文, counts use one form, such as `3,000 個檔案`; numbers read `1,234,567.3`, durations read `45秒`, `2分5秒`, and `1小時2分`, and lists join with `、`. lgse/strata#1745
- Under Magyar, digits group with a no-break space and decimals use a comma: `3 000 fájl`, `1 234 567,3`, `1,5 kB`, and `128,5 MB/s`. lgse/strata#1918
- Under Magyar, durations read `2 mp`, `2 p 5 mp`, and `1 ó 2 p`. lgse/strata#1918
- Under Français, Español, Italiano, Português (Brasil), Magyar, Русский, and Tiếng Việt, a capitalized error reason after a colon continues in lower case. Magyar reads "…: hozzáférés megtagadva". lgse/strata#1519, lgse/strata#1918 (unverified)
- Under 简体中文, 正體中文, or 日本語, a sentence ending in `。`, `！`, or `？` gets no space before the next. This applies to archive extraction errors, FAT32 copy failures, transfer flush errors, and package-managed update text. lgse/strata#1583, lgse/strata#1745 (unverified)
- In those messages, a first sentence without a stop, such as a bare system error, gets the language's full stop. That stop is `。` in Chinese and Japanese and `. ` elsewhere. lgse/strata#1583 (unverified)
- Programs launched from Strata keep the user's locale environment. lgse/strata#1519

## Design

[docs/internationalization.md](https://github.com/lgse/strata/blob/e0f73973926ff67e77c2c56cf288b7b7617bb2e5/docs/internationalization.md) carries the catalog layout and the rules for adding text.

- Changes apply on restart, approved by the owner instead of live relocalization (lgse/strata#1517, lgse/strata#1519). A language change never rebuilds an active browser or resets its navigation, selection, filters, or operations (docs/preferences.md).
- Catalogs are compiled into the binary by `build.rs` with `rust-i18n`, so no system locale packages are needed. Japanese and Korean still need installed CJK fonts (lgse/strata#1519). Simplified Chinese needs a CJK font with Simplified glyphs, such as Noto Sans CJK SC (lgse/strata#1582, lgse/strata#1583). Traditional Chinese needs one with Traditional glyphs, such as Noto Sans CJK TC (docs/internationalization.md).
- `build.rs` embeds the catalogs as static tables behind the `i18n::Catalogs` backend. The `i18n!` loader's per-message initializer overflowed 2 MiB thread stacks in unoptimized builds (lgse/strata#1519).
- Strata never rewrites the process locale. GTK-owned controls, GIO type descriptions, and system errors can therefore stay in the system language (lgse/strata#1519). Unclassified failures on URI network locations show Strata's own text instead (lgse/strata#1909).
- `rust-i18n` moved from 3.1.5 to 4.2.4 because cargo-deny rejects `unsafe-libyaml` (RUSTSEC-2024-0449). `i18n::Catalogs` follows the 4.0 `Backend` trait; the compiled tables are unchanged (lgse/strata#1583).
- Traditional Chinese locales route to their own catalog (Option A), over a manual-only choice (Option B). Option A changes auto-detection for existing `zh_TW` and `zh_HK` users (lgse/strata#1613, lgse/strata#1745).
- Hong Kong and Macau use the Taiwan catalog until a zh-HK one is contributed (lgse/strata#1613).
- Other Chinese regions, such as `zh_MY`, keep Simplified Chinese rather than falling back to English (lgse/strata#1745).
- The zh-TW catalog is translated from English in Taiwan terms, not converted from zh-CN. Key names and F1 descriptions are translated too, because mixed-script labels read as inconsistent (lgse/strata#1613, lgse/strata#1745).
- Two shared helpers were extended instead of adding zh-only paths: `i18n::join_sentences`, replacing an archive-only `。` case, and Settings search (lgse/strata#1583).
- Setting `PANGO_LANGUAGE` from Strata was rejected: it must be set before threads start and scrubbed from every launched program (lgse/strata#1583).
- English is the source of truth. Terms follow GNOME, KDE, and Microsoft usage for each language (lgse/strata#1541).

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |
| 2026-10-31 | lgse/strata#1966 | fix | Revised Hungarian message wording; no keys or placeholders changed. |
| 2026-10-29 | lgse/strata#1918 | feat | Added Hungarian (Magyar) as the thirteenth language, with locale detection, no-break-space digit grouping, and lower-case error details after a colon. |
| 2026-10-18 | lgse/strata#1745 | feat | Added Traditional Chinese (zh-TW) as the twelfth language and routed Traditional Chinese locales to it instead of Simplified Chinese. |
| 2026-10-13 | lgse/strata#1625 | fix | Reworded zh-CN strings so Compact sidebar no longer reads as Hide, and the password choices use the label's verb 保存. |
| 2026-10-12 | lgse/strata#1583 | feat | Added Simplified Chinese as the eleventh language, auto-detected for every Chinese locale, with a shared sentence joiner and Han/kana Settings search matching. |
| 2026-10-08 | lgse/strata#1542 | fix | Reviewed every catalog against English and fixed mistranslations and inconsistent terms. |
| 2026-10-08 | lgse/strata#1519 | feat | Added ten compiled-in languages, locale detection, and a restart-to-apply Language setting. |
| 2026-09-09 | lgse/strata#698 | fix | Rounded a file size before choosing its unit, so 999,950 bytes shows 1 MB instead of 1000 kB. |

## Known gaps

- Update-check failure reasons, such as "GitHub API rate limit reached", are translated lowercase in some languages because they normally follow a colon. lgse/strata#1542
- Some progress messages, such as "%{items} deleted", lack count-aware forms for French and Brazilian Portuguese. lgse/strata#1542
- Han glyph forms follow the process locale or `PANGO_LANGUAGE`, so choosing 简体中文 or 正體中文 on an `en_US` system can show another region's glyph forms. lgse/strata#1583, lgse/strata#1745
- There is no zh-HK catalog; Hong Kong and Macau locales get the Taiwan catalog. lgse/strata#1745
