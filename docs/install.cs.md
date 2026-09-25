# Instalace Yggaro Lite Server

[English](install.md) · [Čeština](install.cs.md)

Jde o serverovou edici: jedna organizace, jedna databáze, jeden stroj. Podporovaný cíl prvního vydání je Ubuntu 24.04, `linux-amd64`, 2 vCPU, 4 GB RAM a 40 GB disku. K instalaci potřebujete root, veřejné DNS jméno a otevřené TCP porty 80/443. Samotný server **neběží jako root**: běží pod vlastním neprivilegovaným účtem a smí jen naslouchat na portech 80 a 443.

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
bash -euo pipefail <<'STEP'
grep '  yggaro-server-linux-amd64$' SHA256SUMS | sha256sum -c -
install -d /opt/yggaro
install -m 755 yggaro-server-linux-amd64 /opt/yggaro/yggaro-server
/opt/yggaro/yggaro-server -version
STEP
```

Blok běží jako jeden skript, který se **zastaví při první chybě**: když otisk nesedí — nebo binárka v `SHA256SUMS` chybí — nic se nenainstaluje ani nespustí. Před verzí musí vypsat `yggaro-server-linux-amd64: OK`. Ověří přesně ten soubor, který budete instalovat: `SHA256SUMS` obsahuje všechny soubory vydání a obyčejné `sha256sum --ignore-missing -c` může skončit úspěšně, aniž by binárku vůbec zkontrolovalo — třeba když se stažený soubor jmenuje jinak.

## 3. Účet služby, data a tajemství

```bash
bash -euo pipefail <<'STEP'
id -u yggaro >/dev/null 2>&1 || useradd --system --home-dir /var/lib/yggaro --no-create-home --shell /usr/sbin/nologin yggaro
install -d -m 700 -o yggaro -g yggaro /var/lib/yggaro /var/lib/yggaro-keys
if [ -e /etc/yggaro-server.env ]; then
  echo "STOP: /etc/yggaro-server.env už existuje a nese heslo k databázi — nepřepisuji ho." >&2
  exit 1
fi
umask 077
printf 'YGGARO_DB_PASSPHRASE=%s\nYGGARO_BOOTSTRAP_TOKEN=%s\n' \
  "$(openssl rand -base64 32)" "$(openssl rand -hex 16)" >/etc/yggaro-server.env
chmod 600 /etc/yggaro-server.env
STEP
```

Opakovaný běh bloku existující `/etc/yggaro-server.env` nikdy nepřepíše: nová passphrase by data zamkla.

- **`YGGARO_DB_PASSPHRASE`** chrání klíč k databázi. Uložte ji i mimo server: bez ní nejde přečíst žádná záloha. Bez ní server nenastartuje.
- **`YGGARO_BOOTSTRAP_TOKEN`** brání tomu, aby si prvního správce založil cizí člověk z internetu. S prázdnou databází server bez něj nenastartuje; jakmile první správce existuje, už se nepoužívá.
- `/etc/yggaro-server.env` zůstává čitelný jen pro root. Čte ho systemd ještě před spuštěním služby, účet `yggaro` ho číst nepotřebuje.

Co služba zapisuje — vše v `/var/lib/yggaro`, vlastník `yggaro`, soubory `0600`, adresáře `0700`:

| Cesta | Obsah |
|---|---|
| `yggaro.db`, `yggaro.db-wal`, `yggaro.db-shm` | databáze (SQLite, obsah šifrovaný v klidu) |
| `files/` | přílohy, šifrované stejným klíčem |
| `acme/` | účet a certifikáty Let's Encrypt |

`/var/lib/yggaro-keys` zůstává u instalace s passphrase prázdný. Jen ho čtou — nikdy do něj nezapisují — instalace vzniklé před 1.0.2 bez passphrase; viz [upgrade](upgrade.md). Domovský adresář účtu je `/var/lib/yggaro`; nic jiného na disku server nepotřebuje.

## 4. systemd služba

Vytvořte `/etc/systemd/system/yggaro-server.service` a nahraďte doménu a ACME e-mail:

```ini
[Unit]
Description=Yggaro Lite Server
After=network-online.target
Wants=network-online.target

[Service]
User=yggaro
Group=yggaro
ExecStart=/opt/yggaro/yggaro-server -domain lite.example.cz -acme-email admin@example.cz -data /var/lib/yggaro
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

`CAP_NET_BIND_SERVICE` je jediné oprávnění, které proces má: dovolí obyčejnému účtu naslouchat na 80 a 443. `ProtectSystem=strict` udělá pro službu celý souborový systém jen ke čtení kromě `/var/lib/yggaro`. Návratový kód `78` znamená, že server odmítl svou konfiguraci (třeba chybějící passphrase); `RestartPreventExitStatus=78` zabrání systemd, aby ho restartoval každé tři sekundy, takže důvod zůstane v journalu jako jeden čitelný záznam.

## 5. Spuštění a první správce

```bash
bash -euo pipefail <<'STEP'
systemctl daemon-reload
systemctl enable --now yggaro-server
timeout 90 bash -c 'until curl -fsS https://lite.example.cz/healthz; do sleep 3; done'
systemctl status yggaro-server --no-pager
ps -o user=,pid=,args= -C yggaro-server
STEP
```

Při prvním startu si server vyžádá certifikát od Let's Encrypt, což může trvat až minutu; řádek s `until` na něj počká a po 90 sekundách celý blok zastaví chybou, takže nic za ním neproběhne. `ps` musí ukázat `yggaro`, ne `root`. Otevřete HTTPS adresu; průvodce se zeptá na aktivační token:

```bash
sed -n 's/^YGGARO_BOOTSTRAP_TOKEN=//p' /etc/yggaro-server.env
```

## 6. Údržbové příkazy pod účtem služby

Zálohy, zkoušky obnovy, exporty, obnova hesla i MCP tokeny jsou jednorázová spuštění téže binárky. **Nespouštějte je jako root**: vedle databáze by vznikly soubory patřící rootovi, do kterých pak služba nemůže zapisovat. Nainstalujte si malého pomocníka, který je spustí pod účtem služby s jejími tajemstvími:

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

Kontrola vytvoří konzistentní snapshot v novém soukromém adresáři, ověří tuto kopii a dočasnou kopii odstraní i při selhání. Musí ohlásit, že je databáze čitelná. Přílohy neověřuje. `-verify-restore` nespouštějte nad adresářem běžící služby: neprázdný WAL odmítne, aby nepřehlédl dosud nezapsané změny. Když dalšímu příkazu zadáte jiné `-data` (`yggaro-admin -data /srv/restore/yggaro …`), platí to poslední. Cílové adresáře záloh a exportů musí patřit účtu `yggaro`.

Pokračujte [konfigurací](configuration.md), [zálohami a obnovou](backup-restore.md) a [bezpečností](security.cs.md).

## Za reverse proxy

Naslouchejte jen na loopbacku a v `ExecStart` nahraďte volby za `-listen 127.0.0.1:7456 -public-host lite.example.cz -secure-cookies`; `-trust-proxy` přidejte jen tehdy, když přímým protějškem je důvěryhodná proxy na loopbacku. Jednotka zůstává stejná — `CAP_NET_BIND_SERVICE` se pak jen nevyužije. `-no-encrypt` server v tomto režimu i s `-domain` odmítne: slouží jen k místní diagnostice.
