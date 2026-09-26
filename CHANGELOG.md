# Changelog — Yggaro Lite

Verze se řídí schématem `MAJOR.MINOR.PATCH` ([VERSIONING](VERSIONING.md)). Verzi,
kterou máte, vypíše `yggaro-server -version`; totéž vrací `/healthz`. Jak ověřit
stažené vydání: [release-verification](docs/release-verification.md).

## [1.0.3] — 26. 9. 2026

**Úplný export funguje i na instancích, kde se používají diskuse.** Ve verzích
1.0.0 až 1.0.2 selhal export dat, jakmile na instanci někdo otevřel diskusní
vlákno: aplikace si ukládá osobní stav přečtení a export tento druh dat neměl
zařazený. Z administrace (`POST /api/admin/export`) export nešel stáhnout vůbec
(HTTP 500 „export je nekompletní“); příkazová řádka (`-export`) skončila chybovým
kódem a balík byl označený jako neúplný (bez stavu přečtení).

* Stav přečtení diskusí všech uživatelů se nově exportuje (`data/readmark.json`)
  a export je úplný (`manifest.json` → `complete: true`).
* Nový test prochází zdrojový kód serveru i webového rozhraní a selže, pokud v něm
  přibude druh dat bez vědomého zařazení do exportu. Návrat téže chyby z nového
  kódu tím výrazně ztěžuje.

**Co to znamená při aktualizaci:** data ani konfigurace se nemění, stačí vyměnit
binárku. Návrat na 1.0.2 je opět jen výměnou binárky. Postup: [upgrade](docs/upgrade.md).

## [1.0.2] — 25. 9. 2026

**Serverová edice odmítne nebezpečnou konfiguraci, místo aby ji potichu přijala.**
Obojí dokumentace od 1.0.0 označovala za povinné, kód to ale nevynucoval:

* **První správce jen s tokenem.** S prázdným `YGGARO_BOOTSTRAP_TOKEN` mohl prvního
  superadministrátora založit kdokoli, kdo se na adresu instance trefil dřív než
  provozovatel. Nově server bootstrap bez tokenu vždy odmítne (403) a první
  spuštění s prázdnou databází bez tokenu nenastartuje. Už založená instance
  token nepotřebuje.
* **Klíč k databázi jen z passphrase.** Bez `YGGARO_DB_PASSPHRASE` server
  nastartoval a klíč si uložil do souboru na stejném stroji jako data. Nově bez
  passphrase nenastartuje, a to dřív, než by na disk cokoli zapsal.
* **`-no-encrypt` jen lokálně.** S veřejnou doménou nebo adresou mimo loopback ho
  server odmítne.
* Odmítnutí kvůli konfiguraci končí kódem **78** s čitelnou zprávou; jednotka
  v návodu má `RestartPreventExitStatus=78`, takže systemd restart netočí dokola.

**Co to znamená při aktualizaci:** instalace podle návodu (passphrase i token
v `/etc/yggaro-server.env`) se nemění. Instalace, která vznikla **bez
passphrase**, po aktualizaci nenastartuje, dokud to provozovatel výslovně
nepotvrdí proměnnou `YGGARO_ALLOW_LOCAL_KEY=1`. Passphrase jí nepřidávejte: data
jsou zašifrovaná souborovým klíčem a s passphrase by se neotevřela. Návrat na
1.0.1 je výměnou binárky, formát dat se nemění. Postup: [upgrade](docs/upgrade.md).

**Služba běží bez roota.** Návod instaluje server pod vlastním účtem `yggaro`
jen s oprávněním navázat porty 80 a 443 a s omezeným přístupem k souborovému
systému. Údržbové příkazy se spouštějí pod týmž účtem. Návod k přechodu
existující instalace začíná zálohou a zkouškou obnovy, bez nich nepokračuje.

**Údržbové příkazy nad neexistující instancí nic nezaloží.** Překlep v `-data` u
zálohy dřív skončil úspěchem a zálohou prázdné databáze, kterou si příkaz sám
založil. Nově `-backup`, `-verify-restore`, `-export`, `-reset-password`,
`-mcp-token` a správa OAuth klientů nejdřív bez zápisu ověří, že v `-data` leží
založená instance, jinak skončí chybou. `-verify-restore` je jen pro čtení
a dešifruje **všechny** uložené hodnoty, ne vzorek; přílohy neověřuje a říká to.

**Vynucené dvoufázové ověření platí i pro připojení aplikací.** Když organizace
vyžaduje 2FA a uživatel ho ještě nemá nastavené, smí po přihlášení heslem jen
dokončit jeho nastavení. Obrazovka souhlasu vestavěného OAuth serveru to
nekontrolovala: uživatel s vydaným MCP mandátem tak mohl připojit aplikaci (např.
Claude) a přes MCP číst data dřív, než 2FA dokončil. Nově dostane vysvětlení ve
svém jazyce a souhlas nejde udělit ani přímým odesláním formuláře. Dřív vydané
tokeny tahle změna neruší.

**Vydání nese licenci produktu.** `LICENSE` a `NOTICE` jsou přílohou vydání
pokrytou `SHA256SUMS`. `-third-party-notices` tiskne aktuální oznámení třetích
stran (1.0.1 tiskla text z 1.0.0); vydání se nepostaví, když se text v binárce
liší od přílohy.

