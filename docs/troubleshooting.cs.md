# Když něco nejde

[English](troubleshooting.md) · [Čeština](troubleshooting.cs.md)

Začněte tady:

```bash
systemctl status yggaro-server
journalctl -u yggaro-server --since '15 minutes ago'
curl -fsS https://vase-domena.example/healthz
```

## Certifikát se nevydá

Skoro vždycky jedna ze tří věcí, v tomhle pořadí pravděpodobnosti:

1. **Doména je za proxy.** TLS končí *na vašem serveru*. Když je DNS záznam proxovaný — třeba oranžový mráček u Cloudflare —, výzva se k instanci nedostane. Přepněte záznam na **DNS only**.
2. **Je zavřený port 80.** ACME ho potřebuje, i když aplikace jede na 443. `ufw allow 80/tcp`.
3. **A záznam neukazuje na tenhle stroj.** Ověřte zvenčí, ne ze serveru: `dig +short vase-domena.example`.

Let's Encrypt opakovaná selhání pro totéž jméno omezuje. Odstraňte příčinu, než to zkusíte znovu — jinak budete čekat na limit, ne na opravu.

Za vlastní reverse proxy `-domain` nepoužívejte vůbec, viz níže.

## Server nenastartuje

**`✗ Server odmítl start: …`, návratový kód 78** — server odmítl svou konfiguraci dřív, než cokoli obsloužil (od 1.0.2). Slovo za dvojtečkou jmenuje pravidlo; systemd nechá službu ve stavu `failed` a nerestartuje ji:

