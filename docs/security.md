# Security model

[English](security.md) · [Čeština](security.cs.md) · [Report a vulnerability](../SECURITY.md)

One server instance belongs to one organisation. The OS administrator, DNS/TLS control and database passphrase are trusted. Users are limited by role and project membership. An MCP client acts as a mapped application principal and cannot exceed that principal's RBAC rights.

- TLS terminates in built-in ACME or an explicitly configured reverse proxy.
- Database content **and attachment contents** are encrypted at rest under the same key; key material lives outside the data directory. Record identifiers and replication metadata stay readable so that indexing works, so filesystem and disk protection remain part of the picture rather than a substitute for it. See [data and privacy](data-and-privacy.md).
- The service runs under its own unprivileged account; the only privilege it keeps is binding ports 80/443 (`CAP_NET_BIND_SERVICE`), and systemd sandboxing leaves it write access to its data directory only. See [install](install.md).
- Secrets belong in a root-only environment file or secret manager, never Git, issues or logs.
- First administrator creation requires a bootstrap token. From 1.0.2 the server refuses to start on an empty database without one, and refuses to start without a database passphrase at all, instead of silently running unprotected.

Main controls cover first-user takeover, session/account theft, object-level authorisation, encrypted backups and overpowered MCP clients (expiring mandates, scopes, capabilities, data classes, confirmation and revocation).

No external penetration test or formal certification is claimed. Operators remain responsible for OS patches, firewall, DNS, TLS/proxy, offsite backups and secret access.