**Kreslicí plocha a editor dokumentů mají zase své styly.** Zpřísněná
Content-Security-Policy blokovala styly, které si Excalidraw a editor vkládají
samy; nově je dostávají s jednorázovým nonce stránky. Politika se neoslabuje.

**Integrace.** Microsoft Teams: upozornění smí jít i na adresy Power Platform
(`*.environment.api.powerplatform.com`), jen tato úzká doména. Discord: slash
příkaz a modal dostávají platné potvrzení viditelné jen autorovi a nepodporované
typy interakcí se odmítají s HTTP 400. Záznam o přijaté zprávě z chatu nese
instalaci a ID zprávy; starší záznamy se zpětně nedoplňují.

**SSO: dokumentace odlišuje, co je ověřené.** Příručka v aplikaci rozlišuje seznam
povolených skupin v aplikaci (ověřeno proti skutečnému tenantu Microsoft 365),
členství přímo v Entra ID (neověřeno) a už otevřenou relaci (odebrání ze skupiny
ji neukončí).

## [1.0.1] — 22. 9. 2026

**Opravné vydání. Kdo provozuje 1.0.0 s ukázkovými daty, měl by aktualizovat.**

**Ukázková data už nerozdávají veřejně známé heslo.** Instalační průvodce
nastavoval všem ukázkovým uživatelům pevné heslo, které bylo čitelné v každé
stažené binárce. Nově se heslo generuje náhodně a ukáže se jednou, stejně jako
obnovovací kódy.

**Co s tím, když už 1.0.0 provozujete s ukázkovými daty:** aktualizace hesla
nezmění. Ve správě uživatelů ukázkové účty zrušte, nebo jim nastavte nová hesla.

**Seznam otisků pokrývá celou sadu příloh.** `SHA256SUMS` nově vzniká ze všech
konečných souborů vydání a vydání se nepostaví, když soubor zůstane mimo něj.

**Oba balíky JavaScriptu mají doložený původ.** Editor a kreslicí plocha se staví
ze zdroje s uzamčenými verzemi a licenční seznam se generuje z lockfile.

## [1.0.0] — 22. 9. 2026

**rc17 (20. 9.) — čerstvé přihlášení už na pohledu Server nelže o šifrování.**
Veřejné `/api/status` dál záměrně nevydává citlivou šifrovací posturu, ale UI po
každém úspěšném vzniku session (bootstrap, heslo včetně 2FA a SSO callback) stav
načte znovu jako přihlášené. Administrace → Server proto hned ukáže „zapnuto“ a
zdroj klíče; reload stránky už není potřeba. Go regresní test drží anonymní a
přihlášený kontrakt API, Playwright test skutečný čerstvý login do šifrované
serverové instance.

**rc16 (20. 9.) — bezpečnostní vydání po vnější kontrole R7 (pravidlo dvou očí).** (1) **Go toolchain 1.25.13** pevně v `go.mod` (`toolchain`): govulncheck 33 → 0 volaných zranitelností ve stdlib (Go 1.25.0 měl otevřené CVE v net/http, crypto/tls a dalších). (2) **CSP bez `'unsafe-inline'` pro elementy** — per-response nonce, viz odstavec níže; přiznaný dluh `script-src-attr`/`style-src-attr` (SECURITY.md); nezávislá revize Grok. (3) **SharePoint: složky zakázky vznikají i pro zakázky založené z UI** — od Fáze B jde UI přes `/api/command CreateOrder`, ale auto-založení složek (a serverový bezpečnostní audit mazání/práv) viselo jen na `/api/ops`; zakázka z UI tak nikdy nedostala složky ani odkaz, fungovalo jen ruční tlačítko. Obě cesty teď sdílejí jednu funkci `afterApplied` (broadcast + audit + SharePoint + události); regresní test proti falešnému Graphu. Nalezeno živým M4 E2E na smoke (25/25 PASS), nezávislá revize Codex. (4) Nasazené hlavičky (HSTS 1 rok, nosniff, DENY, Referrer-Policy, Permissions-Policy) na všech veřejných hostech — mimo binárku, v proxy. Ověření rc16: `go test`/`go vet`, Playwright CSP test, živě na smoke (nonce, hlavičky), zkušební provisioning přes lite-plane TEST. Otevřené po vydání (C): migrace inline atributů (236 onclick + 1110 style=), COOP/COEP/CORP, HEAD 501 na /portal, Graph base per-Server místo globální proměnné.

**CSP nonce pro spustitelné elementy (20. 9., R7).** Server nyní pro každou
HTML odpověď generuje nový 128bit nonce a stejnou hodnotu vloží do CSP i do
inline `<script>`/`<style>` elementů hlavního UI a embedded OAuth obrazovek.
`script-src`, `script-src-elem`, `style-src` ani `style-src-elem` už neobsahují
`'unsafe-inline'`; statické assety zůstávají povolené jen ze `'self'`. Index se
kvůli nonce nikdy nesdílí mezi odpověďmi (`Cache-Control: no-store`); 304 je pro
HTML záměrně vypnuté, aby prohlížeč nespojil staré tělo s novou CSP hlavičkou.
Dočasná kompatibilní hranice je explicitně zúžená na `script-src-attr` a
`style-src-attr`, protože stávající jednosouborové UI generuje event a style
atributy za běhu; její odstranění vyžaduje samostatnou migraci těchto atributů.
Regresní test hlídá délku, shodu i čerstvost nonce a oddělení elementových
direktiv od atributových.

