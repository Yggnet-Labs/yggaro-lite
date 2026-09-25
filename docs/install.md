# Install Yggaro Lite Server

[English](install.md) · [Čeština](install.cs.md)

This is the server edition: one organisation, one database, one machine. The supported first-release target is Ubuntu 24.04, `linux-amd64`, 2 vCPU, 4 GB RAM and 40 GB disk. You need root access to install it, a public DNS name and inbound TCP 80/443. The server itself does **not** run as root: it runs under its own unprivileged account and is only allowed to bind ports 80 and 443.

## 1. DNS and firewall

Point an A record at the server. With built-in TLS the record must be DNS-only: TLS terminates on this server and Let's Encrypt must reach it.

```bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

## 2. Verify and install the release

Download `yggaro-server-linux-amd64` and `SHA256SUMS` from the same GitHub release.

```bash
bash -euo pipefail <<'STEP'
grep '  yggaro-server-linux-amd64$' SHA256SUMS | sha256sum -c -
install -d /opt/yggaro
install -m 755 yggaro-server-linux-amd64 /opt/yggaro/yggaro-server
/opt/yggaro/yggaro-server -version
STEP
```

The block runs as one script that **stops at the first failure**: when the checksum does not match — or the binary is missing from `SHA256SUMS` — nothing is installed and nothing is executed. It must print `yggaro-server-linux-amd64: OK` before the version. It checks exactly the file you are about to install: `SHA256SUMS` lists every file of the release, and a plain `sha256sum --ignore-missing -c` can finish successfully without having checked the binary at all, for example when the downloaded file has a different name.

## 3. Service account, data and secrets

```bash
bash -euo pipefail <<'STEP'
id -u yggaro >/dev/null 2>&1 || useradd --system --home-dir /var/lib/yggaro --no-create-home --shell /usr/sbin/nologin yggaro
install -d -m 700 -o yggaro -g yggaro /var/lib/yggaro /var/lib/yggaro-keys
if [ -e /etc/yggaro-server.env ]; then
  echo "STOP: /etc/yggaro-server.env already exists and holds the database passphrase — not overwriting it." >&2
  exit 1
fi
umask 077
printf 'YGGARO_DB_PASSPHRASE=%s\nYGGARO_BOOTSTRAP_TOKEN=%s\n' \
  "$(openssl rand -base64 32)" "$(openssl rand -hex 16)" >/etc/yggaro-server.env
chmod 600 /etc/yggaro-server.env
STEP
```

Running the block again never replaces an existing `/etc/yggaro-server.env`: a new passphrase would lock the data out.

- **`YGGARO_DB_PASSPHRASE`** protects the database key. Store it off the server as well: without it no backup can be read. The server refuses to start without it.
- **`YGGARO_BOOTSTRAP_TOKEN`** stops an internet stranger from claiming the first administrator account. On an empty database the server refuses to start without it; once the first administrator exists it is no longer used.
- `/etc/yggaro-server.env` stays readable by root only. systemd reads it before it starts the service, so the `yggaro` account never needs to read the file itself.

What the service writes — everything under `/var/lib/yggaro`, owned by `yggaro`, files `0600`, directories `0700`:

| Path | Contents |
|---|---|
| `yggaro.db`, `yggaro.db-wal`, `yggaro.db-shm` | the database (SQLite, content encrypted at rest) |
| `files/` | attachments, encrypted with the same key |
| `acme/` | Let's Encrypt account and certificates |

`/var/lib/yggaro-keys` stays empty on an installation with a passphrase. It is only read — never written — by installations created before 1.0.2 without a passphrase; see [upgrade](upgrade.md). The account's home directory is `/var/lib/yggaro`; the server needs nothing else on disk.

## 4. systemd service

Create `/etc/systemd/system/yggaro-server.service` and replace the domain and ACME email:

```ini
[Unit]
Description=Yggaro Lite Server
After=network-online.target
Wants=network-online.target

