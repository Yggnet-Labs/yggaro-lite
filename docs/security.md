# Security model

[English](security.md) · [Čeština](security.cs.md) · [Report a vulnerability](../SECURITY.md)

One server instance belongs to one organisation. The OS administrator, DNS/TLS control and database passphrase are trusted. Users are limited by role and project membership. An MCP client acts as a mapped application principal and cannot exceed that principal's RBAC rights.

- TLS terminates in built-in ACME or an explicitly configured reverse proxy.
- Database values are encrypted at rest; key material lives outside the data directory. Attachments and operational metadata still require filesystem/disk protection.
- Secrets belong in a root-readable environment file or secret manager, never Git, issues or logs.
- First administrator creation requires a bootstrap token.

Main controls cover first-user takeover, session/account theft, object-level authorisation, encrypted backups and overpowered MCP clients (expiring mandates, scopes, capabilities, data classes, confirmation and revocation).

No external penetration test or formal certification is claimed. Operators remain responsible for OS patches, firewall, DNS, TLS/proxy, offsite backups and secret access.