**SSO: povolená skupina je podmínka přihlášení (16. 9., owner `oa_1636759dc4`).** Správný tenant a MFA samy o sobě nejsou povolení ke vstupu do aplikace. Callback teď po ověření tokenu — a **před** párováním, JIT účtem i session — rozhoduje podle skupinových claims proti novému nastavení `settings.ssoAllowedGroups`. Pravidlo platí i pro **už existující** SSO účet (jinak by stačilo se jednou přihlásit před odebráním ze skupiny). Vše nejisté **odmítá**: prázdný nebo nečitelný seznam, poškozený seznam, token bez skupin i overage (Entra při překročení limitu místo seznamu pošle odkaz v `_claim_names`). Důvody jsou strojové a rozlišené (`sso_group_not_configured`, `sso_group_not_member`, `sso_group_overage`, `sso_group_claim_missing`, `sso_group_config_unreadable`) — administrátora nemá hnát hledat chybu v oprávněních, kde žádná není. Druhá vrstva: `ssoProvision` bez přijetí nezaloží ani nespáruje účet. Odepření přístupu **nemaže data** ani nesahá na lokálního recovery správce; tenant/issuer/audience/podpis/nonce/MFA zůstávají beze změny. Neměřeno zatím: chování proti živému tenantu (retest pod M4) a **vnořené skupiny** — vyhodnocuje se přesně to, co Entra do tokenu dá. Seznam je zároveň v karanténě `remoteSecuritySensitive` (ze sítě se nepřijímá — jinak by si peer přidal vlastní skupinu) a měnit ho smí jen právo `admin.settings`; obojí kryté testem. Seznam se nastavuje v administraci (Nastavení → Přihlašování → Povolené skupiny), jedno Object ID na řádek, s readbackem uložené hodnoty.

**SSO: tři díry ve fail-closed kontraktu zavřené (16. 9., nález nezávislého review).** Celý callback proti podepsanému tokenu ukázal, co rozhodovací funkce sama o sobě neukáže: (1) **jedna neplatná položka v seznamu povolených skupin** dřív nevadila — stačila jedna sedící a přihlášení prošlo; teď se validuje každé Object ID (GUID) a jediný nesmysl odmítne **celý** seznam (`sso_group_config_invalid`). (2) **`null` v claimu `groups`** se při dekódování do `[]string` měnil na prázdný řetězec, ten se přeskočil a zbytek pole rozhodl o povolení; claim se teď dekóduje jako `[]any` a jakýkoli neřetězcový prvek znamená „tvaru nerozumím" → odmítnutí (`sso_group_claim_invalid`). (3) **Nečitelné claims** se odmítaly bez jediného řádku v auditu — přibyl strojový důvod `login.sso_claims_unreadable` bez tokenu a bez obsahu claimů. Navíc: token se skupinami v jiném formátu než Object ID (hybridní AD) se hlásí jako `sso_group_claim_unsupported`, ne jako „nejsi členem" — administrátor má hledat chybu v nastavení claimů, ne v členství. Regresní test celé cesty token → session (19 případů, vlastní RS256/JWKS na loopbacku) je nově součástí produktu. **Dodatek téhož dne:** členství se validuje **celé, než se cokoli povolí** — dřív se neznámá hodnota přeskočila a o povolení rozhodl zbytek pole, takže `[povolená skupina, "jmeno-skupiny"]` prošlo. Jedna neznámá hodnota teď odmítne bez ohledu na pořadí. Důsledek pro hybridní tenanty, který je nutné znát: token, kde Entra posílá jména synchronizovaných skupin místo Object ID, nepustí **nikoho** (`sso_group_claim_unsupported`) — řešením je nastavit v registraci aplikace emitování **Group ID**.

**rc15 (8. 9.):** dvě opravy souběhů nalezené oživeným E2E harnessem (otevřené body z rc14): **bezpečnostní log (H3)** — čtení posledního hashe a zápis nového záznamu nebyly serializované, dva souběžné zápisy mohly rozbít řetěz → mutex kolem celé sekvence (`Store.SecLog`, jediná zápisová cesta; `go test -race ./internal/store` ok). **Import JSON z prototypu** — obnova z uzlu přes SSE mohla přepsat lokálně naimportovaná data dřív, než doběhl zápis na uzel (tichá ztráta importu) → import drží zámek proti obnově a čeká na zápis (`importInProgress`, `importJsonData` async). Harness: `until()` umí asynchronní predikáty. Ověření: 3 čisté běhy 450/0 nad opravou i nad merge. Autor oprav Codex (2793c28, 7e38b7a, 0ca6d87), křížová kontrola Claude. NENASAZENO — nasazení na flotilu = samostatné GO ownera.

