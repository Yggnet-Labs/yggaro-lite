# Verifying a release

Every release carries enough material to answer three questions before you run anything: **did I get the file we published, what is inside it, and was it built from the source it claims.**

## What a release contains

| File | What it is |
|---|---|
| `yggaro-server-linux-amd64` | the server binary — the supported target for the 1.0.x releases |
| `SHA256SUMS` | checksums covering every file below |
| `LICENSE` | the product licence (FSL-1.1-ALv2) that governs the downloaded binary |
| `NOTICE` | the short notice that accompanies the licence |
| `THIRD-PARTY-NOTICES.md` | licences of the third-party components compiled into the binary; `yggaro-server -third-party-notices` prints the same text |
| `PROVENANCE.json` | what was built, from which commit and tag |
| `SBOM.cdx.json` | the dependency inventory, CycloneDX 1.6 |
| `VERSION.txt` | the same facts in one human-readable page |

`LICENSE` and `NOTICE` are attached from 1.0.2 on; 1.0.0 and 1.0.1 were published without them, and for those the licence is the `LICENSE` file in this repository.

## 1. Check what you downloaded

```bash
grep '  yggaro-server-linux-amd64$' SHA256SUMS | sha256sum -c -
```

It must print `yggaro-server-linux-amd64: OK`. The command checks exactly the file you are about to run: `SHA256SUMS` lists every file of the release, and a plain `sha256sum -c --ignore-missing SHA256SUMS` can finish successfully without having checked the binary at all — for example when the downloaded file has a different name. Check any other file you downloaded the same way, with its own name in the pattern.

The checksums prove integrity — that the file is the one listed — not who made it. Take `SHA256SUMS` from the same GitHub release page you trust.

Then confirm the binary agrees:

```bash
chmod +x yggaro-server-linux-amd64
./yggaro-server-linux-amd64 -version
```

The version it prints is compiled in, together with the commit. A binary that disagrees with `VERSION.txt` is not the one we published.

## 2. Read the provenance

```json
{
  "version": "1.0.3",
  "tag": "v1.0.3",
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

Building the same commit **with the same Go toolchain** produces a byte-identical server binary, because every timestamp and identifier is derived from the commit rather than from the clock. So a release can be checked by rebuilding and comparing the binary's checksum with its line in `SHA256SUMS`. The other files follow the same rule, but the SBOM also records the version of the tool that generated it, so it matches only when that tool matches too.

The toolchain qualifier is not boilerplate. The compiler version affects the binary, and we do not pin the build environment beyond recording it: `PROVENANCE.json` names the exact `goVersion` used, and that is the one to rebuild with. A different Go version may well produce a different, equally valid binary.

Within that scope it is enforced rather than hoped for: the release test suite builds twice with a delay and fails if anything differs. That test is how we found a build embedding wall-clock time in three separate artifacts — including the SBOM, which we would otherwise have missed.

The application source is not published in this repository, so rebuilding it is not a check you can run from these files. What you can hold us to is the published checksum of the binary.

## 4. Dependencies

`SBOM.cdx.json` is a CycloneDX 1.6 inventory of every module compiled in, for your own vulnerability scanning. We run `govulncheck` as part of the release build, and a failure there stops the release rather than warning about it.

An SBOM tells you what was included on the day it was built. It does not stay true as new vulnerabilities are published, which is the reason to keep your own scanning rather than to trust the file.

## What we do not claim

There is no code signature on the binaries for this edition yet, and no external penetration test or formal certification.

**The 1.0.x releases ship `linux/amd64` only.** We build arm64 internally, but we do not publish it: an artifact named like the others implies a level of support we cannot honour yet, and a sentence in the documentation is weaker than the expectation the file itself creates. If you need arm64, tell us — knowing that someone actually wants it is what would move it up the list.

Where any of this matters to you, say so; it helps us order the work.

## Related

[Upgrade](upgrade.md) · [Install](install.md) · [Security model](security.md) · [Versioning](../VERSIONING.md)
