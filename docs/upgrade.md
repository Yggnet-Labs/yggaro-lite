# Upgrade

Read release notes and `CHANGELOG.md`; back up and verify restore first.

```bash
grep '  yggaro-server-linux-amd64$' SHA256SUMS | sha256sum -c -
./yggaro-server-linux-amd64 -version
systemctl stop yggaro-server
cp -p /opt/yggaro/yggaro-server /opt/yggaro/yggaro-server.previous
install -m 755 yggaro-server-linux-amd64 /opt/yggaro/yggaro-server
systemctl start yggaro-server
curl -fsS https://lite.example.com/healthz
journalctl -u yggaro-server --since '10 minutes ago'
```

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

### Migration

Back up first ([backup and restore](backup-restore.md)), then:

```bash
systemctl stop yggaro-server
cp -p /opt/yggaro/yggaro-server /opt/yggaro/yggaro-server.previous
cp -p /etc/systemd/system/yggaro-server.service /root/yggaro-server.service.previous
useradd --system --home-dir /var/lib/yggaro --no-create-home --shell /usr/sbin/nologin yggaro
chown -R yggaro:yggaro /var/lib/yggaro /var/lib/yggaro-keys
chmod 700 /var/lib/yggaro /var/lib/yggaro-keys
install -m 755 yggaro-server-linux-amd64 /opt/yggaro/yggaro-server
```

Replace `/etc/systemd/system/yggaro-server.service` with the unit from [install, step 4](install.md#4-systemd-service), keeping your own `-domain` and `-acme-email`. Install the `yggaro-admin` helper from [step 6](install.md#6-maintenance-commands-run-as-the-service-account). Then:

```bash
systemctl daemon-reload
systemctl start yggaro-server
systemctl status yggaro-server
ps -o user=,pid=,args= -C yggaro-server
yggaro-admin -verify-restore
curl -fsS https://lite.example.com/healthz
```

`ps` must show `yggaro`. If the service ends in `failed`, `journalctl -u yggaro-server -n 20` states the reason in one message and systemd does not keep restarting it (exit code `78`); see [troubleshooting](troubleshooting.md#the-server-will-not-start).

### Rollback

Keep the new unit and file ownership; only put the previous binary back:

```bash
systemctl stop yggaro-server
install -m 755 /opt/yggaro/yggaro-server.previous /opt/yggaro/yggaro-server
systemctl start yggaro-server
```

1.0.1 runs under the `yggaro` account and the same unit, and reads data written by 1.0.2 — 1.0.2 does not change the data format. It ignores `YGGARO_ALLOW_LOCAL_KEY`, which is harmless. Going back to the old root unit is not recommended: files the service creates as root would have to be handed back to `yggaro` by hand before the next upgrade.
