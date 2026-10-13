# Instalace Yggaro Lite Server 1.0.5

[English](install.md) · [Čeština](install.cs.md)

Serverová edice, nikoli Mesh. Podporovaný cíl Ubuntu 24.04/linux-amd64. Root je potřeba k instalaci; proces běží jako yggaro s jedinou capability CAP_NET_BIND_SERVICE.

1. Připravte nový čistý host, veřejné DNS bez proxy a TCP 80/443; zachovejte SSH. Stávající instance patří do samostatného upgrade postupu.
2. Stáhněte ze stejného GitHub Release binárku, LICENSE, NOTICE, PROVENANCE.json, SBOM.cdx.json, THIRD-PARTY-NOTICES.md, VERSION.txt a SHA256SUMS. Ověřte všech sedm souborů, nikoli ignore-missing:

```bash
bash -euo pipefail <<'CHECK'
printf '50d979f634f49536aeca10d16a9e7193a2aa59889eecad1bda8744cdc06e4e6c  SHA256SUMS\n' | sha256sum -c -
sha256sum -c SHA256SUMS
CHECK
```

Vydání není podepsané. SHA256SUMS ověřuje integritu, nikoli původ; návod a pin manifestu sdílejí distribuční zdroj. Porovnejte SHA256 binárky s release notes: fd943def65417fa4480df345406652690898a27bcf63387b300fec30e39d86a8.

3. Použijte pomocníky ze stejného publikovaného dokumentačního commitu, ve složce docs/installation-105. Stáhněte archiv publikovaného dokumentačního repozitáře ze stejného přijatého commitu a rozbalte jej vedle release souborů. Aktuální adresář pak obsahuje SHA256SUMS i docs/installation-105/. Příkazy spusťte z tohoto adresáře; --bundle "$PWD" odkazuje na stažené release soubory. Před spuštěním pomocníka jako root ověřte jejich otisky:

```bash
bash -euo pipefail <<'HELPERS'
printf '57442de6ccf3d18add6a645f6da9e9b64eb0637ad245b00726b6aacf95953062  docs/installation-105/install.py\n' | sha256sum -c -
printf 'f0185500711f309b16ac8edc42c4579e79dc21200b487bdcd050417024dfbb18  docs/installation-105/yggaro-server.service.in\n' | sha256sum -c -
printf 'cbf58c165b61f502f6a3a249b356195c1bc6aa6291f5d0b0d802e5f52f438614  docs/installation-105/yggaro-admin\n' | sha256sum -c -
printf 'e48920d6f1135f628e7f4150a951c95abcba8f208fa1f5691ceb61ac6156a7ad  docs/installation-105/uninstall.py\n' | sha256sum -c -
HELPERS
```

Nahraďte doménu a e-mail svými hodnotami:

```bash
sudo python3 docs/installation-105/install.py --bundle "$PWD" --domain lite.example.com --email admin@example.com
```

Instalátor odmítne chybějící či jiný soubor, existující data/env/unit/program a root účet yggaro. Nevypisuje tajemství a službu sám nespouští. Passphrase z /etc/yggaro-server.env bezpečně uchovejte mimo host; její hodnotu ani bootstrap token nedávejte do chatu, logu či nahrávání obrazovky. Potom:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now yggaro-server
sudo systemctl status yggaro-server
curl -fsS https://lite.example.com/healthz
```

4. Ověřte verzi 1.0.5, commit 2ce7da1, proces jako yggaro, práva 0600/0700 a platný certifikát. V HTTPS průvodci bezpečně zadejte bootstrap token. Zálohu/obnovu/export spouštějte pouze přes yggaro-admin; adresář cíle musí patřit yggaro. Verify-restore pracuje nad snapshotem, nikoli živým WAL.
5. Ověřte instalaci bez výpisu souboru prostředí či tajemství:

```bash
curl -fsS https://lite.example.com/healthz
ps -o user= -p "$(systemctl show -p MainPID --value yggaro-server)"
sudo stat -c '%a %U:%G %n' /etc/yggaro-server.env /var/lib/yggaro /var/lib/yggaro-keys
```

Health odpověď musí hlásit status ok, verzi 1.0.5 a commit 2ce7da1; uživatel procesu musí být yggaro. Soubor prostředí musí patřit rootovi a mít 0600, adresáře dat a klíčů 0700. Skutečné vydání certifikátu Let's Encrypt a HTTPS s ověřením hostname prošlo na čistém Ubuntu hostu 12. října 2026. Veřejné stažení z GitHubu zbývá ověřit po publikaci. Interní dodavatelská přejímka není instalační krok zákazníka.
6. Odinstalace zachovávající data: sudo python3 docs/installation-105/uninstall.py. Odstraní službu, binárku a pomocníka; data, klíče, env s passphrase, zálohy a účet zůstanou. Jejich trvalý výmaz je jiné rozhodnutí po ověření záloh a výmazových povinností. Síťová pravidla/DNS/certifikáty se nemění automaticky.

Součástí instalace je přesná systemd jednotka User/Group=yggaro, Ambient/Bounding=CAP_NET_BIND_SERVICE, UMask=0077, ProtectSystem=strict a RestartPreventExitStatus=78. Konfigurační chyba tedy nekončí restartovací smyčkou. TLS za proxy používá samostatně přijatý postup; vestavěné TLS bylo ověřeno při přejímce na čistém stroji.
