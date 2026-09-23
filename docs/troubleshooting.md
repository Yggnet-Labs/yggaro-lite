# Troubleshooting

[English](troubleshooting.md) · [Čeština](troubleshooting.cs.md)

Start here:

```bash
systemctl status yggaro-server
journalctl -u yggaro-server --since '15 minutes ago'
curl -fsS https://your-domain.example/healthz
```

> **Note on language.** The web application speaks your language, but the server's startup and command-line messages are currently **Czech only**. The exact strings are quoted below so you can match what you see in the journal.

## The certificate is never issued

Almost always one of three things, in this order of likelihood:

1. **The domain is behind a proxy.** TLS terminates *on your server*. If the DNS record is proxied — an orange cloud on Cloudflare, for example — the challenge never reaches the instance. Set the record to **DNS only**.
2. **Port 80 is closed.** ACME needs it, even though the application serves on 443. `ufw allow 80/tcp`.
3. **The A record does not point at this machine.** Check from outside, not from the server: `dig +short your-domain.example`.

Let's Encrypt rate-limits repeated failures for the same name. Fix the cause before retrying, or you will be waiting on the limit rather than on the fix.

Behind your own reverse proxy, do not use `-domain` at all — see below.

## The server will not start

**`✗ Server odmítl start: …`, exit code 78** — the server refused its configuration before serving anything (from 1.0.2). The word after the colon names the rule; systemd leaves the service in `failed` and does not restart it:

| Code in the message | Meaning | What to do |
|---|---|---|
| `no-db-passphrase` | `YGGARO_DB_PASSPHRASE` is not set | Set it in `/etc/yggaro-server.env`. **If the message names a key file, do not** — the instance was created without a passphrase; see [upgrade](upgrade.md#from-100-or-101-to-102) |
| `no-bootstrap-token` | empty database and no `YGGARO_BOOTSTRAP_TOKEN` | set the token, restart, enter it in the setup wizard |
| `passphrase-and-local-key` | both the passphrase and `YGGARO_ALLOW_LOCAL_KEY` are set | keep only the one your instance was created with |
| `no-existing-local-key` | `YGGARO_ALLOW_LOCAL_KEY` is set but there is no key on this machine | the acknowledgement is only for an existing key; a new one is never created. Set a passphrase, or check `YGGARO_KEYS` |
| `invalid-local-key` | the local key exists but is damaged or unreadable | nothing was overwritten. Restore the key directory from backup |
| `no-encrypt-in-public-mode` | `-no-encrypt` together with a public setup | remove `-no-encrypt`; it is for local diagnostics only |

`database-state-unknown` (exit code 1, restarted) means the server could not tell whether the instance already has an administrator. It will not guess; the rest of the line names the database error.

**`✗ Chybný šifrovací klíč pro tuto databázi`** — the key does not open this database. The server stops on purpose instead of writing over data it cannot read. Check that `YGGARO_DB_PASSPHRASE` is the one this instance was created with and that `YGGARO_KEYS` points at the right key directory. A restored backup needs *both* the key directory and the original passphrase.

**`nelze otevřít databázi`** / **`nelze vytvořit datový adresář`** — filesystem, not cryptography: permissions, ownership, or a full disk. `df -h` and `ls -ln /var/lib/yggaro`. Everything there must belong to `yggaro`; a maintenance command run as root instead of through `yggaro-admin` leaves root-owned files behind. Fix with `chown -R yggaro:yggaro /var/lib/yggaro`.

**`inicializace selhala`** — the database opened but setup did not finish. The rest of the line names the cause; the journal entry immediately before it is usually the real story.

## Nobody can create the first administrator

Setup asks for the activation token from `YGGARO_BOOTSTRAP_TOKEN` (`sed -n 's/^YGGARO_BOOTSTRAP_TOKEN=//p' /etc/yggaro-server.env`). From 1.0.2 an empty database without the token does not even start — that is deliberate, so that a stranger who finds a fresh instance cannot claim your organisation first. Set it in `/etc/yggaro-server.env` and restart.

## Checksum verification says "No such file or directory"

`SHA256SUMS` covers every artifact of the release, and you probably downloaded only the binary. Check exactly that file:

```bash
grep '  yggaro-server-linux-amd64$' SHA256SUMS | sha256sum -c -
```

It must print `yggaro-server-linux-amd64: OK`. Do not rely on `--ignore-missing` alone: it also succeeds when the binary was not checked at all.

## Behind a reverse proxy

Three symptoms, three flags — see [configuration](configuration.md):

| Symptom | Cause | Fix |
|---|---|---|
| Audit log and rate limits show `127.0.0.1` for everyone | the client IP is in `X-Forwarded-For`, and is not trusted by default | `-trust-proxy` (honoured only when the direct connection is from loopback) |
| Sessions drop, or the browser will not keep the cookie | the cookie is not marked `Secure` because the instance itself is not on TLS | `-secure-cookies` |
| Requests are rejected on the host name | the public name is not in the host allowlist | `-public-host your-domain.example` |

Rate limiting and audit are only as good as the IP they see. A proxy without `-trust-proxy` makes every visitor look like one very busy local user.

## An administrator is locked out

Break-glass recovery needs access to the machine and the key — which is the point:

```bash
systemctl stop yggaro-server
yggaro-admin -reset-password admin@your-company.example
systemctl start yggaro-server
```

`yggaro-admin` is the helper from [install, step 6](install.md#6-maintenance-commands-run-as-the-service-account).

It prints the new password unless you pass `-new-password`.

## An MCP client will not connect

Work outwards from the instance: is MCP on (`YGGARO_MCP=1`), is the client using OAuth (`YGGARO_MCP_OAUTH=1`) or a token issued with `-mcp-token`, and does the mapped principal actually hold the rights for what the client is trying to do? A refusal that looks like a connection problem is often a permissions answer. See [MCP](mcp.md) and [MCP permissions](mcp-permissions.md).

## A backup that may not be good

Do not find out during an incident:

```bash
YGGARO_KEYS=/srv/restore/yggaro-keys yggaro-admin -data /srv/restore/yggaro -verify-restore
```

Exit code zero proves the data is readable with that key. It does not prove the backup is recent or complete — check the record counts it prints against what you expect. See [back up and restore](backup-restore.md).

## Still stuck

[SUPPORT.md](../SUPPORT.md) says where to ask. Include the version (`yggaro-server -version`), the journal lines around the failure, and what you changed last. **Redact secrets and customer data before posting anything in public.** Vulnerabilities go privately to [SECURITY.md](../SECURITY.md), never to a public issue.
