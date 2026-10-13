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

`data/update-keys.json` is the trust store compiled into Strata. It contains raw
32-byte Ed25519 public keys encoded as lowercase hexadecimal. Private keys must
never enter the repository or a release artifact. A key ID is the lowercase
SHA-256 of the raw public key, not of its textual encoding.

Every release publishes these two files alongside its archives:

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
consumer accepts at most eight unique, supported artifacts and verifies the
selected architecture and exact asset name. Files inside the archive may evolve;
the package directory, executable, and `SOURCE_COMMIT` remain required. Release
archives use `tar --format=ustar` so long prerelease portal paths do not introduce
GNU/PAX extension records, which the bounded extractor rejects.

The signature envelope has `schema: 1` and a `signatures` array. Each entry has
only `key_id` (64 lowercase hex characters) and `signature` (128 hex characters).
The Ed25519 message is the bytes `strata-update-manifest-v1`, one NUL byte, then
the **exact published manifest bytes**, including its trailing newline. Readers
must not reserialize the JSON before checking the signature. At least one
signature from an embedded key must verify. Unknown keys do not confer trust;
multiple signatures allow old and new clients to coexist during rotation.

The client bounds manifest/signature downloads to 32 KiB/8 KiB respectively,
including bodies without Content-Length. It authenticates metadata before
requesting the archive, caps the archive at its signed size (at most 128 MiB),
and verifies its SHA-256 in Rust before extraction or execution. The signed tag,
repository, architecture, package name, and source commit must match the requested
release and package. No separately downloaded checksum or mutable API lookup is
an authentication authority. Stable releases sign the original build source SHA,
not the subsequent version-bump commit; previews sign their selected source SHA.

Malformed, unsigned, oversized, or mismatched updates are refused without
replacing the installed binary. GitHub's build-provenance attestations and
`.sha256` files remain published for independent verification and packaging, but
are not prerequisites or fallbacks for this client protocol.

## Rotation and compromise

<!-- node: app/updates/install, Signed manifest -->

For a planned rotation:

1. Add the new public key alongside the old key in `data/update-keys.json` through
   a reviewed PR. Keep the old signing secret as `UPDATE_SIGNING_KEY`.
2. Set `UPDATE_SIGNING_KEY_NEXT` to the new private key. Publish a bridge release
   whose binary trusts both keys and whose manifest is signed by both keys.
3. Continue dual-signing while older clients must be able to upgrade directly.
   Removing the old signature strands clients that only trust the old key; there
   is no untrusted network-key override or automatic trust-on-first-use fallback.
4. Once that compatibility tradeoff is explicitly accepted, switch the primary
   secret to the new key, remove the secondary secret, and remove the old public
   key from subsequent binaries.

If a key is compromised, disable signing and publishing, revoke/remove the
secret, and distribute a trusted replacement through an independently verified
installation channel. An attacker holding an embedded trusted key can sign a
malicious update; an online revocation claim cannot repair that trust bootstrap.
Do not describe ordinary overlapping-key rotation as sufficient compromise
recovery for old clients.

## Rollout and limitations

<!-- node: app/updates/install, Signed manifest -->
<!-- node: app/updates/release-channels, Return to stable -->
<!-- node: app/updates/release-channels, Channels -->

Already published releases do not have these manifests. The new updater refuses
them and explains that the user must choose a newer signed release or install
manually. This includes an explicit return-to-stable request targeting an older
unsigned stable release. Publish the first signed stable release before expecting
that path to work; do not silently fall back to checksum-only or `gh` verification.
The first signed release can be installed through the existing manual/package
flow. No existing release is modified or re-signed automatically by this change.

This protocol authenticates release contents and identity, not the initial
installation or the freshness of GitHub's release feed. It does not prevent a
server from withholding an update. Normal update selection rejects older
versions; an explicit user-requested return to stable may intentionally select
an older signed version. There is no clock-dependent manifest expiry.
