---
title: Remote locations and file providers
status: shipped
origin: {issue: lgse/strata#20, pr: null}
branch: null
reviewed_at: 86df474dc0e8352e0e2098637a017cc4c77a8c44
review: draft
code: []
tests: []
docs: []
related: []
---

## Summary

How files that do not live on a local disk reach Strata. This node groups two separate mechanisms and has no code of its own. `remote/file-providers/network-locations` covers SMB, SFTP, and other GIO/GVfs locations, with mounting and sign-in; it is not a file provider in the protocol sense. `remote/file-providers/external` covers opt-in provider programs that add live badges, context actions, and Send to… destinations through Strata's provider protocol. `remote/file-providers/integrations` is the Settings → Integrations catalog that installs bundled providers. `remote/file-providers/kde-connect` and `remote/file-providers/localsend` are the two bundled providers.

## Behavior

## Design

Strata delegates remote access instead of implementing protocols, accounts, or credential storage itself. The two mechanisms share that rule and nothing else. Network locations are GIO/GVfs URIs that Strata browses (lgse/strata#20). Providers are trusted programs that decorate native files (lgse/strata#1356). [docs/file-providers.md](https://github.com/lgse/strata/blob/86df474dc0e8352e0e2098637a017cc4c77a8c44/docs/file-providers.md) specifies only the provider protocol.

- Network locations go through GIO/GVfs and a GTK mount operation, not `ssh`, `smbclient`, or `mount`. Permanent secrets are left to the backend and the desktop keyring (lgse/strata#20).
- Cloud services stay outside Strata. A provider program keeps authentication and cloud operations in its own service, and Strata has no dependency on any one provider (lgse/strata#1356, lgse/strata#1385).
- Integrations such as KDE Connect and LocalSend ship in Strata's repository but stay separate, opt-in provider programs that the user installs from Settings (lgse/strata#1741, lgse/strata#1748).
- HTTP(S) URL downloads in the file chooser belong to `integration/portal-file-chooser/url-download`, and remote preview staging to `preview/preview-panel`.

## History

| Date | PR | Type | Change |
| --- | --- | --- | --- |

## Known gaps

None known.
