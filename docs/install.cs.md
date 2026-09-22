# Instalace Yggaro Lite Server

[English](install.md) · [Čeština](install.cs.md)

Jde o serverovou edici: jedna organizace, jedna databáze, jeden stroj. Podporovaný cíl prvního vydání je Ubuntu 24.04, `linux-amd64`, 2 vCPU, 4 GB RAM a 40 GB disku. Potřebujete root, veřejné DNS jméno a otevřené TCP porty 80/443.

## 1. DNS a firewall

Nasměrujte A záznam na server. Při vestavěném TLS musí být záznam bez proxy: TLS končí na tomto serveru a Let's Encrypt se na něj musí dostat.

```bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

## 2. Ověření a instalace vydání

Stáhněte `yggaro-server-linux-amd64` a `SHA256SUMS` ze stejného GitHub Release.

```bash
sha256sum --ignore-missing -c SHA256SUMS
install -d /opt/yggaro
install -m 755 yggaro-server-linux-amd64 /opt/yggaro/yggaro-server
/opt/yggaro/yggaro-server -version
```

`--ignore-missing` je záměrně: `SHA256SUMS` pokrývá celé vydání, zatímco vy potřebujete stáhnout jen binárku pro svou architekturu. Příkaz přesto musí u stažené binárky vypsat `OK`.

## 3. Data, klíče a ochrana prvního správce

```bash
install -d -m 700 /var/lib/yggaro /var/lib/yggaro-keys
umask 077
printf 'YGGARO_DB_PASSPHRASE=%s\nYGGARO_BOOTSTRAP_TOKEN=%s\n' \
  "$(openssl rand -base64 32)" "$(openssl rand -hex 16)" >/etc/yggaro-server.env
```

`YGGARO_DB_PASSPHRASE` uložte mimo server. Bez něj je šifrovaná záloha nečitelná. Bootstrap token brání cizímu člověku zabrat účet prvního správce.

## 4. Služba systemd

Vytvořte `/etc/systemd/system/yggaro-server.service`; nahraďte doménu a e-mail pro ACME:

```ini
[Unit]
Description=Yggaro Lite Server
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/opt/yggaro/yggaro-server -domain lite.example.cz -acme-email admin@example.cz -data /var/lib/yggaro
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
curl -fsS https://lite.example.cz/healthz
```

Otevřete HTTPS adresu a v průvodci zadejte bootstrap token. Pokračujte [konfigurací](configuration.md), [zálohou a obnovou](backup-restore.md) a [bezpečnostním modelem](security.cs.md).

Za reverse proxy poslouchejte jen na loopbacku: `-listen 127.0.0.1:7456 -public-host lite.example.cz -secure-cookies`. `-trust-proxy` zapínejte jen tehdy, když je přímým peerem důvěryhodná proxy na loopbacku.
