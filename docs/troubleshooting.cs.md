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

**`✗ Chybný šifrovací klíč pro tuto databázi`** — klíč tuhle databázi neotevře. Server se záměrně zastaví, místo aby přepsal data, která neumí přečíst. Zkontrolujte, že `YGGARO_DB_PASSPHRASE` je to heslo, se kterým instance vznikla, a že `YGGARO_KEYS` ukazuje na správný adresář klíčů. Obnovená záloha potřebuje *obojí* — adresář klíčů i původní heslo.

**`nelze otevřít databázi`** / **`nelze vytvořit datový adresář`** — souborový systém, ne kryptografie: práva, vlastník nebo plný disk. `df -h` a `ls -ld /var/lib/yggaro /var/lib/yggaro-keys`.

**`inicializace selhala`** — databáze se otevřela, ale příprava nedoběhla. Příčinu nese zbytek řádku; skutečný příběh je obvykle v řádku těsně před ním.

## Nejde založit prvního správce

Průvodce chce aktivační token z `YGGARO_BOOTSTRAP_TOKEN`. Když není nastavený, první spuštění se nedokončí — a je to schválně, aby si cizí člověk, který narazí na čerstvou instanci, nezaložil vaši organizaci dřív než vy. Doplňte ho do `/etc/yggaro-server.env` a restartujte.

## Kontrola otisků hlásí „No such file or directory"

`SHA256SUMS` pokrývá všechny soubory vydání a vy jste si nejspíš stáhli jen některý. Ověřte to, co opravdu máte:

```bash
sha256sum -c --ignore-missing SHA256SUMS
```

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
YGGARO_DB_PASSPHRASE='…' /opt/yggaro/yggaro-server \
  -data /var/lib/yggaro -reset-password spravce@vase-firma.example
systemctl start yggaro-server
```

Nové heslo vypíše, pokud nezadáte `-new-password`.

## AI klient se přes MCP nepřipojí

Postupujte od instance ven: je MCP zapnuté (`YGGARO_MCP=1`), používá klient OAuth (`YGGARO_MCP_OAUTH=1`) nebo token vydaný přes `-mcp-token`, a má namapovaný principál vůbec práva na to, oč se klient pokouší? Odmítnutí, které vypadá jako problém se spojením, bývá odpověď o oprávněních. Viz [MCP](mcp.cs.md) a [oprávnění MCP](mcp-permissions.cs.md).

## Záloha, o které nevíte, jestli je dobrá

Nezjišťujte to při havárii:

```bash
YGGARO_KEYS=/srv/restore/yggaro-keys YGGARO_DB_PASSPHRASE='…' \
  /opt/yggaro/yggaro-server -data /srv/restore/yggaro -verify-restore
```

Nulový návratový kód dokládá, že data jsou tím klíčem čitelná. Nedokládá, že je záloha čerstvá a úplná — počty záznamů, které vypíše, porovnejte s tím, co čekáte. Viz [záloha a obnova](backup-restore.md).

## Pořád to nejde

Kam s dotazem, říká [SUPPORT.md](../SUPPORT.md). Přiložte verzi (`yggaro-server -version`), řádky z journalu kolem selhání a co jste měnili naposledy. **Než cokoli zveřejníte, odstraňte tajemství a zákaznická data.** Zranitelnosti patří soukromě podle [SECURITY.md](../SECURITY.md), nikdy do veřejného issue.
