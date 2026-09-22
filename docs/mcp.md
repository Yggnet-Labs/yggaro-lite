# Connect an AI client through MCP

[English](mcp.md) · [Čeština](mcp.cs.md) · [Tool list and limits](mcp-tools.md) · [Permission model](mcp-permissions.md)

MCP lets a customer's own AI client work with Yggaro Lite. It is not “AI inside Yggaro Lite”: no model is bundled and the server does not choose a model or send data to one by itself.

## Enable the endpoint

Add `YGGARO_MCP=1` to the service environment and restart. The Streamable HTTP endpoint is `https://your-domain.example/mcp`. Built-in OAuth is opt-in with `YGGARO_MCP_OAUTH=1`; otherwise issue an opaque bearer mandate locally:

```bash
YGGARO_DB_PASSPHRASE='…' /opt/yggaro/yggaro-server \
  -data /var/lib/yggaro -mcp-token admin@example.com -mcp-scopes 'mcp.read'
```

The plaintext token is shown once. Store it in the AI client's secret storage, never in Git or chat. Configure the client with the MCP URL and `Authorization: Bearer <token>`. Start read-only and ask the client for the capability description before using tools.

## Operational lifecycle

Every client access maps to a local principal and mandate. The default mandate is read-only, expires after 90 days (maximum 365), and can be revoked immediately by a superadmin. Application RBAC still applies. Review active mandates, their data classes and audit events regularly; revoke access on device loss, staff departure or unexpected activity.

Test after configuration: discover tools, read an allowed object, confirm a forbidden write fails, then revoke a test mandate and confirm the next call fails. See [permissions](mcp-permissions.md) and [security](security.md).
