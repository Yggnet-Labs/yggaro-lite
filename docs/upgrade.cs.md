# Aktualizace na 1.0.5

[English](upgrade.md) · [Čeština](upgrade.cs.md)

Pro samostatně provozovanou serverovou edici běžící jako **root**, tak jak ji nastavoval návod k instalaci verzí 1.0.0–1.0.3 (binárka v `/opt/yggaro/yggaro-server`, data v `/var/lib/yggaro`, klíče v `/var/lib/yggaro-keys`, služba `yggaro-server`). Platí pro 1.0.3, poslední zveřejněnou verzi, i pro 1.0.4. Verze 1.0.4 byla opravné sestavení jen pro hostované instance a nebyla zveřejněna; pokud ji provozujete, postup je stejný.

## Co bylo a nebylo vyzkoušeno

* **Vyzkoušeno:** čistá instalace 1.0.5 na Ubuntu 24.04 (služba bez root oprávnění, automatický HTTPS certifikát) a aktualizace **testovací instalace 1.0.1** (server 1.0.1 sestavený pro test znovu ze zdroje, ne původně zveřejněná binárka) na 1.0.5 instalační sadou tohoto testu.
* **Nevyzkoušeno:** aktualizace produkční instance z 1.0.3 nebo 1.0.4 podle kroků níže, obnova zálohy příkazy z části Návrat zpět na skutečné instanci a spuštění starší binárky nad daty, která už zapsala 1.0.5 (proto to návrat zpět nikdy nedělá). Blok aktualizace i postup návratu byly spuštěny jen proti zástupným příkazům v pomocném adresáři (10 případů aktualizace: úspěch, špatný součet, chybějící řádek součtu, špatná verze, selhání zastavení, selhání startu a čtyři chybné odpovědi kontroly zdraví; u návratu se kontroluje obnovení souborů, uchování kopií `*.failed-1.0.5`, pořadí příkazů a selhání při neúplné záloze), aby se ověřilo, že skončí u prvního selhání a obnoví očekávané soubory. Kroky jsou standardní postup dřívějších verzí použitý pro 1.0.5. Oproti 1.0.3 zdroj nepřidává žádné databázové tabulky ani sloupce, přesto berte aktualizaci jako jednosměrnou a zálohu si ponechte.

## Než začnete

