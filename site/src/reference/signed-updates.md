---
nodes: [app/updates/install, app/updates/release-channels, app/updates/package-managed]
reviewed_at: 0a086aa3bdb251842a1e8413e2a6b35970d0b409
---

# Signed updates

Strata authenticates in-place updates in process. Users need neither the GitHub
CLI nor a GitHub account, token, keyring, OpenSSL command, or signing tool.
Package-managed installations still use their package manager.

## Trust and format

<!-- node: app/updates/install, Signed manifest -->
<!-- node: app/updates/install, Download limits -->
<!-- node: app/updates/install, Extraction and replacement -->
<!-- node: app/updates/install, Starting -->
<!-- node: app/updates/install, Progress and cancellation -->
<!-- node: app/updates/install, After replacement -->

`data/update-keys.json` is the trust store compiled into Strata. It contains raw
32-byte Ed25519 public keys encoded as lowercase hexadecimal. Private keys must
never enter the repository or a release artifact. A key ID is the lowercase
SHA-256 of the raw public key, not of its textual encoding.

Every release since signed updates were introduced (v1.0.0, and the v0.22.0
prereleases before it) publishes these two files alongside its archives:

- `strata-update-manifest.json`
- `strata-update-manifest.signatures.json`

The manifest is UTF-8 JSON with exactly these fields:

```json
{
  "schema": 1,
  "repository": "lgse/strata",
  "tag": "v0.12.0",
  "source_commit": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "artifacts": [
    {
      "name": "strata-0.12.0-x86_64-unknown-linux-gnu.tar.gz",
      "target": "x86_64-unknown-linux-gnu",
      "size": 123456,
      "sha256": "<64 lowercase hexadecimal characters>"
    }
  ]
}
```

The example values are illustrative, not a usable release. The publisher must
include both `x86_64-unknown-linux-gnu` and `aarch64-unknown-linux-gnu`. The
consumer accepts at most one artifact per supported target, so two in total, and
verifies the selected architecture and exact asset name. Each artifact must be
named `strata-<version>-<target>.tar.gz`, with a nonzero size of at most 128 MiB.
A manifest with a missing, extra, or wrongly typed field fails with "Invalid
signed update manifest: \<reason>". A manifest with another schema, repository,
or tag, a `source_commit` that is not 40 lowercase hex characters, or an empty
or over-eight-entry `artifacts` list fails with "The signed manifest does not
identify the selected Strata release". An unknown target, a duplicate name or
target, a misnamed entry, a zero or oversized size, or a `sha256` that is not 64
lowercase hex characters fails with "The signed manifest contains invalid or
duplicate artifacts". A manifest without this machine's architecture fails with
"The signed manifest does not contain this architecture's update". Files inside the
archive may evolve; the package directory, executable, and `SOURCE_COMMIT` remain
required. Release archives use `tar --format=ustar` so long prerelease portal
paths do not introduce GNU/PAX extension records, which the bounded extractor
rejects.

The signature envelope has `schema: 1` and a `signatures` array of one to eight
entries. Each entry has only `key_id` (64 lowercase hex characters) and
`signature` (128 hex characters). An envelope with a missing, extra, or wrongly
typed field fails with "Invalid update signatures: \<reason>". Any other schema
or entry count fails with "Unsupported update signature format".
The Ed25519 message is the bytes `strata-update-manifest-v1`, one NUL byte, then
the **exact published manifest bytes**, including its trailing newline. Readers
must not reserialize the JSON before checking the signature. At least one
signature from an embedded key must verify, or the update fails with "No
trusted release key signed this update manifest". Unknown keys do not confer
trust; multiple signatures allow old and new clients to coexist during rotation.

Manifests are signed in a release job that runs only after both builds succeed
and needs a maintainer's approval. It runs signing tools from the workflow's own
commit, never from the selected prerelease source. A missing signing key, or one
Strata's trust store does not list, stops publication.

### Download and verification

A release whose tag or archive name does not match its version is refused first,
with "The release names an unexpected update artifact." Strata downloads the
archive only from
`https://github.com/lgse/strata/releases/download/<tag>/strata-<version>-<arch>-unknown-linux-gnu.tar.gz`.
Any other location is refused with "The release points at an unexpected
download location."

The client bounds manifest/signature downloads to 32 KiB/8 KiB respectively,
including bodies without Content-Length. Metadata over its limit fails with "The
signed update metadata is too large". A release without a manifest fails with
"This release has no signed update manifest. Choose a newer release or download
it manually." While Strata fetches and checks the signed manifest, the Updates
row and the update dialog read "Verifying update…". They read it again after
the download, while the archive is checked.

