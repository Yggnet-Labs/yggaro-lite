# Backup and restore

A useful backup includes a consistent database snapshot, attachments, the key directory and an independently stored passphrase.

```bash
YGGARO_DB_PASSPHRASE='…' /opt/yggaro/yggaro-server \
  -data /var/lib/yggaro -backup /srv/backup/yggaro.db
tar -C /var/lib/yggaro -czf /srv/backup/files.tgz files
tar -C /var/lib -czf /srv/backup/yggaro-keys.tgz yggaro-keys
```

Copy artifacts off the instance. Store `YGGARO_DB_PASSPHRASE` separately.

Restore only into an isolated directory first:

```bash
install -d -m 700 /srv/restore/yggaro /srv/restore/yggaro-keys
install -m 600 /srv/backup/yggaro.db /srv/restore/yggaro/yggaro.db
tar -C /srv/restore/yggaro -xzf /srv/backup/files.tgz
tar -C /srv/restore -xzf /srv/backup/yggaro-keys.tgz
YGGARO_KEYS=/srv/restore/yggaro-keys YGGARO_DB_PASSPHRASE='…' \
  /opt/yggaro/yggaro-server -data /srv/restore/yggaro -verify-restore
```

A zero exit proves technical readability, not business completeness. Record version, timestamp, hashes and drill result. Test restoration regularly.
