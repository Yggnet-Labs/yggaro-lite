# Install Yggaro Lite Server

[English](install.md) · [Čeština](install.cs.md)

This is the server edition: one organisation, one database, one machine. The supported first-release target is Ubuntu 24.04, `linux-amd64`, 2 vCPU, 4 GB RAM and 40 GB disk. You need root access, a public DNS name and inbound TCP 80/443.

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
sha256sum --ignore-missing -c SHA256SUMS
install -d /opt/yggaro
install -m 755 yggaro-server-linux-amd64 /opt/yggaro/yggaro-server
/opt/yggaro/yggaro-server -version
```

`--ignore-missing` is intentional: `SHA256SUMS` covers the complete release, while you only need to download the binary for your architecture. The command must still print that your downloaded binary is `OK`.

## 3. Data, keys and first-admin protection

```bash
install -d -m 700 /var/lib/yggaro /var/lib/yggaro-keys
umask 077
printf 'YGGARO_DB_PASSPHRASE=%s\nYGGARO_BOOTSTRAP_TOKEN=%s\n' \
  "$(openssl rand -base64 32)" "$(openssl rand -hex 16)" >/etc/yggaro-server.env
```

Store `YGGARO_DB_PASSPHRASE` off the server. Without it an encrypted backup is unreadable. The bootstrap token prevents an internet stranger from claiming the first administrator account.

## 4. systemd service

Create `/etc/systemd/system/yggaro-server.service` and replace the domain and ACME email:

```ini
[Unit]
Description=Yggaro Lite Server
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/opt/yggaro/yggaro-server -domain lite.example.com -acme-email admin@example.com -data /var/lib/yggaro
EnvironmentFile=/etc/yggaro-server.env
Environment=YGGARO_KEYS=/var/lib/yggaro-keys
Restart=always
RestartSec=3
NoNewPrivileges=true
ProtectSystem=full
ReadWritePaths=/var/lib/yggaro /var/lib/yggaro-keys
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable --now yggaro-server
systemctl status yggaro-server
curl -fsS https://lite.example.com/healthz
```

Open the HTTPS URL and use the bootstrap token when the setup wizard asks for it. Continue with [configuration](configuration.md), [backup and restore](backup-restore.md) and [security](security.md).

For a reverse proxy, bind only to loopback and use `-listen 127.0.0.1:7456 -public-host lite.example.com -secure-cookies`; add `-trust-proxy` only when the direct peer is a trusted loopback proxy.
