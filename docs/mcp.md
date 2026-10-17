# Connect an AI client through MCP

[English](mcp.md) · [Čeština](mcp.cs.md) · [Tool list and limits](mcp-tools.md) · [Permission model](mcp-permissions.md)

MCP lets a customer's own AI client work with Yggaro Lite. It is not “AI inside Yggaro Lite”: no model is bundled and the server does not choose a model or send data to one by itself.

**It is entirely optional and off by default.** Yggaro Lite is fully functional without any AI: nothing here is required to run the product, and leaving MCP off costs you no other feature. It stays off until an operator explicitly switches it on.

## Enable the endpoint

Add `YGGARO_MCP=1` to the service environment and restart. The Streamable HTTP endpoint is `https://your-domain.example/mcp`. Built-in OAuth is opt-in with `YGGARO_MCP_OAUTH=1`; otherwise issue an opaque bearer mandate locally:

```bash
yggaro-admin -mcp-token admin@example.com -mcp-scopes 'mcp.read'
```

`yggaro-admin` runs the command under the service account ([install, step 6](install.md#6-maintenance-commands-run-as-the-service-account)). The plaintext token is shown once. Store it in the AI client's secret storage, never in Git or chat. Configure the client with the MCP URL and `Authorization: Bearer <token>`. Start read-only and ask the client for the capability description before using tools.

## Operational lifecycle

Every client access maps to a local principal and mandate. A token mandate is read-only by default and expires after 90 days (maximum 365); a mandate bound to a sign-in identity (OIDC binding) has no expiry in the 1.0 series and must be revoked explicitly. A superadmin can revoke any mandate immediately. Application RBAC still applies. Review active mandates, their data classes and audit events regularly; revoke access on device loss, staff departure or unexpected activity.

Test after configuration: discover tools, read an allowed object, confirm a forbidden write fails, then revoke a test mandate and confirm the next call fails. See [permissions](mcp-permissions.md) and [security](security.md).

## Known limitation 1.0.5: revoking the access of a connected AI client (OAuth)

*Added on 17 October 2026, after the 1.0.5 release. The 1.0.5 code and released files are unchanged.*

**What can happen.** The "Active access" overview lets you revoke the access of an AI client connected through OAuth (the "OAuth token family" row). Revoking that row **can fail** when no access-token record is left for the family. Access tokens are valid for 15 minutes and expired records are cleaned up over time, so this mainly affects a client that has been holding only its long-lived refresh token for a while. On failure the row shows "×" and the message "Some revocations failed". The client's access is **not** revoked and the client can keep renewing it.

**Workaround.** Revoke the client's whole mandate (permission). Only a superadmin can do this:
1. Sign in as a superadmin.
2. Open **Administration** in the left menu.
3. Choose the **Settings** tab.
4. In the **MCP mandates** panel find the client's mandate row (columns Principal, Permissions, Data classes, Valid until, State, Note).
5. Click **Revoke** and confirm "Really revoke this mandate? The client stops working immediately."

You can also revoke a mandate in **Administration → Permissions → Active access**: tick the "MCP mandate" row, click **Revoke selected** and enter your current password. The filter **"Only accounts without local TOTP"** is ticked by default and hides users with local TOTP. If you do not see the mandate row, untick it.

**Please note.** In 1.0.5 the interface does not link an OAuth family row to its mandate row (the mandate identifier is not shown on the family row); identify the mandate by user, permissions and note. If a user has several mandates and you cannot tell which one belongs to the client, revoke all of that user's mandates and reconnect the other clients.

**What holds after the mandate is revoked.** The client can no longer renew access and requests with a still-valid access token are rejected. Verified by a test against the 1.0.5 source (renewal after mandate revocation fails; the row disappears from the overview) and by reading the access-token verification code; not verified on a running instance.

**Fix:** planned for version 1.0.6.