1. Přečtěte si [poznámky k vydání](https://github.com/Yggnet-Labs/yggaro-lite/releases) verze 1.0.5 včetně známých omezení.
2. Naplánujte krátký výpadek a uživatele upozorněte.
3. Pořiďte a zkontrolujte zálohu — není volitelná. Postupujte podle [zálohy a obnovy](backup-restore.md): snímek databáze (`-backup`), adresář `files`, adresář `yggaro-keys` a **heslo (passphrase) uložené mimo server**. Obnovte ji do izolovaného adresáře a spusťte `-verify-restore`. Zálohu zkopírujte mimo stroj.

## Aktualizace

Do prázdného adresáře na serveru stáhněte z vydání 1.0.5 na GitHubu `yggaro-server-linux-amd64` a `SHA256SUMS` a spusťte **celý tento blok jako root najednou**. Skončí u prvního problému a běžící službu se nedotkne, dokud není stažený soubor ověřen.

```bash
bash -euo pipefail <<'UPGRADE'
YGG=/opt/yggaro            # kde má vaše instalace binárku
SVC=yggaro-server          # název vaší systemd služby
URL=https://lite.example.com/healthz   # vaše instance

# 1. Ověření PŘED zásahem do služby
grep ' yggaro-server-linux-amd64$' SHA256SUMS | sha256sum -c -
chmod +x yggaro-server-linux-amd64
./yggaro-server-linux-amd64 -version | grep -q '^Yggaro Lite Server 1.0.5 (2ce7da1,' \
  || { echo "KONEC: neočekávaná verze, nic nebylo změněno"; exit 1; }

# 2. Výměna (jakýkoli neúspěšný krok skončí; předchozí binárka zůstává jako .previous)
systemctl stop "$SVC" || { echo "KONEC: služba se nezastavila, nic nebylo vyměněno"; exit 1; }
cp -p "$YGG/yggaro-server" "$YGG/yggaro-server.previous"
install -m 755 yggaro-server-linux-amd64 "$YGG/yggaro-server.new"
mv "$YGG/yggaro-server.new" "$YGG/yggaro-server"
systemctl start "$SVC" \
  || { echo "START SELHAL: nová binárka je nainstalovaná a start byl zkoušen - postupujte podle 'Návrat zpět' níže"; exit 1; }

# 3. Kontrola
sleep 5
curl -fsS "$URL" | python3 -c 'import sys,json;d=json.load(sys.stdin);sys.exit(0 if (d.get("status"),d.get("version"),d.get("commit"))==("ok","1.0.5","2ce7da1") else 1)' \
  || { echo "KONTROLA SELHALA: nová binárka už byla spuštěna - postupujte podle 'Návrat zpět' níže"; exit 1; }
echo "AKTUALIZACE OK"
UPGRADE
```

Blok porovná binárku s jejím řádkem v `SHA256SUMS`; chybějící řádek nebo neshoda skončí chybou. `SHA256SUMS` dokládá jen integritu: stejně jako 1.0.0–1.0.3 není ani 1.0.5 kryptograficky podepsána, proto porovnejte SHA-256 binárky (`sha256sum yggaro-server-linux-amd64`) i s hodnotou v poznámkách k vydání (`fd943def65417fa4480df345406652690898a27bcf63387b300fec30e39d86a8`) a obojí berte ze stránky vydání.

Poté zkontrolujte `journalctl -u yggaro-server --since '10 minutes ago'`, přihlaste se jako administrátor, ověřte, že data jsou na místě, že umíte přečíst a uložit záznam a že funguje dvoufázové přihlášení.

Stávající soubor služby ponechte. Verze 1.0.5 po něm žádnou změnu nevyžaduje; zpřísnění služby na běh bez root oprávnění z nového návodu k instalaci je samostatná migrace a součástí této aktualizace není.

## Co se po aktualizaci změní

* Administrátoři mají bezpečnostní panel se seznamem sessions, MCP mandátů a rodin OAuth tokenů a s výslovným odvoláním. Zapnutí povinného dvoufázového ověření samo existující přístupy neukončí — odvolejte, co chcete ukončit.
* Zapnutí a změna dvoufázového ověření se zapisují jako samostatné události do bezpečnostního logu; uživatelé vidí své události.
* Bezpečnostní nastavení uložené poprvé na instanci se projeví okamžitě.
* Sada nástrojů MCP je oproti 1.0.3 beze změny. Známé omezení: capability `mcp.dependency.write` je rezervovaná a ve verzi 1.0.5 nemá žádný nástroj (viz poznámky k vydání).

## Návrat zpět

Postup závisí na jediné věci: **byla nová binárka někdy spuštěna?**

* **Blok skončil před `systemctl start`** (selhal součet, verze nebo zastavení, nebo samotná výměna): nová binárka nikdy neběžela, takže nic nezapsala do vašich aplikačních dat (změnily se jen kroky zastavení, kopie a výměny). Je-li služba zastavená, spusťte ji znovu; pokud `yggaro-server.previous` existuje a `yggaro-server` je neúplný, nejdřív zkopírujte `.previous` zpět.
* **Nová binárka byla spuštěna, i krátce** (včetně „KONTROLA SELHALA“): mohla už zapsat do vašich dat, s přihlášenými uživateli i bez nich. **Nespouštějte** starou binárku nad aktuálními daty. Obnovte zálohu před aktualizací spolu s předchozí binárkou:

```bash
set -euo pipefail
systemctl stop yggaro-server
mv /var/lib/yggaro /var/lib/yggaro.failed-1.0.5          # ponechat, nemazat
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

Použijte cesty, kam jste zálohu uložili. `/healthz` pak musí znovu hlásit předchozí verzi. Práce provedená po aktualizaci je ztracena; adresáře `*.failed-1.0.5` ji uchovávají k prohlídce. Starší databázi nepřekrývejte přes migrovanou, pokud to poznámky k vydání výslovně nedovolují.

Pokud něco neodpovídá tomuto návodu, zastavte se a zeptejte se nás (bezpečnostní věci: kontakt v `SECURITY.md`) — neimprovizujte na produkčních datech.
