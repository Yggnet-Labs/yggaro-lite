# FAQ

[English](faq.md) · [Čeština](faq.cs.md)

**Is this Mesh?** No. This release is the single-tenant server edition. Mesh is deferred.

**Is it open source?** No. It is source-available under FSL-1.1-ALv2. Internal self-hosting is permitted; a competing hosted service is not.

**Does it send data to AI?** No model runs inside this edition. You may connect your own AI client through MCP and explicitly grant limited access.

**Where is data stored?** In the instance data directory and attachment tree on your machine. Optional integrations send only data needed for their configured purpose.

**Can I back up or export?** Yes. See [backup and restore](backup-restore.md); the server also provides a readable ZIP export.

**Supported self-host platform?** Ubuntu 24.04 on `linux-amd64` for 1.0.0, unless release notes say otherwise.

**Help?** See [SUPPORT.md](../SUPPORT.md). Report security issues privately.
