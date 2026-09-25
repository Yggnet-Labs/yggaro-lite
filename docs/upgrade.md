# Upgrade

Read release notes and `CHANGELOG.md`; back up and verify restore first.

```bash
bash -euo pipefail <<'STEP'
grep '  yggaro-server-linux-amd64$' SHA256SUMS | sha256sum -c -
systemctl stop yggaro-server
cp -p /opt/yggaro/yggaro-server /opt/yggaro/yggaro-server.previous
install -m 755 yggaro-server-linux-amd64 /opt/yggaro/yggaro-server
/opt/yggaro/yggaro-server -version
systemctl start yggaro-server
STEP
timeout 90 bash -c 'until curl -fsS https://lite.example.com/healthz; do sleep 3; done'
journalctl -u yggaro-server --since '10 minutes ago'
```

The block stops at the first failure: with a checksum that does not match, the running service is not even stopped.

Confirm the version, login and a representative read/write path. If smoke checks fail, restore the previous binary. Do not put an older database over a migrated database unless release notes explicitly allow it; use the pre-upgrade backup.

## From 1.0.0 or 1.0.1 to 1.0.2

1.0.2 changes two things that affect an existing installation:

1. **The server stops running as root.** Earlier versions of the [install guide](install.md) started the service as root. From 1.0.2 it runs under its own account `yggaro`, and maintenance commands go through `yggaro-admin`.
2. **The server refuses unsafe configuration instead of accepting it.** Without `YGGARO_DB_PASSPHRASE` it does not start, and on an empty database it does not start without `YGGARO_BOOTSTRAP_TOKEN` either. An instance that already has its first administrator does not need the token.

### First, find out how your instance is protected

```bash
grep -c '^YGGARO_DB_PASSPHRASE=.' /etc/yggaro-server.env
ls -l /var/lib/yggaro-keys
```

- `1` — the instance uses a passphrase, as the install guide recommends. Continue below.
- `0` and a `*.key` file in `/var/lib/yggaro-keys` — the instance was created **without a passphrase** and its data is encrypted with that key file. **Do not add a passphrase:** it would produce a different key and the data would not open. Instead add `YGGARO_ALLOW_LOCAL_KEY=1` to `/etc/yggaro-server.env`. That is an explicit acknowledgement that the key lives on the same machine as the data; back up the key directory separately. The server only ever *reads* that existing key — it never creates a new one or overwrites a damaged one.

### Back up the old installation first

The procedure in [backup and restore](backup-restore.md) already assumes the `yggaro` account and the `yggaro-admin` helper, which do not exist yet. Back up the old root installation with its own binary, as root, while it still runs — and prove the copy opens:

```bash
bash -euo pipefail <<'STEP'
B=/srv/backup/pre-1.0.2
install -d -m 700 "$B"
/opt/yggaro/yggaro-server -data /var/lib/yggaro -backup "$B/yggaro.db"
if [ -d /var/lib/yggaro/files ]; then tar -C /var/lib/yggaro -czf "$B/files.tgz" files; fi
if [ -d /var/lib/yggaro-keys ]; then tar -C /var/lib -czf "$B/yggaro-keys.tgz" yggaro-keys; fi
cp -p /etc/yggaro-server.env "$B/yggaro-server.env"
cp -p /opt/yggaro/yggaro-server "$B/yggaro-server.previous"
cp -p /etc/systemd/system/yggaro-server.service "$B/yggaro-server.service.previous"
R=$(mktemp -d)
trap 'rm -rf "$R"' EXIT
install -m 600 "$B/yggaro.db" "$R/yggaro.db"
if [ -d /var/lib/yggaro-keys ]; then cp -a /var/lib/yggaro-keys "$R/keys"; else mkdir "$R/keys"; fi
( set -a; . /etc/yggaro-server.env; set +a
  YGGARO_KEYS="$R/keys" /opt/yggaro/yggaro-server -data "$R" -verify-restore )
STEP
```

It must end with `✓ Databáze se otevřela a je čitelná.` On an installation **without** a passphrase the old binary also prints a warning to set `YGGARO_DB_PASSPHRASE`; ignore it here — for such an installation 1.0.2 is confirmed with `YGGARO_ALLOW_LOCAL_KEY=1`, and adding a passphrase would make the existing data unreadable (see above). The drill runs on a copy, with a copy of the key directory, so it cannot change the live instance. `$B` now holds the database snapshot, attachments, key directory, environment file, binary and unit — **copy it off the machine**; the environment file contains the passphrase.

### Migration

```bash
bash -euo pipefail <<'STEP'
grep '  yggaro-server-linux-amd64$' SHA256SUMS | sha256sum -c -
test -s /srv/backup/pre-1.0.2/yggaro.db
systemctl stop yggaro-server
cp -p /opt/yggaro/yggaro-server /opt/yggaro/yggaro-server.previous
id -u yggaro >/dev/null 2>&1 || useradd --system --home-dir /var/lib/yggaro --no-create-home --shell /usr/sbin/nologin yggaro
install -d -m 700 /var/lib/yggaro-keys
chown -R yggaro:yggaro /var/lib/yggaro /var/lib/yggaro-keys
chmod 700 /var/lib/yggaro /var/lib/yggaro-keys
install -m 755 yggaro-server-linux-amd64 /opt/yggaro/yggaro-server
/opt/yggaro/yggaro-server -version
STEP
```

The block stops before touching the running service when the checksum does not match or the backup from the previous step is missing.

Replace `/etc/systemd/system/yggaro-server.service` with the unit from [install, step 4](install.md#4-systemd-service), keeping your own `-domain` and `-acme-email`. Install the `yggaro-admin` helper from [step 6](install.md#6-maintenance-commands-run-as-the-service-account). Then:

```bash
systemctl daemon-reload
systemctl start yggaro-server
timeout 90 bash -c 'until curl -fsS https://lite.example.com/healthz; do sleep 3; done'
systemctl status yggaro-server
ps -o user=,pid=,args= -C yggaro-server
bash -euo pipefail <<'CHECK'
R=$(mktemp -d /var/lib/yggaro-restore-check.XXXXXX)
trap 'rm -rf -- "$R"' EXIT
chown yggaro:yggaro "$R"
yggaro-admin -backup "$R/yggaro.db"
yggaro-admin -data "$R" -verify-restore
CHECK
curl -fsS https://lite.example.com/healthz
```

The restore check above reads a fresh snapshot, not the running database; it checks database readability, not attachments or business completeness. Its temporary directory is removed on success or failure. `ps` must show `yggaro`. If the service ends in `failed`, `journalctl -u yggaro-server -n 20` states the reason in one message and systemd does not keep restarting it (exit code `78`); see [troubleshooting](troubleshooting.md#the-server-will-not-start).

### Rollback

Keep the new unit and file ownership; only put the previous binary back:

```bash
systemctl stop yggaro-server
install -m 755 /opt/yggaro/yggaro-server.previous /opt/yggaro/yggaro-server
systemctl start yggaro-server
```

If the data itself is damaged, restore from `/srv/backup/pre-1.0.2` as described in [backup and restore](backup-restore.md), under the unit that was in place when the backup was taken.

1.0.1 runs under the `yggaro` account and the same unit, and reads data written by 1.0.2 — 1.0.2 does not change the data format. It ignores `YGGARO_ALLOW_LOCAL_KEY`, which is harmless. Going back to the old root unit is not recommended: files the service creates as root would have to be handed back to `yggaro` by hand before the next upgrade.
