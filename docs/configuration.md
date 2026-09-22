# Configuration

Yggaro Lite Server accepts flags shown by `yggaro-server -help`. Prefer a root-readable environment file for secrets.

| Setting | Default | Purpose |
|---|---|---|
| `-data` / `YGGARO_DATA` | `/var/lib/yggaro` | Database and attachments (`files/`) |
| `YGGARO_KEYS` | `/var/lib/yggaro-keys` | Key material outside the data tree |
| `YGGARO_DB_PASSPHRASE` | none | Protects the at-rest database key; production requirement |
| `YGGARO_BOOTSTRAP_TOKEN` | none | Required secret for first administrator bootstrap |
| `-domain` | none | Public host; enables built-in ACME TLS on 80/443 |
| `-acme-email` | none | Let's Encrypt contact |
| `-listen` | `127.0.0.1:7456` | HTTP listener when `-domain` is absent |
| `-public-host` | none | Host allowlist behind a reverse proxy |
| `-secure-cookies` | false | Required behind a TLS-terminating proxy |
| `-trust-proxy` | false | Trust X-Forwarded-For only from a loopback proxy |
| `YGGARO_MCP=1` | off | Enable `/mcp`; see [MCP](mcp.md) |
| `YGGARO_MCP_OAUTH=1` | off | Enable embedded OAuth for MCP |
| `YGGARO_MCP_OAUTH_WRITE_HIGH=1` | off | Let OAuth consent request the pre-approved high-impact write scope; keep off unless explicitly required |

Optional Microsoft Entra SSO requires all of `YGGARO_OIDC_TENANT`, `YGGARO_OIDC_CLIENT_ID` and `YGGARO_OIDC_CLIENT_SECRET`, plus a known public host.

SharePoint/Graph integration is optional and should be treated as preview unless your release notes explicitly support it. It requires the complete family `YGGARO_GRAPH_TENANT`, `YGGARO_GRAPH_CLIENT_ID`, `YGGARO_GRAPH_CLIENT_SECRET` and `YGGARO_GRAPH_SITE`; setting only part of the family does not enable the integration. `YGGARO_MCP_OAUTH_COMPAT=1` is a narrow compatibility switch for affected MCP clients, not a normal production default.

Treat every secret, token and the DB passphrase as sensitive.

Never use `-no-encrypt` in production. Do not expose the plain HTTP listener directly to the internet. After a change, check `/healthz`, the version, login and the audit log.
