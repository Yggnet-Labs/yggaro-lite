# Install Yggaro Lite Server 1.0.5

[English](install.md) · [Čeština](install.cs.md)

This is the server edition, not Mesh. Supported target: Ubuntu 24.04/linux-amd64. Installation requires root; the process runs as yggaro with only CAP_NET_BIND_SERVICE.

1. Prepare a new clean host, public DNS without a proxy, and inbound TCP 80/443; preserve SSH. Existing instances require the separate upgrade procedure.
2. Download the binary, LICENSE, NOTICE, PROVENANCE.json, SBOM.cdx.json, THIRD-PARTY-NOTICES.md, VERSION.txt and SHA256SUMS from the same GitHub Release. Check all seven files, without ignore-missing:

```bash
bash -euo pipefail <<'CHECK'
printf '50d979f634f49536aeca10d16a9e7193a2aa59889eecad1bda8744cdc06e4e6c  SHA256SUMS\n' | sha256sum -c -
sha256sum -c SHA256SUMS
CHECK
```

This release is unsigned. SHA256SUMS checks integrity, not origin; this guide and its manifest pin share a distribution source. Compare the binary SHA256 with the release notes: fd943def65417fa4480df345406652690898a27bcf63387b300fec30e39d86a8.

3. Use the installation helpers from the same published documentation commit, in docs/installation-105. Download the published documentation repository archive from the same accepted commit and unpack it beside the release files, so the current directory contains both SHA256SUMS and docs/installation-105/. Run the commands from that directory; --bundle "$PWD" refers to the downloaded release files. Check helpers before running any as root:

```bash
bash -euo pipefail <<'HELPERS'
printf '57442de6ccf3d18add6a645f6da9e9b64eb0637ad245b00726b6aacf95953062  docs/installation-105/install.py\n' | sha256sum -c -
printf 'f0185500711f309b16ac8edc42c4579e79dc21200b487bdcd050417024dfbb18  docs/installation-105/yggaro-server.service.in\n' | sha256sum -c -
printf 'cbf58c165b61f502f6a3a249b356195c1bc6aa6291f5d0b0d802e5f52f438614  docs/installation-105/yggaro-admin\n' | sha256sum -c -
printf 'e48920d6f1135f628e7f4150a951c95abcba8f208fa1f5691ceb61ac6156a7ad  docs/installation-105/uninstall.py\n' | sha256sum -c -
HELPERS
```

Replace the domain and e-mail with yours:

```bash
sudo python3 docs/installation-105/install.py --bundle "$PWD" --domain lite.example.com --email admin@example.com
```

The installer refuses missing/changed assets, existing data/env/unit/program paths and a root yggaro account. It never prints secrets and does not start the service. Securely store the passphrase from /etc/yggaro-server.env off-host; keep it and the bootstrap token out of chat, logs and screen recordings. Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now yggaro-server
sudo systemctl status yggaro-server
curl -fsS https://lite.example.com/healthz
```

4. Check version 1.0.5, commit 2ce7da1, the yggaro process account, modes 0600/0700 and a valid certificate. Enter the bootstrap token privately in the HTTPS wizard. Run backup/restore/export only through yggaro-admin; destination directories must belong to yggaro. Verify-restore reads a snapshot, not live WAL.
5. Check the installation without printing the environment file or secrets:

```bash
curl -fsS https://lite.example.com/healthz
ps -o user= -p "$(systemctl show -p MainPID --value yggaro-server)"
sudo stat -c '%a %U:%G %n' /etc/yggaro-server.env /var/lib/yggaro /var/lib/yggaro-keys
```

The health response must report status ok, version 1.0.5 and commit 2ce7da1; the process user must be yggaro. The environment file must be root-owned 0600 and data/key directories 0700. Real Let's Encrypt issuance and hostname-verified HTTPS passed on a clean Ubuntu host on 12 October 2026. Public GitHub download remains to be checked after publication. Internal supplier acceptance is not a customer installation step.
6. Uninstall while preserving data: sudo python3 docs/installation-105/uninstall.py. It removes the service, binary and helper; data, keys, env/passphrase, backups and account remain. Permanent erasure needs a separate decision after checking backups and erasure requirements. Firewall/DNS/certificates are not changed automatically.

The installation includes the exact systemd unit User/Group=yggaro, Ambient/Bounding=CAP_NET_BIND_SERVICE, UMask=0077, ProtectSystem=strict and RestartPreventExitStatus=78, so configuration failures do not restart-loop. TLS behind a proxy requires its separate accepted procedure; built-in TLS was verified during clean-host acceptance.
