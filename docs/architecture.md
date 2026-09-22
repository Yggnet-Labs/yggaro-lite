# Architecture

What actually runs on the machine, for the person who has to approve it.

## One process, one organisation

Yggaro Lite Server is a **single Go binary**. The web interface, its fonts and assets are compiled into it, and so is the SQLite engine — the driver is pure Go, so there is no cgo and no shared library to match. One instance serves one organisation.

There is nothing else to operate: no separate database server, no message broker, no cache, no container runtime required. An instance is a binary, a data directory, a key directory and a systemd unit.

```
                       ┌──────────────────────────────┐
  browser ─── 443 ───▶ │                              │
                       │      yggaro-server           │   /var/lib/yggaro
  AI client ── /mcp ──▶│  ┌────────────────────────┐  │   ├── yggaro.db   (SQLite, WAL)
                       │  │ web UI (embedded)      │  │   ├── files/      (attachments)
  WebDAV ──── /dav ───▶│  │ HTTP API · MCP · WebDAV│  │   └── acme/       (certificates)
                       │  │ SQLite (pure Go)       │  │
       ACME ◀── 80 ────│  └────────────────────────┘  │   /var/lib/yggaro-keys
                       └──────────────────────────────┘   └── key material
```

## Storage

The database is SQLite in WAL mode, in the data directory. Attachments are separate files under `files/`, encrypted with the same key as the database content. Key material lives in its own directory **outside** the data tree, so a backup of one is not automatically a backup of the other — which is deliberate.

See [data and privacy](data-and-privacy.md) for exactly which fields are encrypted and which stay readable.

## How requests arrive

Two supported shapes, and you pick one:

**Built-in TLS.** Give the instance `-domain`; it obtains and renews its own certificate and serves 443, with 80 kept for the ACME challenge and a redirect. The DNS record must be **DNS only** — TLS terminates here, so a proxy in front breaks issuance.

**Behind your reverse proxy.** Leave `-domain` unset; the instance listens on `-listen` (loopback by default). The proxy terminates TLS and must pass the client IP, and you must tell the instance to trust it with `-trust-proxy`, to mark cookies `Secure` with `-secure-cookies`, and to accept the public name with `-public-host`. Skipping those is the most common misconfiguration — see [troubleshooting](troubleshooting.md).

## Interfaces

| Surface | Purpose |
|---|---|
| Web UI and HTTP API | the application itself |
| `/mcp` | your own AI client, off unless enabled; scoped and audited — [MCP](mcp.md) |
| `/dav/…` | WebDAV access to a document, for editing in a desktop application |
| `/healthz` | liveness and version, for your monitoring |

## What it talks to

By default: Let's Encrypt, and nothing else. Notification webhooks, Microsoft Entra sign-in and SharePoint are each off until configured. There is no telemetry and no update check. The full list is in [data and privacy](data-and-privacy.md).

## Scaling

This edition scales by giving each organisation its own instance, not by clustering one. A small machine (2 vCPU, 4 GB RAM) serves a normal team; growth is handled by the machine, and separation by the instance boundary. If you need one deployment serving many organisations, that is a different product.

## Related

[Configuration](configuration.md) · [Security model](security.md) · [Operations](operations.md)