**rc14 (7. 9. večer):** **oprava regrese rc10–rc13** — první spuštění s „demo daty" posílalo demo uživatele s prázdným polem hesla v hromadné dávce operací; zábrana uzlu `secret-field-via-dedicated-endpoint` (od 31. 7.) celou dávku odmítla a instance zůstala prázdná. Klient teď tajná pole (`pw`, `password`, `totp`, `backup`, `recovery`) do dávky nikdy nedává (celé dokumenty i cestové operace), hesla jdou jen přes `/api/password`. Dále: sprint (číslo i okno) se počítá v UTC kalendářních dnech — po změně letního času ukazoval předchozí sprint; klient bez oprávnění admina už neposílá operaci na nastavení (uzel ji odmítal a s ní zahodil celou dávku změn). **E2E harness `tests/e2e.js` znovu živý** (heslo v požadavku na obnovovací kódy, blok obnovy na konci, kontrola stavu uzlu po seedu, čekání na perzistenci importu): 450 kontrol. **Otevřené (rc15, před otevřením prodeje):** import JSON z prototypu je v harnessu nedeterministický (2 ze 3 běhů zelené, jednou se import na klientu vůbec neprojevil do 8 s — podezření na souběh s obnovením z uzlu přes SSE); jednou pozorováno `seclog intact=false` při souběžném čtení `/api/db` — obojí k diagnostice. Follow-up: lokální aritmetika dnů v burndown / cycle time / EVM. GO ownera `oa_9c4ab96892` + `oa_4b4baa10fb`; křížová kontrola Claude (build z větve Codexe 450/0, merge 450/0 + 1× import flake).

**rc13 (7. 9.):** **akceptace výstupů** — výstup (deliverable) zakázky
lze **přijmout nebo odmítnout** s poznámkou; server zapíše kdo/kdy a auditní záznam.
Rozhodovat smí jen PM zakázky, administrátor nebo člen s právem `order.control`
(řadový člen s `order.daily` ne); jedno rozhodnutí na výstup, další ho přepíše —
žádné vícekolové schvalovací řetězce (rozhodnutí ownera 23. 8. + 4. 9., minimální
tvar). Výstup bez rozhodnutí je **neposouzeno**: hotové úkoly přijetí nenahrazují
a `get_scope_status` to říká oddělenými čísly (`accepted` / `rejected` /
`notEvaluated`, `acceptanceTracked: true`; `fullyDone` zůstává pokrytí úkoly).
Nový příkaz `AcceptDeliverable` (REST `/api/command` i MCP `accept_deliverable`,
capability `mcp.deliverable.write`), v UI badge + tlačítka Přijmout/Odmítnout na
kartě výstupu (6 jazyků), manuál a AI reference dorovnány. **Migrace: žádná** —
stávající výstupy zůstávají „neposouzeno“, export vydává jen to, co vzniklo
(test). Intent `int-draft-ad979346`.

**rc10 (16. 8.):** vydání kvůli SROVNÁNÍ FLOTILY. Demo a o2 běžely na rc8,
ntt na rc9 — a ntt navíc na netagované hlavě mainu, která se hlásila týmž
řetězcem „1.0.0-rc9" jako tag. Verze pak neurčovala kód, což je přesně past
popsaná v MCP příručce; rc10 ji ruší tím, že tag a hlava sedí. Kód serveru
se proti rc9 nemění.

Obsahově přibývá **opravený AI playbook (CS+EN)**, který je embedovaný
v binárce a servíruje se přes `/api/playbook` a `search_docs` — instance tedy
do teď připojeným AI podávaly text ze 14. 8. s tvrzeními, o nichž už víme, že
neplatí. Prošel dvěma verifikacemi: adversariální proti kódu (Codex) a
praktickou proti živé rc9 instanci (Cowork, jen čtecí volání). Mimo jiné:
`get_changes_since` je auditní proud, ne přehled · `openRisks` počítá i
`mitigated`, takže se neshoduje s `list_risks` · `search_docs` je česky slepý,
proto se AI má ptát anglicky · `instance_info` nevrací `frameworkProfile` ·
autoritou pro zápis je `allowedWriteTools`, ne `scopes` · „rizika", která jsou
strojovým otiskem semaforu, se nemají reportovat jako rizika.

**rc9 (15. 8.):** přepínač `YGGARO_MCP_OAUTH_COMPAT=1` — úsporný tvar AS
metadat podle doloženě fungujícího cizího custom konektoru claude.ai. Porovnání
metadat řádek po řádku ukázalo, že jsme proti němu „ukecaní": inzerujeme tři
metody ověření klienta místo jedné, 14 scopes místo dvou a navíc `iss`. Klient
si z bohatšího inzerátu vybírá složitější cestu (14. 8. si takhle vybral
client_secret_post). V compat režimu inzerujeme jen `none`, jen `mcp.read`
a `iss` neinzerujeme ani neposíláme. Jména scopes se NEmění (visí na nich
mandáty), zužuje se jen to, co si klient smí vyžádat. Výchozí stav beze změny;
je to experiment k reklamaci připojení, ne nová politika.

**rc8 (15. 8.):** ① **přihlašovací a souhlasová obrazovka v 6 jazycích**
(cs, en, de, pl, sk, hu — týž seznam jako UI a manuál), jazyk podle prohlížeče,
**fallback angličtina**. Byly natvrdo česky, přitom je to jediné místo produktu,
které uvidí i člověk, který se teprve přihlašuje. ② **Přesměrování s autorizačním
kódem nově 303 See Other místo 302 Found.** Souhlas se odesílá POSTem a 303 je
přesně pro tenhle případ; u 302 může programový klient metodu zachovat a poslat
na callback POST, který tam nikdo nečeká — projeví se to jako „kód vydán, token
endpoint nikdo nezavolal". Na tenhle rozdíl nezávisle ukázaly dvě rešerše
a doloženě fungující cizí custom konektor pro claude.ai 303 používá. Pro
prohlížeč se nemění nic, sémanticky je 303 správně tak jako tak.

