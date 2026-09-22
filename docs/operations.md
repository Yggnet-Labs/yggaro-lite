# Operations

Day-to-day running of an instance. Install is in [install](install.md); this is everything after.

## Is it healthy

```bash
curl -fsS https://your-domain.example/healthz
systemctl status yggaro-server
journalctl -u yggaro-server --since today
```

`/healthz` reports liveness and the running version. Point your existing monitoring at it — and alert on the version too, not only on the status: a machine that quietly stayed on an old binary is the failure you find out about late.

## Routine

| How often | What |
|---|---|
| Continuously | `/healthz` from your monitoring; disk space on the data volume |
| Daily | backup runs, and it produced a file of a plausible size |
| Each release | read the notes, back up, upgrade, smoke-test — [upgrade](upgrade.md) |
| Quarterly | a real restore drill into a scratch directory — [back up and restore](backup-restore.md) |
| Quarterly | review who has an account, who is an administrator, and which MCP clients are still authorised |

The restore drill is the one people skip. An untested backup is a belief, not a backup.

## Backups

Three things, all of them: the database snapshot, `files/`, and the key directory. And, stored somewhere else entirely, the passphrase. See [back up and restore](backup-restore.md).

```bash
YGGARO_DB_PASSPHRASE='…' /opt/yggaro/yggaro-server \
  -data /var/lib/yggaro -backup /srv/backup/yggaro-$(date +%F).db
```

`-backup` is consistent and works while the instance is running, so it does not need a maintenance window.

## Users and access

Accounts, roles and project membership are managed in the application. Two things worth knowing at the operations level:

- The **observer** role can never write. That is enforced in code, not by a permission checkbox someone can tick by accident.
- **Exporting the whole instance** is a right of its own (`data.export.full`) on top of being an administrator, and it re-asks for the password. Grant it deliberately.

If an administrator is locked out, recovery requires shell access to the machine and the key — see [troubleshooting](troubleshooting.md).

## Audit

The application keeps an audit trail of who changed what, and alongside it a **security log** covering roughly a hundred kinds of event: sign-ins and every reason a sign-in was refused, role and permission changes, password resets and recovery codes, exports — including the ones that were denied or came out incomplete — file operations, OAuth client lifecycle and replay detection, notification configuration, and MCP mandates, disclosures and refusals.

That log is **hash-chained**: each entry commits to the one before it, so a deleted or edited entry stops the chain verifying. `GET /api/seclog` returns the recent entries together with `intact`, `count` and `brokenSeq`, which is what to watch — an `intact` that turns false is a much stronger signal than anything in the entries themselves.

When you enable MCP or put the instance behind a proxy, check that the log shows real client addresses rather than `127.0.0.1`; if it does not, the instance is not trusting your proxy yet.

## Secrets

Secrets belong in the root-only environment file or your secret manager — never in Git, an issue, or a log. Rotate a notification webhook by replacing it in the application. Rotating the database passphrase is not a routine operation; treat it as a migration, with a verified backup first.

## Related

[Configuration](configuration.md) · [Upgrade](upgrade.md) · [Troubleshooting](troubleshooting.md) · [Security model](security.md)
