# Upgrade to 1.0.5

[English](upgrade.md) · [Čeština](upgrade.cs.md)

For the self-hosted server edition running as **root**, as set up by the installation guide of versions 1.0.0–1.0.3 (binary in `/opt/yggaro/yggaro-server`, data in `/var/lib/yggaro`, keys in `/var/lib/yggaro-keys`, service `yggaro-server`). It applies to 1.0.3, the last public release, and to 1.0.4. 1.0.4 was a maintenance build for hosted instances only and was never published; if you run it, the steps are the same.

## What was and was not tested

* **Tested:** a clean installation of 1.0.5 on Ubuntu 24.04 (non-root service, automatic HTTPS certificate), and an upgrade of a **1.0.1 test installation** (a 1.0.1 server rebuilt from its source for the test, not the originally published binary) to 1.0.5 with the installation kit of that test.
* **Not tested:** upgrading a production instance from 1.0.3 or 1.0.4 with the steps below, restoring a backup with the rollback commands on a real instance, and running an older binary on data that 1.0.5 has already written (that is why the rollback never does it). The upgrade block and the rollback sequence were run only against stand-in commands in a scratch directory (10 upgrade cases: success, wrong checksum, missing checksum line, wrong version, failed stop, failed start, and four wrong answers from the health check; the rollback sequence is checked for restored files, kept `*.failed-1.0.5` copies, command order and failure when the backup is incomplete) to check that they stop at the first failure and restore the expected files. The steps are the standard procedure of earlier releases, applied to 1.0.5. Compared with 1.0.3, the source adds no database tables or columns, but treat the upgrade as one-way and keep your backup.

## Before you start

1. Read the [release notes](https://github.com/Yggnet-Labs/yggaro-lite/releases) for 1.0.5, including the known limitations.
2. Schedule a short outage and tell your users.
3. Take and check a backup — this is not optional. Follow [backup and restore](backup-restore.md): database snapshot (`-backup`), the `files` directory, the `yggaro-keys` directory and your **passphrase stored off the server**. Restore it into an isolated directory and run `-verify-restore` on it. Copy the backup off the machine.

## Upgrade

Download `yggaro-server-linux-amd64` and `SHA256SUMS` from the 1.0.5 GitHub release into an empty directory on the server, then run this **whole block as root in one go**. It stops at the first problem and never touches the running service before the download has been verified.

```bash
bash -euo pipefail <<'UPGRADE'
YGG=/opt/yggaro            # where your install keeps the binary
SVC=yggaro-server          # your systemd service name
URL=https://lite.example.com/healthz   # your instance

# 1. Verify BEFORE touching the service
grep ' yggaro-server-linux-amd64$' SHA256SUMS | sha256sum -c -
chmod +x yggaro-server-linux-amd64
./yggaro-server-linux-amd64 -version | grep -q '^Yggaro Lite Server 1.0.5 (2ce7da1,' \
  || { echo "ABORT: unexpected version, nothing was changed"; exit 1; }

# 2. Swap (any failing step aborts; the previous binary stays as .previous)
systemctl stop "$SVC" || { echo "ABORT: service did not stop, nothing was replaced"; exit 1; }
cp -p "$YGG/yggaro-server" "$YGG/yggaro-server.previous"
install -m 755 yggaro-server-linux-amd64 "$YGG/yggaro-server.new"
mv "$YGG/yggaro-server.new" "$YGG/yggaro-server"
systemctl start "$SVC" \
  || { echo "START FAILED: the new binary is installed and a start was attempted - follow 'Rolling back' below"; exit 1; }

# 3. Check
sleep 5
curl -fsS "$URL" | python3 -c 'import sys,json;d=json.load(sys.stdin);sys.exit(0 if (d.get("status"),d.get("version"),d.get("commit"))==("ok","1.0.5","2ce7da1") else 1)' \
  || { echo "CHECK FAILED: the new binary has now been started - follow 'Rolling back' below"; exit 1; }
echo "UPGRADE OK"
UPGRADE
```

The block compares the binary with the line for it in `SHA256SUMS`; a missing line or a mismatch aborts. `SHA256SUMS` proves integrity only: like 1.0.0–1.0.3, 1.0.5 is not cryptographically signed, so also compare the SHA-256 of the binary (`sha256sum yggaro-server-linux-amd64`) with the value in the release notes (`fd943def65417fa4480df345406652690898a27bcf63387b300fec30e39d86a8`) and take both from the release page itself.

Afterwards check `journalctl -u yggaro-server --since '10 minutes ago'`, sign in as an administrator, confirm your data is present, that you can read and save a record, and that two-factor sign-in still works.

Keep your existing service file. Version 1.0.5 does not require changes to it; the non-root service hardening described in the new installation guide is a separate migration, not part of this upgrade.

## What changes after the upgrade

* Administrators get a security panel listing sessions, MCP mandates and OAuth token families, with explicit revocation. Switching on mandatory two-factor authentication does not by itself end existing access — revoke what you want to end.
* Enabling and changing two-factor authentication are recorded as separate events in the security log; users can see their own events.
* A security setting saved for the first time on an instance takes effect immediately.
* The MCP tool set is unchanged from 1.0.3. Known limitation: the `mcp.dependency.write` capability is reserved and has no tool in 1.0.5 (see release notes).

## Rolling back

Which procedure applies depends on one fact: **has the new binary ever been started?**

* **The block aborted before `systemctl start`** (checksum, version or stop failed, or the swap itself failed): the new binary never ran, so it wrote nothing to your application data (the stop, copy and swap steps themselves are the only changes). If the service is stopped, start it again; if `yggaro-server.previous` exists and `yggaro-server` is incomplete, copy `.previous` back over it first.
* **The new binary was started, even briefly** (including "CHECK FAILED"): it may already have written to your data, with or without users signed in. Do **not** run the old binary on the current data. Restore the pre-upgrade backup together with the previous binary:

```bash
set -euo pipefail
systemctl stop yggaro-server
mv /var/lib/yggaro /var/lib/yggaro.failed-1.0.5          # keep, do not delete
mv /var/lib/yggaro-keys /var/lib/yggaro-keys.failed-1.0.5
install -d -m 700 /var/lib/yggaro /var/lib/yggaro-keys
install -m 600 /srv/backup/yggaro.db /var/lib/yggaro/yggaro.db
tar -C /var/lib/yggaro -xzf /srv/backup/files.tgz
tar -C /var/lib -xzf /srv/backup/yggaro-keys.tgz
install -m 755 /opt/yggaro/yggaro-server.previous /opt/yggaro/yggaro-server
set -a; . /etc/yggaro-server.env; set +a
YGGARO_KEYS=/var/lib/yggaro-keys /opt/yggaro/yggaro-server -data /var/lib/yggaro -verify-restore
systemctl start yggaro-server
curl -fsS https://lite.example.com/healthz
```

Use the paths where you stored the backup. After this, `/healthz` must report the previous version again. Work done after the upgrade is lost; the `*.failed-1.0.5` directories keep it for inspection. Do not put an older database over a migrated one unless the release notes say it is allowed.

If something does not match this guide, stop and ask us (security matters: the contact in `SECURITY.md`) — do not improvise on production data.
