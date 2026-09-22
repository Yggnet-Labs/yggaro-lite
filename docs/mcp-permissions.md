# MCP permissions

[English](mcp-permissions.md) · [Čeština](mcp-permissions.cs.md)

Authentication (OAuth or bearer token) only identifies an MCP mandate. Authorisation is the intersection of:

1. mandate expiry and revocation state;
2. the mapped user's application RBAC and object membership;
3. broad scopes (`mcp.read`, legacy `mcp.write`, `mcp.write.high`);
4. domain capabilities such as task, chat, document, decision and deliverable operations;
5. optional allowed data classes;
6. `confirm:true` for high-impact actions unless the mandate explicitly has `mcp.write.high`.

Read-only is the safe default. Grant domain capabilities individually. Do not use `all` or `mcp.write.high` for routine clients. Creating/proposing and deciding/accepting are deliberately separate capabilities; a client allowed to propose a decision need not be allowed to decide it.

Tokens are stored as hashes and plaintext is returned once. Mandates default to 90 days and are capped at 365. Deleting a token from the client is not revocation: revoke the mandate server-side and confirm a subsequent call fails. Superadmin issuance, class changes and revocation are security-audited.
