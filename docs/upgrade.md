# Upgrade

Read release notes and `CHANGELOG.md`; back up and verify restore first.

```bash
sha256sum -c SHA256SUMS
./yggaro-server-linux-amd64 -version
systemctl stop yggaro-server
cp -p /opt/yggaro/yggaro-server /opt/yggaro/yggaro-server.previous
install -m 755 yggaro-server-linux-amd64 /opt/yggaro/yggaro-server
systemctl start yggaro-server
curl -fsS https://lite.example.com/healthz
journalctl -u yggaro-server --since '10 minutes ago'
```

Confirm the version, login and a representative read/write path. If smoke checks fail, restore the previous binary. Do not put an older database over a migrated database unless release notes explicitly allow it; use the pre-upgrade backup.
