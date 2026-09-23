# Backup and restore

A useful backup includes a consistent database snapshot, attachments, the key directory and an independently stored passphrase.

```bash
install -d -m 700 -o yggaro -g yggaro /srv/backup
yggaro-admin -backup /srv/backup/yggaro.db
tar -C /var/lib/yggaro -czf /srv/backup/files.tgz files
tar -C /var/lib -czf /srv/backup/yggaro-keys.tgz yggaro-keys
```

`yggaro-admin` (see [install, step 6](install.md#6-maintenance-commands-run-as-the-service-account)) runs the command under the service account with the service's secrets, so the passphrase never appears on a command line. `-backup` is consistent and works while the instance is running.

Copy artifacts off the instance. Store `YGGARO_DB_PASSPHRASE` separately.

`-verify-restore` reads a standalone database snapshot without modifying it.
It rejects a nonempty `yggaro.db-wal`, rather than silently checking an older
main file. Use the snapshot produced by `-backup`; never delete a live WAL
to make the check pass. A missing source database is an error, not a new
instance. A zero exit does not check attachment files or business completeness.

Restore only into an isolated directory first:

```bash
install -d -m 700 -o yggaro -g yggaro /srv/restore /srv/restore/yggaro
install -m 600 -o yggaro -g yggaro /srv/backup/yggaro.db /srv/restore/yggaro/yggaro.db
tar -C /srv/restore/yggaro -xzf /srv/backup/files.tgz
tar -C /srv/restore -xzf /srv/backup/yggaro-keys.tgz
chown -R yggaro:yggaro /srv/restore
YGGARO_KEYS=/srv/restore/yggaro-keys yggaro-admin -data /srv/restore/yggaro -verify-restore
```

This reads the passphrase from `/etc/yggaro-server.env`. To prove that the passphrase stored *off the server* opens the backup — the case that matters after losing the machine — run the drill on a scratch machine with that copy in its own environment file.

A zero exit proves technical readability, not business completeness. Record version, timestamp, hashes and drill result. Test restoration regularly.
