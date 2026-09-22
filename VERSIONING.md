# Versioning and support

Yggaro Lite uses `MAJOR.MINOR.PATCH` semantic versioning.

- **MAJOR**: incompatible product, API, data or operational changes.
- **MINOR**: backward-compatible capabilities.
- **PATCH**: backward-compatible fixes, including security fixes.
- `-devN` and `-rcN` are pre-release builds and are not production releases.

The first production release is `1.0.0`. A release requires a clean `X.Y.Z` tag, matching version reported by the binary and `/healthz`, a changelog entry, tested upgrade/installation instructions and verifiable release artifacts.

Until a longer policy is announced, only the latest production release receives fixes. Upgrade notes will identify breaking or irreversible migrations. Support status is a product commitment; a Git tag alone does not make an unsupported development build a release.