[Service]
User=yggaro
Group=yggaro
ExecStart=/opt/yggaro/yggaro-server -domain lite.example.com -acme-email admin@example.com -data /var/lib/yggaro
EnvironmentFile=/etc/yggaro-server.env
Environment=YGGARO_KEYS=/var/lib/yggaro-keys
AmbientCapabilities=CAP_NET_BIND_SERVICE
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=true
UMask=0077
ProtectSystem=strict
ReadWritePaths=/var/lib/yggaro
ProtectHome=true
PrivateTmp=true
PrivateDevices=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectKernelLogs=true
ProtectControlGroups=true
ProtectClock=true
ProtectHostname=true
RestrictNamespaces=true
RestrictRealtime=true
RestrictSUIDSGID=true
LockPersonality=true
MemoryDenyWriteExecute=true
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
SystemCallArchitectures=native
SystemCallFilter=@system-service
SystemCallErrorNumber=EPERM
Restart=always
RestartSec=3
RestartPreventExitStatus=78

[Install]
WantedBy=multi-user.target
```

`CAP_NET_BIND_SERVICE` is the only privilege the process keeps: it lets an ordinary account listen on 80 and 443. `ProtectSystem=strict` makes the whole filesystem read-only for the service except `/var/lib/yggaro`. Exit code `78` means the server refused its configuration (for example a missing passphrase); `RestartPreventExitStatus=78` stops systemd from restarting it every three seconds, so the reason stays readable as a single entry in the journal.

## 5. Start and create the first administrator

```bash
systemctl daemon-reload
systemctl enable --now yggaro-server
timeout 90 bash -c 'until curl -fsS https://lite.example.com/healthz; do sleep 3; done'
systemctl status yggaro-server
ps -o user=,pid=,args= -C yggaro-server
```

On the first start the server obtains its certificate from Let's Encrypt, which can take up to a minute; the `until` line waits for it and gives up after 90 seconds. `ps` must show `yggaro`, not `root`. Open the HTTPS URL; the setup wizard asks for the activation token:

```bash
sed -n 's/^YGGARO_BOOTSTRAP_TOKEN=//p' /etc/yggaro-server.env
```

## 6. Maintenance commands run as the service account

Backups, restore drills, exports, password recovery and MCP tokens are one-off runs of the same binary. **Do not run them as root**: the database would get root-owned files next to it that the service can no longer write. Install a small helper that runs them under the service account with the service's own secrets:

```bash
cat >/usr/local/sbin/yggaro-admin <<'EOF'
#!/bin/sh
# One-off yggaro-server commands under the service account, with the service's secrets.
exec systemd-run --quiet --wait --pipe --collect \
  --uid=yggaro --gid=yggaro -p UMask=0077 \
  -p EnvironmentFile=/etc/yggaro-server.env \
  -p Environment=YGGARO_KEYS=${YGGARO_KEYS:-/var/lib/yggaro-keys} \
  /opt/yggaro/yggaro-server -data /var/lib/yggaro "$@"
EOF
chmod 755 /usr/local/sbin/yggaro-admin
bash -euo pipefail <<'CHECK'
R=$(mktemp -d /var/lib/yggaro-restore-check.XXXXXX)
trap 'rm -rf -- "$R"' EXIT
chown yggaro:yggaro "$R"
yggaro-admin -backup "$R/yggaro.db"
yggaro-admin -data "$R" -verify-restore
CHECK
```

The check creates a consistent snapshot in a new private directory, verifies that copy, then removes the temporary copy even if verification fails. It must report that the database is readable. It does not verify attachments. Do not run `-verify-restore` against the running service’s data directory: a nonempty WAL is rejected so that uncheckpointed changes cannot be missed. Every later option that takes `-data` accepts another directory (`yggaro-admin -data /srv/restore/yggaro …`); the last value wins. Target directories for backups and exports must belong to `yggaro`.

Continue with [configuration](configuration.md), [backup and restore](backup-restore.md) and [security](security.md).

## Behind a reverse proxy

Bind only to loopback and replace the `ExecStart` options with `-listen 127.0.0.1:7456 -public-host lite.example.com -secure-cookies`; add `-trust-proxy` only when the direct peer is a trusted loopback proxy. The unit stays the same — `CAP_NET_BIND_SERVICE` is then simply unused. `-no-encrypt` is refused in this mode and with `-domain`: it exists for local diagnostics only.
