# Data a soukromí

[English](data-and-privacy.md) · [Čeština](data-and-privacy.cs.md)

Tahle stránka odpovídá na to, co se u zákazníka ptá IT a právní oddělení jako první: **kde naše data leží, kdo se k nim dostane a jak je dostaneme zpátky ven.** Popisuje self-hostovanou serverovou edici. U hostované služby viz [yggarolite.cz](https://yggarolite.cz).

## Kde data leží

Všechno, co aplikace ukládá, je na vašem stroji:

| Co | Kde |
|---|---|
| Databáze (SQLite) | `<data>/yggaro.db`, výchozí `/var/lib/yggaro` |
| Přílohy | `<data>/files/` |
| Klíčový materiál | `YGGARO_KEYS`, výchozí `/var/lib/yggaro-keys` — mimo datový strom |
| Certifikáty TLS | `<data>/acme/` při vestavěném ACME |

Žádná externí databáze, žádná fronta, žádná cache, kterou byste museli provozovat. Binárka je čistě v Go včetně SQLite driveru, takže vedle ní není co instalovat.

## Co je šifrované v klidu

S nastaveným `YGGARO_DB_PASSPHRASE` — což je požadavek pro ostrý provoz — je obsah šifrovaný algoritmem **XChaCha20-Poly1305** klíčem, který leží v adresáři klíčů a odemyká ho heslo:

- **obsah** — hodnoty záznamů a dokumenty, tedy vaše projekty, zakázky, rizika a rozhodnutí;
- **obsah příloh**, týmž klíčem;
- **uložená tajemství**, například organizační klíč a nastavené adresy webhooků.

V ukradeném souboru databáze naopak čitelné zůstávají — kvůli indexům a replikaci: identifikátory záznamů, názvy entit, cesty a metadata o zařízení a čase. Čitelný je i **bezpečnostní log** (přihlášení s e-mailem a IP adresou, práce se soubory včetně jejich názvů) — je řetězený otiskem, ne šifrovaný. Mimo bezpečnostní log platí: kdo má jen soubor, zjistí, *že* záznamy existují a kolik jich je. Ne co je v nich.

Když klíč k datům nesedí, server **odmítne nastartovat**, místo aby přepsal data, která neumí přečíst.

Plynou z toho dvě povinnosti provozovatele: chránit disk a adresář klíčů běžnými právy souborového systému a **mít kopii hesla mimo server**. Bez něj jsou zálohy trvale nečitelné — o to v tom šifrování jde a platí to i na vás.

## Co odchází ze stroje

Nic, dokud si to nenastavíte. **Produkt neobsahuje žádnou telemetrii, žádnou analytiku ani kontrolu aktualizací**; nikam se nehlásí a není volba, která by to zapnula.

Odchozí spojení existují jen pro funkce, které si zapnete:

| Kam | Kdy | Co odchází |
|---|---|---|
| Let's Encrypt | je zadaná `-domain` (vestavěné TLS) | jméno domény kvůli vydání certifikátu |
| Váš webhook upozornění (Teams nebo kompatibilní) | správce uloží adresu webhooku | text upozornění |
| Váš webhook na Discord | správce uloží adresu webhooku | text upozornění |
| Microsoft Entra ID | je nastavená rodina `YGGARO_OIDC_*` | jen přihlášení |
| Microsoft Graph / SharePoint | je nastavená rodina `YGGARO_GRAPH_*` (preview) | dokumenty, na které je integrace nastavená |

**MCP je příchozí.** Váš vlastní AI klient se připojuje *k* instanci; instance nevolá žádného poskytovatele AI. Uvnitř téhle edice neběží žádný model a produkt sám do něj data neposílá. Co smí připojený klient číst nebo měnit, je dané právy principála, na kterého je namapovaný — viz [oprávnění MCP](mcp-permissions.cs.md).

## Jak data dostanete ven

Dvě cesty, jedna implementace, takže obě dají tentýž balík:

```bash
# Z aplikace, jako správce (co k tomu potřebuje, viz níže)
# POST /api/admin/export

# Nebo z příkazové řádky — tahle funguje i nad zastavenou instancí
# (pod účtem služby — yggaro-admin, viz instalace krok 6; /srv/export musí patřit účtu yggaro)
yggaro-admin -export /srv/export/yggaro-export.zip
```

V ZIPu je `data/<entita>.json` pro každou exportovanou entitu, `files/` s přílohami pod původními jmény a `manifest.json`, který přesně říká, co uvnitř je a kolik čeho. Je to obyčejný JSON: čitelný bez nás a bez tohohle softwaru. Od 1.0.3 v něm je i stav přečtení diskusí všech uživatelů (`data/readmark.json`: kdo má které vlákno přečtené po kterou zprávu) — správce, který export stáhne, ho tak vidí u všech uživatelů, což aplikace sama neukazuje. Obsahuje také celý bezpečnostní log instance (`data/_security_log.json`): přihlášení včetně neúspěšných pokusů s IP adresou, změny rolí, práv a hesel, exporty a přístupy integrací, každý záznam řetězený otiskem s předchozím. `manifest.json` → `security_log` uvádí počet záznamů a zda řetěz prošel kontrolou, a `README.txt` v balíku popisuje, jak si ho přepočítat sami a co řetěz ukázat neumí. Log pokrývá celou historii bez časového omezení a obsahuje i lidi, kteří uživateli nejsou — IP adresu kohokoli, kdo se pokusil přihlásit (záznamy z verzí do 1.0.2 i identifikátor, který zadal) — takže kdo export stáhne, zachází s ním jako s osobními údaji. Záznamy zapsané verzemi do 1.0.2 mohou obsahovat adresu webhooku notifikací i s tokenem nebo text z pole e-mail, který může být heslem; balík je vyjmenuje a řekne to nahlas. Do logu se zapíše i export pořízený z příkazové řádky serveru.

Cesta z aplikace je záměrně těžší než běžné čtení, protože jedním voláním odchází celý obsah firmy: chce správce, který navíc drží právo `data.export.full` a — protože balík nese bezpečnostní log — i právo `audit.view`, znovuzadání hesla a platnou hlavičku CSRF. Balík se sestaví z konzistentního snímku do dočasného souboru, ověří se úplnost, a teprve pak se pošle — useknutý export se nikdy neodešle jako úspěch. Souběžný export dostane `429`.

Kdyby přílohy nešly přečíst, manifest to řekne a balík označí za neúplný, místo aby vypadal celý.

## Mazání dat

Jednotlivé záznamy se mažou v aplikaci. Když chcete pryč všechno, smažte datový adresář, adresář klíčů a zálohy — a zničte heslo. Protože je obsah šifrovaný tím klíčem, zničením klíče a jeho kopií se stane nečitelným i obsah kopie, na kterou jste zapomněli — kromě bezpečnostního logu, který šifrovaný není; ten je potřeba smazat ve všech kopiích.

Software sám od sebe nic nemaže ani nenechává propadnout. Retence je vaše politika a váš rozvrh.

## Co vidíme my

Nic. Tohle je software, který provozujete vy. K vaší instanci nemáme přístup, nic nám z ní nechodí a vaše heslo neumíme obnovit.

## Související

[Bezpečnostní model](security.cs.md) · [Konfigurace](configuration.md) · [Záloha a obnova](backup-restore.md) · [Oprávnění MCP](mcp-permissions.cs.md)
