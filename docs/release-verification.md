# Verifying a release

Every release carries enough material to answer three questions before you run anything: **did I get the file we published, what is inside it, and was it built from the source it claims.**

## What a release contains

| File | What it is |
|---|---|
| `yggaro-server-linux-amd64` | the server binary — the supported target for 1.0.0 |
| `yggaro-server-linux-arm64` | the same build for arm64, provided but not a supported platform for 1.0.0 |
| `SHA256SUMS` | checksums covering every file below |
| `PROVENANCE.json` | what was built, from which commit and tag |
| `SBOM.cdx.json` | the dependency inventory, CycloneDX 1.6 |
| `VERSION.txt` | the same facts in one human-readable page |

## 1. Check what you downloaded

```bash
sha256sum -c --ignore-missing SHA256SUMS
```

`--ignore-missing` matters: `SHA256SUMS` covers the whole release and you probably downloaded only the binary for your architecture. Without it you will see `No such file or directory` for the files you did not take, and that is not a failure.

Then confirm the binary agrees:

```bash
chmod +x yggaro-server-linux-amd64
./yggaro-server-linux-amd64 -version
```

The version it prints is compiled in, together with the commit. A binary that disagrees with `VERSION.txt` is not the one we published.

## 2. Read the provenance

```json
{
  "version": "1.0.0",
  "tag": "v1.0.0",
  "commit": "…",
  "cleanTree": true,
  "builtAt": "…",
  "goVersion": "go version go1.25.13 linux/amd64",
  "mode": "release"
}
```

For a genuine release, three fields must hold: `mode` is `release`, `cleanTree` is `true`, and `tag` matches `version`. Our build refuses to produce a release otherwise — a modified working tree, a commit without an annotated tag, or a tag that disagrees with the version in the source all stop it before any artifact exists.

`builtAt` is the **commit** timestamp, not the moment somebody ran the build. That is deliberate; see below.

`PROVENANCE.json` on its own is not proof of authenticity: anyone who can replace a binary can replace the JSON beside it. It is the description of what was built — the thing a signature would sign. Treat the checksums, and where you got them, as the trust anchor for now.

## 3. Reproducibility

Building the same commit twice produces **byte-identical artifacts** — both binaries and, because every timestamp and identifier is derived from the commit rather than from the clock, an identical `SHA256SUMS`. So the whole release can be checked by rebuilding and comparing one file.

This is enforced, not hoped for: the release test suite builds twice with a delay and fails if anything differs. It is how we caught a build that embedded wall-clock time in three separate artifacts.

The source tree is not published in this repository yet, so today this property is something we verify and you can hold us to, rather than something you can re-run yourself. When the source is published, the rebuild is the check.

## 4. Dependencies

`SBOM.cdx.json` is a CycloneDX 1.6 inventory of every module compiled in, for your own vulnerability scanning. We run `govulncheck` as part of the release build, and a failure there stops the release rather than warning about it.

An SBOM tells you what was included on the day it was built. It does not stay true as new vulnerabilities are published, which is the reason to keep your own scanning rather than to trust the file.

## What we do not claim

There is no code signature on the binaries for this edition yet, and no external penetration test or formal certification. Where that matters to you, say so — it helps us order the work.

## Related

[Upgrade](upgrade.md) · [Install](install.md) · [Security model](security.md) · [Versioning](../VERSIONING.md)