| Kód ve zprávě | Význam | Co dělat |
|---|---|---|
| `no-db-passphrase` | chybí `YGGARO_DB_PASSPHRASE` | nastavte ji v `/etc/yggaro-server.env`. **Když zpráva jmenuje soubor klíče, nedělejte to** — instance vznikla bez passphrase; viz [upgrade](upgrade.md#from-100-or-101-to-102) |
| `no-bootstrap-token` | prázdná databáze a chybí `YGGARO_BOOTSTRAP_TOKEN` | nastavte token, restartujte, zadejte ho v průvodci |
| `passphrase-and-local-key` | nastavená je passphrase i `YGGARO_ALLOW_LOCAL_KEY` | nechte jen to, s čím instance vznikla |
| `no-existing-local-key` | `YGGARO_ALLOW_LOCAL_KEY` je nastavené, ale na stroji žádný klíč není | souhlas platí jen pro existující klíč, nový nevznikne nikdy. Nastavte passphrase, nebo zkontrolujte `YGGARO_KEYS` |
| `invalid-local-key` | lokální klíč existuje, ale je poškozený nebo nečitelný | nic se nepřepsalo. Obnovte adresář klíčů ze zálohy |
| `no-encrypt-in-public-mode` | `-no-encrypt` spolu s veřejným provozem | odeberte `-no-encrypt`; je jen pro místní diagnostiku |

`database-state-unknown` (návratový kód 1, restartuje se) znamená, že server nepoznal, jestli už instance správce má. Hádat nebude; zbytek řádku jmenuje chybu databáze.

**`✗ Chybný šifrovací klíč pro tuto databázi`** — klíč tuhle databázi neotevře. Server se záměrně zastaví, místo aby přepsal data, která neumí přečíst. Zkontrolujte, že `YGGARO_DB_PASSPHRASE` je to heslo, se kterým instance vznikla, a že `YGGARO_KEYS` ukazuje na správný adresář klíčů. Obnovená záloha potřebuje *obojí* — adresář klíčů i původní heslo.

**`nelze otevřít databázi`** / **`nelze vytvořit datový adresář`** — souborový systém, ne kryptografie: práva, vlastník nebo plný disk. `df -h` a `ls -ln /var/lib/yggaro`. Všechno tam musí patřit účtu `yggaro`; údržbový příkaz spuštěný jako root místo přes `yggaro-admin` po sobě nechá soubory patřící rootovi. Oprava: `chown -R yggaro:yggaro /var/lib/yggaro`.

**`inicializace selhala`** — databáze se otevřela, ale příprava nedoběhla. Příčinu nese zbytek řádku; skutečný příběh je obvykle v řádku těsně před ním.

## Nejde založit prvního správce

Průvodce chce aktivační token z `YGGARO_BOOTSTRAP_TOKEN` (`sed -n 's/^YGGARO_BOOTSTRAP_TOKEN=//p' /etc/yggaro-server.env`). Od 1.0.2 prázdná databáze bez tokenu ani nenastartuje — a je to schválně, aby si cizí člověk, který narazí na čerstvou instanci, nezaložil vaši organizaci dřív než vy. Doplňte ho do `/etc/yggaro-server.env` a restartujte.

## Kontrola otisků hlásí „No such file or directory"

`SHA256SUMS` pokrývá všechny soubory vydání a vy jste si nejspíš stáhli jen binárku. Ověřte přesně ten soubor:

```bash
grep '  yggaro-server-linux-amd64$' SHA256SUMS | sha256sum -c -
```

Musí vypsat `yggaro-server-linux-amd64: OK`. Samotnému `--ignore-missing` nevěřte: projde i tehdy, když se binárka vůbec nezkontrolovala.

## Za reverse proxy

Tři příznaky, tři přepínače — viz [konfigurace](configuration.md):

| Příznak | Příčina | Řešení |
|---|---|---|
| V auditu a rate-limitu mají všichni `127.0.0.1` | IP klienta je v `X-Forwarded-For` a ve výchozím stavu se jí nevěří | `-trust-proxy` (platí, jen když přímé spojení přichází z loopbacku) |
| Sezení padají nebo si prohlížeč nedrží cookie | cookie není `Secure`, protože samotná instance neběží na TLS | `-secure-cookies` |
| Požadavky se odmítají kvůli jménu hosta | veřejné jméno není v povolených | `-public-host vase-domena.example` |

Rate limit a audit jsou tak dobré, jak dobrou IP vidí. Proxy bez `-trust-proxy` udělá ze všech návštěvníků jednoho velmi pilného místního uživatele.

## Správce se nemůže dostat dovnitř

Nouzová obnova potřebuje přístup ke stroji a ke klíči — a právě o to jde:

```bash
systemctl stop yggaro-server
yggaro-admin -reset-password spravce@vase-firma.example
systemctl start yggaro-server
```

`yggaro-admin` je pomocník z [instalace, krok 6](install.cs.md#6-údržbové-příkazy-pod-účtem-služby).

Nové heslo vypíše, pokud nezadáte `-new-password`.

## AI klient se přes MCP nepřipojí

Postupujte od instance ven: je MCP zapnuté (`YGGARO_MCP=1`), používá klient OAuth (`YGGARO_MCP_OAUTH=1`) nebo token vydaný přes `-mcp-token`, a má namapovaný principál vůbec práva na to, oč se klient pokouší? Odmítnutí, které vypadá jako problém se spojením, bývá odpověď o oprávněních. Viz [MCP](mcp.cs.md) a [oprávnění MCP](mcp-permissions.cs.md).

## Záloha, o které nevíte, jestli je dobrá

Nezjišťujte to při havárii:

```bash
YGGARO_KEYS=/srv/restore/yggaro-keys yggaro-admin -data /srv/restore/yggaro -verify-restore
```

Nulový návratový kód dokládá, že data jsou tím klíčem čitelná. Nedokládá, že je záloha čerstvá a úplná — počty záznamů, které vypíše, porovnejte s tím, co čekáte. Viz [záloha a obnova](backup-restore.md).

## Pořád to nejde

Kam s dotazem, říká [SUPPORT.md](../SUPPORT.md). Přiložte verzi (`yggaro-server -version`), řádky z journalu kolem selhání a co jste měnili naposledy. **Než cokoli zveřejníte, odstraňte tajemství a zákaznická data.** Zranitelnosti patří soukromě podle [SECURITY.md](../SECURITY.md), nikdy do veřejného issue.