**rc7 (15. 8.):** oprava, bez které byli confidential klienti z rc6 v praxi
nepoužitelní. Do konektoru se vyplňují **dvě** hodnoty, ale administrace
**Client ID vůbec nezobrazovala** — modal po vytvoření ukázal jen tajemství
a tabulka klientů měla sloupce Název / Metoda / Otisk / Poslední použití.
API `id` vracelo, obrazovka ho zahodila. Uživatel tedy neměl kde vzít půlku
údajů a do pole Client ID vyplnil jméno klienta; připojení pak selhalo dřív,
než se cokoli dotklo serveru, a navenek to vypadalo jako chyba klienta.
Nově: Client ID je v okně po vytvoření i po rotaci a je vlastním sloupcem
v tabulce (Client ID není tajemství, v OAuth je veřejné — tajemství zůstává
jednorázové). K tomu **logování odmítnutých OAuth požadavků**: instance
servíruje TLS sama, takže nemá access log, a bez něj nešlo odlišit „server to
odmítl" od „klient nám vůbec nezavolal" — v obou případech je v datech nula
žádostí a nula kódů. Logují se jen veřejné hodnoty (kód chyby, popis,
client_id), nikdy tajemství, kódy ani tokeny. Manuály CS+EN doplněny o to, že
Client ID je `yoc_…` a **není to název**, a že do tajemství nepatří token
`ymcp_`.