Strata authenticates metadata before requesting the archive, caps the archive at
its signed size (at most 128 MiB), and verifies its SHA-256 in Rust before
extraction or execution. An archive that exceeds its signed size stops with "The
update is larger than expected and was not installed". The signed tag,
repository, architecture, package name, and source commit must match the requested
release and package. An archive whose size or SHA-256 differs from the signed
values fails with "The update does not match its signed size and checksum". An
archive whose package directory is not the selected one fails with "The
authenticated archive does not contain the selected release package". A
packaged `SOURCE_COMMIT` that differs fails with "The packaged source commit
does not match the signed manifest". No separately downloaded checksum or mutable API lookup is
an authentication authority. Stable releases sign the original build source SHA,
not the subsequent version-bump commit; previews sign their selected source SHA.

Each download, the signed metadata included, fails after 30 seconds without a
connection or 30 seconds without receiving any bytes, the wait for the server's
first reply included. Sending the request and receiving the response headers
must also each finish within 60 seconds. There is no limit on total download
time, so a slow download that keeps receiving bytes finishes.

When the archive download times out while looking up or connecting to the
server, or while sending the request, it reads "Could not reach the download
server — check your connection and try again". When it times out waiting for
the response or for data, it reads "The download stalled — check your
connection and try again". Other network errors, such as a refused connection
or a failed name lookup, read "Could not download the update: \<reason>". A
metadata request that fails before its response arrives, a timeout included,
reads "Could not download signed update metadata: \<reason>". Once the metadata
response has started, its errors read as for the archive.

### Extraction, probe, and rollback

Strata extracts the archive itself. It rejects an archive containing symbolic or
hard links, device files, named pipes, GNU or PAX extension records, absolute
paths or `..` components, more than 512 entries, more than one top-level
directory, a file over 256 MiB, or more than 512 MiB of extracted data. The
extracted package directory must match the selected asset name and contain
`strata` and `SOURCE_COMMIT`.

Before installing, Strata runs the extracted binary headless with
`--gvfs-probe`. If the probe exits with an error, the update fails with "The
downloaded update does not run on this system". If it runs longer than 2
seconds, it fails with "Update verification timed out". The previous binary is
kept beside the new one as `.strata-update-rollback`. If the installed binary
fails the same probe, Strata restores the previous binary and the update fails;
the running Strata is not relaunched. If the relaunched binary exits with an
error within 20 seconds, Strata restores the previous binary and launches it. Strata deletes
the preserved copy 60 seconds after it starts.

Malformed, unsigned, oversized, or mismatched updates are refused without
replacing the installed binary. GitHub's build-provenance attestations and
`.sha256` files remain published for independent verification and packaging, but
are not prerequisites or fallbacks for this client protocol.

## Rotation and compromise

<!-- node: app/updates/install, Signed manifest -->

A release may be signed by several keys. A new key is introduced by a bridge
release whose binary trusts both the old and new keys and whose manifest both
keys sign, so older Strata builds keep updating in place while releases stay
dual-signed. Once releases stop carrying the old key's signature, a build that
trusts only the old key cannot update in place and must be reinstalled manually.
Strata trusts only the keys compiled into it: there is no network-key override
and no automatic trust-on-first-use fallback.

If a signing key is compromised, an attacker holding it can sign updates that
every build trusting that key accepts. No online revocation claim can repair
that trust, and overlapping-key rotation does not protect old builds. Recovery
means installing a trusted replacement from an independently verified source.

## Rollout and limitations

<!-- node: app/updates/install, Signed manifest -->
<!-- node: app/updates/release-channels, Return to stable -->
<!-- node: app/updates/release-channels, Channels -->

Releases published before signed updates (v0.21.0 and earlier, and prereleases
before v0.22.0) have no signed manifest. Strata refuses to install them with
"This release has no signed update manifest. Choose a newer release or download
it manually." It never falls back to checksum-only or `gh` verification. v1.0.0
is the first signed stable release, so Return to stable from a signed prerelease
targets a signed release.

This protocol authenticates release contents and identity, not the initial
installation or the freshness of GitHub's release feed. It does not prevent a
server from withholding an update. Normal update selection rejects older
versions; an explicit user-requested return to stable may intentionally select
an older signed version. There is no clock-dependent manifest expiry.
