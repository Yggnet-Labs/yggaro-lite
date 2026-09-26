# Data and privacy

[English](data-and-privacy.md) · [Čeština](data-and-privacy.cs.md)

This page answers the question a buyer's IT and legal people ask first: **where does our data live, who can reach it, and how do we get it back out.** It describes the self-hosted server edition. For the hosted service, see [yggarolite.cz](https://yggarolite.cz).

## Where the data is

Everything the application stores is on your machine:

| What | Where |
|---|---|
| Database (SQLite) | `<data>/yggaro.db`, by default `/var/lib/yggaro` |
| Attachments | `<data>/files/` |
| Key material | `YGGARO_KEYS`, by default `/var/lib/yggaro-keys` — outside the data tree |
| TLS certificates | `<data>/acme/` when built-in ACME is used |

There is no external database server, no message broker and no cache to operate. The binary is pure Go, including the SQLite driver, so there is nothing to install alongside it.

## What is encrypted at rest

With `YGGARO_DB_PASSPHRASE` set — the production requirement — the content is encrypted with **XChaCha20-Poly1305** under a key held in the key directory and unlocked by the passphrase:

- **business content** — the record values and documents that carry your project, order, risk and decision data;
- **attachment contents**, with the same key;
- **stored secrets**, such as the organisation key and configured notification webhook URLs.

Readable in a stolen database file, by design, because indexing and replication need them: record identifiers, entity names, paths, device and clock metadata. In other words, a thief with only the file learns *that* records exist and how many — not what they say.

If the key does not match the data, the server **refuses to start** rather than writing over data it cannot read.

Two things follow, and they are the operator's job: protect the disk and the key directory with normal filesystem permissions, and **keep a copy of the passphrase off the server**. Without it, backups are permanently unreadable — that is the point of the encryption, and it applies to you as well.

## What leaves the machine

Nothing, unless you configure it. **The product contains no telemetry, no analytics and no update check**; it never calls home, and there is no setting that turns that on.

Outbound connections exist only for features you switch on:

| Destination | When | What is sent |
|---|---|---|
| Let's Encrypt | `-domain` is set (built-in TLS) | the domain name, for certificate issuance |
| Your notification webhook (Teams or compatible) | an administrator saves a webhook URL | the notification text |
| Your Discord webhook | an administrator saves a Discord webhook URL | the notification text |
| Microsoft Entra ID | the `YGGARO_OIDC_*` family is set | sign-in only |
| Microsoft Graph / SharePoint | the `YGGARO_GRAPH_*` family is set (preview) | the documents that integration is configured to exchange |

**MCP is inbound.** Your own AI client connects *to* the instance; the instance does not call any AI provider. No model runs inside this edition and application data is not sent to one by the product itself. What a connected client may read or change is bounded by that client's mapped rights — see [MCP permissions](mcp-permissions.md).

## Getting your data out

Two routes, one implementation, so both give the same package:

```bash
# From the application, as an administrator (see below for what it requires)
# POST /api/admin/export

# Or from the command line — this one also works on a stopped instance
# (as the service account — yggaro-admin, see install step 6; /srv/export must belong to yggaro)
yggaro-admin -export /srv/export/yggaro-export.zip
```

The ZIP contains `data/<entity>.json` for every exported entity, `files/` with attachments under their original names, and `manifest.json` stating exactly what is inside and how many records of each kind. It is plain JSON: readable without us, and without this software. From 1.0.3 it also contains every user's read state of discussions (`data/readmark.json`: who has read which thread up to which message) — the administrator who downloads the export sees it for all users, which the application itself does not show. It also contains the instance's whole security log (`data/_security_log.json`): sign-ins including failed attempts with their IP address, role, permission and password changes, exports and integration access, each entry hash-chained to the one before it. `manifest.json` → `security_log` gives the number of entries and whether the chain verified, and `README.txt` in the package describes how to recompute it yourself and what the chain cannot show. The log covers the whole history without a time limit and includes people who are not users — the address and the identifier typed by anyone who tried to sign in — so whoever downloads the export handles it as personal data. Entries written by versions up to 1.0.2 may contain a notification webhook address with its token; the package lists them and says so.

The in-application route is deliberately harder to trigger than an ordinary read, because one call takes the whole contents of the company: it needs an administrator who additionally holds the `data.export.full` right and, because the package carries the security log, the `audit.view` right, a re-entry of the password, and a valid CSRF header. It builds the package from a consistent snapshot into a temporary file and verifies completeness before sending, so a truncated export is never served as success. Concurrent exports get `429`.

If attachments could not be read, the manifest says so and marks the package incomplete rather than letting it look whole.

## Deleting data

Individual records are deleted in the application. To remove everything, delete the data directory, the key directory and the backups — and destroy the passphrase. Because the content is encrypted under that key, destroying the key and its copies renders any missed copy unreadable.

The software does not expire or delete anything on its own. Retention is your policy, and your schedule.

## What we can see

Nothing. This is software you run. We have no access to your instance, receive no data from it, and cannot recover your passphrase.

## Related

[Security model](security.md) · [Configuration](configuration.md) · [Back up and restore](backup-restore.md) · [MCP permissions](mcp-permissions.md)