**rc6 (15. 8.):** **confidential OAuth klienti** — ruční Client ID + Secret.
Proč: DCR cesta se u klikacích konektorů claude.ai láme (server vydá
autorizační kód, klient si ho nikdy nevyzvedne — `anthropics/claude-ai-mcp`
#215), zatímco ručně vložený Client ID + Secret v Advanced settings funguje
a sám Anthropic ho doporučuje. Do 1.0.0-rc5 jsme uměli jen veřejné klienty,
takže jediná fungující cesta nám chyběla.
Obsahuje: DCR vydává i confidential klienty a **vynucuje přesně tu metodu,
kterou klient zaregistroval** (jiný transport tajemství = 401) · ruční
životní cyklus přes API, UI i CLI nad jednou doménovou službou — právo
`oauth.clients.manage` + step-up heslem, tajemství se zobrazí **jednou**,
rotace s překryvem 0–24 h (běžící konektor rotace neshodí; překryv 0 zabíjí
staré tajemství okamžitě, což je cesta při úniku), odvolání v jedné transakci
ruší klienta, granty i vydané tokeny · ruční klient nemá expiraci a sleduje se
podle „posledního použití" (expirace by konektor po čase tiše zabila) ·
**metriky autorizačních kódů jako monotónní čítače** (vydáno / vyměněno /
vypršelo nevyměněno + živý gauge čekajících) — dřív se počítaly z tabulky,
kterou úklid maže, takže selhání „klient si kód nevyzvedl" bylo pět minut po
pokusu neviditelné a vypadalo jako „nikdy se nic nestalo" · **oddělené limity
na `/oauth/authorize`**: neplatné validace přísně po IP, platné starty
`IP+client_id` 120/10 min — dřív sdílela celá firma za jedním NATem osm
pokusů za deset minut, a započítávaly se přitom úspěchy místo selhání ·
audit `oauth.client.create/rotate/revoke` včetně CLI cesty.
Ověřeno živě proti instanci za reverzní proxy: **56/56** (všechny inzerované
metody celým řetězem DCR → authorize → souhlas → token → tools/list, negativní
matice transportu, ruční klient včetně rotace, odvolání i auditu), dvakrát po
sobě bez restartu.

**rc5 (14. 8. večer):** OAuth interop pro klikací konektory dotažen podle
skutečného chování klientů, ne podle domněnek. **Blokátor:** metadata
inzerovala tři metody ověření klienta (`none`, `client_secret_basic`,
`client_secret_post`), ale registrace uměla vydat výhradně veřejného klienta —
claude.ai si podle inzerátu vybral `client_secret_post` a jeho konektor se
nešel zaregistrovat. Nově inzerát říká pravdu a požadavek na confidential
metodu se podle RFC 7591 §3.2.1 sníží a **přizná v odpovědi** místo tvrdého
odmítnutí. K tomu discovery tvary pro claude.ai (path-aware/OIDC well-known,
RFC 8707 `resource` nepovinný a lomítko-tolerantní) a **použitelnost souhlasu**:
tlačítka se po odeslání zakazují (dvojklik dřív přebil úspěšné udělení přístupu
strojovou chybou), rozhodnutí jde skrytým polem a už spotřebovaná žádost vrací
lidské vysvětlení místo `invalid_request`. Bezpečnostní chování beze změny —
PKCE S256, přesná redirect URI a jednorázový handle platí dál.

**rc4 (14. 8. večer):** vestavěný OAuth 2.1 authorization server pro klikací
konektory (claude.ai/Claude Desktop/ChatGPT/Claude Code login): DCR + PKCE
S256, consent nad živým mandátem (OAuth mandáty nevyrábí, jen propůjčuje),
opaque tokeny s rotací a replay revokací, rollout flag `YGGARO_MCP_OAUTH=1`
(default vypnuto). K tomu interop opravy ověřené skutečným Claude Code
klientem (loopback DCR bez application_type, zužování scope, /mcp za reverse
proxy) a AI playbook v2 (CS+EN). Implementace Codex + Claude, vzájemné
adversariální review, živý E2E.

**rc3 (14. 8.):** oprava MCP katalogu pro Claude Code — `get_document`
mělo v `outputSchema` boolean podschéma (`content: true`, z Go `any`);
striktní klienti (Claude Code 2.x) kvůli němu zahazovali VŠECH 55 nástrojů
(„Connected · tools fetch failed"). Prázdná podschémata se nově uzemňují
popisem, kontrakt zamčen testem nad živým katalogem. Reklamace ownera,
review Codex APPROVE.

**rc2 (12. 8. pozdě večer):** čtení souborů pro AI — `get_file_content`
(lokální textové přílohy ≤ 1 MiB, poctivá detekce typu z obsahu),
`list_sharepoint_files` + `get_sharepoint_file_content` (přes stávající
Graph integraci) a `list_templates`. Celkem 55 MCP nástrojů (33 čtecích).
Implementace Codex, adversariální review Claude.

Kódový gate rc1: adversariální review Codexem (3 kola, rozsah `b83186b..16ea176`)
uzavřeno verdiktem APPROVE 12. 8. 2026. Součástí i polní přístupová práva
financí a vynucení pohledových práv (rozhodnutí ownera, sémantika A).

**První produkční verze.** Release notes pro zákazníka — souhrn od
`1.0.0-beta5` (15. 7.) do rc1:

- **Dokumentová vrstva:** interní dokumenty (Tiptap editor, immutable verze +
  conflict guard, AI draft bez auto-publish), volitelné úložiště (server /
  SharePoint / odkazy), heslo 2×, knihovní šablony u bran, Otevřít/Uložit ve
  Wordu přes WebDAV, DOCX export ze zákaznické šablony (go-template-docx),
  **MS Project XML (MSPDI) export**, **Excalidraw kreslicí vrstva** (self-hosted,
  offline, sdílený JSON kontrakt s velkým Yggarem).
- **Diskuse a spolupráce (Fáze A):** vlákna a zprávy u zakázky, doručenka,
  konverze zprávy na úkol / riziko / rozhodnutí, odchozí napojení na MS Teams.
- **AI asistent přes MCP — 51 nástrojů (29 čtecích + 22 zápisových):**
  mandáty s okamžitým odvoláním, oprávnění po rodinách nástrojů, datové třídy,
  egress účtenky a neměnný audit; agregované přehledy (zdraví portfolia a
  projektu s oficiálním EVM paritním s UI, „co vyžaduje mou pozornost",
  změny od data, výkazy, scope, agilní tok); atomický zápis ze schůzky
  (deník + úkoly + odkazy jedním voláním); `dryRun`, `idempotencyKey`,
  verzní tokeny (optimistic concurrency); strukturované chybové kódy;
  projekce obsahu dokumentů (metadata / plain_text / structured).
- **AI playbook jako součást produktu:** připravené instrukce pro zákazníkova
  GPT/Clauda (CS+EN), ke stažení přímo z aplikace (`GET /api/playbook`,
  odkaz v manuálu), tatáž znalost dostupná asistentovi přes `search_docs`.
- **Dokumentace:** vestavěný manuál kompletně v 6 jazycích (CS/EN/DE/PL/SK/HU)
  vč. kapitoly o AI přístupu; MCP příručka pro adminy a uživatele (CS+EN).
- **Export dat:** kompletní export zakázky/instance (E1–E3, E5) pro zálohu
  a přenositelnost.
- **SAFe Alignment** (volitelný, default OFF, per-order opt-in): profil + ROAM,
  PI kadence + objectives + poctivá predictability, Feature/Enabler + WSJF,
  dependency + PI report + dependency card DOCX.
- **Kapacitní mřížka** (člověk × týden) + **Zdroje po lidech** (drill-down
  přiřazených úkolů).
- **Bezpečnost/provoz:** CSP zpřísnění + worker-src (kreslicí vrstva),
  server-side sanitizace dokumentů, hash-řetězený seclog jako neměnný audit,
  rate limit + circuit breaker na MCP.
- **Verzní a release identita:** jediný zdroj pravdy verze
  (`internal/version`), build metadata (commit + datum) v `/healthz`,
  `-version` i startovní hlášce, releaseguard (vydání jen z čistého stromu
  s tagem), SBOM, govulncheck, SHA256SUMS, generovaný `VERZE.txt`.

**Vědomě mimo 1.0.0** (přiznáno v manuálu §11): historie verzí dokumentů,
baselines, kapacitní plánování přes MCP, upload souborů přes MCP. (Akceptace
výstupů byla původně také mimo 1.0.0 — rozhodnutím ownera 4. 9. 2026 se vrátila
do 1.0.0 a je součástí rc13, viz výše.) Čtení obsahu souborů (lokální přílohy + SharePoint) přijde ještě
ve v1.0.0 během soak týdne — viz plán.

> ✅ Historický tag `v1.0.0` z 12. 6. 2026 (předprodukční „release" před
> verzní konvencí z 31. 7.) byl 12. 8. přejmenován na `legacy/v1.0-2026-06-12`
> (lokálně i na GitLabu) — jméno `v1.0.0` patří téhle verzi.

## 1.0.0-beta5 (Balík 5) — 2026-07-14 — procesy: přejmenování + práva na proces
- **„Typy" → „Procesy"** napříč UI (všech 6 jazyků) — jen texty, entita `type` beze změny
  (žádná migrace dat). Editor bran zůstává jako „Definice procesu".
- **Práva na proces**: v katalogu (Administrace → Procesy) nový přepínač **„🔒 jen admin"** —
  zakázky daného procesu pak smí zakládat pouze administrátor. Vynuceno **na serveru** (RBAC při
  vzniku zakázky kontroluje `type.createRoles`), i v UI (běžný uživatel takový proces nevidí ve
  výběru při zakládání). Test `TestRoleAllowedToCreate`. Mesh i Server identické.

## 1.0.0-beta4 (Balík 4) — 2026-07-14 — repozitář šablon zakázek
- **Šablony zakázek**: opakovaně použitelný skelet zakázky. U zakázky nové tlačítko
  **„🗂 Uložit jako šablonu"** (jen admin) uloží typ procesu, metodiku, poznámky, **milníky,
  výstupy i úkoly** jako šablonu. Při zakládání zakázky nový výběr **„Z šablony"** vše naklonuje
  s čerstvými ID (milníky→výstupy se správně přemapují, úkoly bez řešitele ve stavu „todo").
- **Administrace → Šablony**: přehled šablon (typ, obsah = počet milníků/výstupů/úkolů, kolik
  zakázek z ní vzniklo), přejmenování/popis, mazání.
- Nová entita `template` v oplogu — **RBAC: zápis jen `admin.types`** (jako procesní typy),
  čtení v snapshotu pro všechny (bez tajných dat); mazání jde do seclogu. Mesh i Server identické.

## 1.0.0-beta3 (Balík T) — 2026-07-14 — tikety: výkazy + upozornění
- **Výkazy práce** (nová položka menu „Výkazy", ikona ⏱): týdenní grid odpracovaných hodin
  podle osob, čerpaný z existujícího worklogu tiketů (`x.logs[]`). Navigace po týdnech, filtr
  podle zakázky, součty na osobu / den / tým, **export CSV** (středníky, BOM, čárka jako
  desetinná — pro účetní/Excel). RBAC: manažer (super/admin) a PM vidí celý tým, ostatní jen
  své výkazy. Doplňuje pohled Zdroje (plán) o skutečnost.
- **Upozornění** (zvonek 🔔 v horní liště, odznak s počtem): odvozená schránka bez nové entity —
  moje otevřené úkoly po termínu (🔴) a do 2 dnů (🟠) a **brány, které vlastním** na aktivních
  zakázkách (⚑). Kliknutí skočí na zakázku, u úkolu rovnou otevře detail tiketu.
- Beze změny datového modelu i serveru (čistě odvozené z dat, která už máme) — Mesh i Server
  identické.

## 1.0.0-beta2.6 — 2026-06-12
- **Produkt se jmenuje Yggaro Lite** (velké Yggaro je samostatný, robustnější systém) —
  přejmenováno napříč: binárky `yggaro-lite-*`, UI, výpisy, pozvánka, manuály, návody.
- **Čtyři podrobné manuály** v `release/yggaro-beta2/manualy/` (HTML skripta dle firemního
  stylu, tisk do PDF): uživatelský CS+EN (~105 kB: slovníček, postupy krok za krokem, pole po
  poli, číselný EVM příklad, obsah bran G1–G9, 8 táhel poradce, kapacity, portfolio, matice
  práv, bezpečnost, FAQ) a development CS+EN (~77 kB: architektura se schématy, datový model,
  oplog+HLC+LWW, replikační protokol se sekvenčním diagramem, API tabulka, RBAC matice,
  frontend diff vrstva, život jedné změny, testování, výkon a limity, konvence, ADR souhrn).
  Loga: plot = Yggaro Lite u titulu, strom = Yggnet Labs u copyrightu. Jazyková korektura
  (automatický sken cizích znaků + ruční čtení).
- Vestavěný manuál v aplikaci zrušen (rozhodnutí: velikost binárky) — manuály jsou samostatné.

## 1.0.0-beta2.3 — 2026-06-11 (opravy z 2. kola testu na 2 počítačích)
- **✕ platí trvale**: smazaná adresa se ukládá do blokačního seznamu — mDNS objevování ji už
  nekřísí (dřív se mrtvé adresy z inzerátů vracely každých ~35 s). Ruční přidání adresy blokaci ruší.
- **mDNS kandidáti se nejdřív sondují**: adresa z inzerátu se do seznamu zapíše až po úspěšném
  šifrovaném handshaku — virtuální adaptéry a cizí podsítě v inzerátech (Parallels, druhá Wi-Fi…)
  už nevytvářejí mrtvé karty.
- **Jednosměrné sítě (firewall/NAT)**: příjemce synchronizace si protistranu zapíše z příchozího
  spojení (hello nese i naslouchací port) — uzel za firewallem teď vidí toho, kdo se k němu
  připojuje, jeho přihlášené uživatele i stav online. Dřív „MacBook nevidí Mac mini", ač data tekla.
- NAVOD: upozornění na macOS firewall („Accept incoming connections?" → povolit na obou počítačích).
- Testy: +3 sync unit (sonda kandidátů, trvalá blokace, zápis iniciátora u respondéra), integrace 10/10, e2e 364.

## 1.0.0-beta2.2 — 2026-06-11
- **Oprava závodu při zakládání uživatele**: UI posílalo „nastav heslo" souběžně se „založ
  uživatele" — když heslo dorazilo na uzel dřív, založení (celodokumentová operace, LWW) ho
  přepsalo a uživatel zůstal trvale bez hesla („špatné heslo" na všech uzlech, projevovalo se
  náhodně). Nově se heslo odesílá až po potvrzeném doručení založení; totéž u demo seedu
  a obnovy dat. Pokud vám takto „umřel" účet z bety 2/2.1: admin mu v ✎ nastaví heslo znovu.
- Nový e2e scénář: založení uživatele přes UI → odhlášení → přihlášení novým účtem (364 kontrol).

## 1.0.0-beta2.1 — 2026-06-11 (opravy z reálného testu na 2 počítačích)
- **Mrtví peeři z pozvánky**: pozvánka už nezahrnuje adresy virtuálních adaptérů (Parallels vnic,
  VMware vmnet, Docker, bridge, AWDL…) — na MacBooku s Parallels vytvářely nedostupné karty.
- **Úklid seznamu uzlů**: ✕ na kartě peeru (admin) odebere adresu i z perzistence; adresa vedoucí
  na vlastní uzel se detekuje při handshaku a vyřadí se sama; více adres téhož uzlu se po
  synchronizaci sloučí do jedné karty (dedupe dle ID zařízení).
- **Skuteční „Přihlášení uživatelé"**: uzly si při synchronizaci vyměňují lokálně přihlášené
  uživatele (hello.users) — panel v Síti ukazuje kdo a na kterém uzlu je přihlášen (dříve
  demo logika ukazující prvních N uživatelů — proto se objevoval Marek Novák).
- Integrační test rozšířen na 10 kontrol (prezence, odebrání peeru); sync unit testy +3
  (self-detect, dedupe, hello.users).

## 1.0.0-beta2 — 2026-06-11
- **Replikace mezi uzly** (model Lotus Notes, ADR-003/004/008): uzly jedné organizace si vyměňují
  operační logy podle vektoru verzí — obousměrně, párově a **tranzitivně** (hub topologie funguje
  bez konfigurace). Po lokální změně se synchronizace spouští automaticky (debounce) + každých 30 s.
- **Šifrovaný kanál**: X25519 handshake autentizovaný HMAC z org-klíče → ChaCha20-Poly1305 rámce;
  uzel s cizím klíčem se nepřipojí a nic se mu nevydá. Operace podepsané pozorovatelem se při
  příjmu zahazují.
- **Pozvánka místo klonu**: Síť → „⬇ Pozvánka pro další počítač" (klíč organizace + adresy uzlu);
  nový počítač ji načte na úvodní obrazovce („Připojit se pozvánkou"), stáhne si kompletní data
  a kolega se přihlásí svým účtem — hesla (Argon2id hashe) se replikují.
- **Objevování uzlů**: mDNS v LAN automaticky (vypnutelné `-no-mdns`); přes VPN/internet ruční
  adresa v pohledu Síť (host:port) nebo hub replika (ADR-008).
- **Pohled Síť naživo**: skuteční peeři (online/offline, poslední synchronizace), tlačítko
  ⟳ Synchronizovat, vydání pozvánky, přidání ručního uzlu.
- **Merge zpevněn pro síť**: re-materializace dokumentů při doručení operací mimo pořadí;
  testy konvergence 3 replik s náhodným pořadím doručení.
- Testy: Go unit + replikační scénáře (hub, souběh, cizí klíč, observer), **integrační test dvou
  skutečných binárek 8/8**, e2e UI 362 kontrol.
- Parametry: `-sync-listen 0.0.0.0:7460`, `-no-mdns`.

## 1.0.0-beta1 — 2026-06-11
- **Uzel** (Go + čistě-Go SQLite + vestavěné UI, jediná binárka, win/mac/linux): lokální UI na
  http://127.0.0.1:7456, datový adresář v profilu uživatele (`YGGARO_DATA` jej přepíše).
- **Operační log s LWW merge per pole + HLC hodiny** — základ replikace à la Lotus Notes (ADR-004);
  dávky operací atomicky v jedné transakci; testy konvergence dvou replik.
- **Bezpečnost (ADR-005):** Argon2id hesla (PHC), session cookie HttpOnly+SameSite, CSRF, rate-limit
  přihlášení; hesla výhradně přes /api/password (hash nikdy neopustí uzel); RBAC vynucené jádrem
  (pozorovatel jen čte, uživatel píše jen své zakázky/úkoly, administrace jen admin).
- **Frontend = ověřené UI prototypu v0.17**, mutace tečou diff vrstvou (`save()` → operace → uzel),
  SSE tlačí změny do otevřených oken; demo seed vč. hesel `demo123` přes API.
- **E2E: 356 kontrol** (kompletní smoke prototypu + konzistence uzel↔klient + serverové RBAC) proti
  živé binárce; Go unit testy jádra s -race.
- Klon/import nahradí v Betě 2 replikace + pozvánka; výkazy práce záměrně nejsou (v1.5, NTT je vede jinde).
