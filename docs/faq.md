# FAQ

[English](faq.md) · [Čeština](faq.cs.md)

**Is this Mesh?** No. This release is the single-tenant server edition. Mesh is deferred.

**Is it open source?** No. The server binary is under FSL-1.1-ALv2. The application source is not in this repository. Internal self-hosting of that binary is permitted; a competing hosted service is not.

**Does it send data to AI?** No model runs inside this edition. You may connect your own AI client through MCP and explicitly grant limited access.

**Where is data stored?** In the instance data directory and attachment tree on your machine. Optional integrations send only data needed for their configured purpose.

**Can I back up or export?** Yes. See [backup and restore](backup-restore.md); the server also provides a readable ZIP export.

**Supported self-host platform?** Ubuntu 24.04 on `linux-amd64` for the 1.0.x releases, unless release notes say otherwise.

**Does it send anything to you?** No. There is no telemetry, no analytics and no update check, and no setting that turns one on. The only connection it makes on its own is to Let's Encrypt for its certificate. See [data and privacy](data-and-privacy.md).

**How do we get our data out?** A ZIP of plain JSON plus your attachments, from the application or from the command line — the command-line route works even on a stopped instance. It is readable without this software. See [data and privacy](data-and-privacy.md).

**What if you stop developing it?** Your data is already on your machine and exports to plain JSON. The licence converts each version to Apache-2.0 two years after that version is made available — that is part of the licence you get today, not a promise about the future. See [LICENSING.md](../LICENSING.md).

**How big a machine do we need?** A small one: 2 vCPU and 4 GB RAM serves a normal team. This edition scales by giving each organisation its own instance rather than by clustering one.

**What is not in 1.0.x yet?** Orders can be created and changed in the application, but through MCP they are read-only for now, and projects can be created but not listed or updated — the [MCP roadmap](mcp-roadmap.md) says what comes next and in what order. Mesh and Lite AI are separate products with no release date. The binaries are checksummed but not code-signed.

**Help?** See [SUPPORT.md](../SUPPORT.md). Report security issues privately.
