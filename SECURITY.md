# Bezpečnost — Yggaro Lite

## Hlášení zranitelnosti

Našli jste bezpečnostní chybu? **Nezakládejte veřejný issue.**

Napište na **[security@yggnet.cz](mailto:security@yggnet.cz)**. Do prvního
hlášení patří popis dopadu a bezpečná reprodukce na syntetických datech.
Neposílejte hesla, tokeny, privátní klíče, databáze ani zákaznické údaje.
Pokud jsou pro ověření potřeba citlivé podklady, nejprve si s námi domluvte
způsob jejich předání; běžný e-mail není příslib koncového šifrování.

Pokud můžete, uveďte:

- co jste udělali (kroky k reprodukci),
- co jste čekali a co se stalo,
- verzi (`yggaro-server -version` (serverová edice) nebo `yggaro -version` (Mesh) — vypíše i commit a datum buildu),
- edici (Mesh / serverová).

**Co můžete čekat:**

| | |
|---|---|
| Potvrzení přijetí | do **3 pracovních dnů** |
| První posouzení závažnosti | do **10 pracovních dnů** |
| Informace o postupu | průběžně, dokud se to nezavře |

Jsme malý tým. Neslibujeme reakci do hodin — slibujeme, že vám odpovíme
člověk a že vás necháme vědět, jak to dopadlo, i když nálezu nedáme za pravdu.

**Prosba:** dejte nám čas na opravu, než to zveřejníte. Nemáme na to formální
politiku ani odměny; spoléháme na slušnost a oplácíme ji tím, že vás uvedeme
v poznámkách k vydání, pokud si to přejete.

## Reporting in English

Do not open a public issue for a vulnerability. Email
[security@yggnet.cz](mailto:security@yggnet.cz) with the affected edition,
version, impact and safe reproduction steps using synthetic data. Do not
send passwords, tokens, private keys, databases or customer information.
Agree on a transfer method with us before sharing sensitive evidence;
ordinary email is not a promise of end-to-end encryption.

## Co je a co není zranitelnost

**Je:** obejití autentizace nebo oprávnění, čtení cizích dat, vzdálené spuštění
kódu, únik tajemství, obejití šifrování, pád uzlu z požadavku.

**Není:** chybějící hlavička bez doložitelného dopadu, nálezy z automatického
skeneru bez ověření, sociální inženýrství vůči našim lidem, DoS hrubou silou.

## Podporované verze

Opravy dostává **poslední vydaná verze**. Starší se neudržují — jsme malý tým
a udržovat víc větví by znamenalo dělat to špatně na obou.

## Jak k bezpečnosti přistupujeme

Nemáme externí penetrační test a **netvrdíme, že máme**. Místo papíru děláme
vlastní adversariální prověrku napříč více modely a **každý potvrzený nález
zamykáme testem**, který na neopraveném kódu prokazatelně padá.

Podrobnosti, včetně toho, co aplikace záměrně **nedělá** a co v databázi
**není šifrované**, jsou v bezpečnostním balíčku pro zákazníky (na vyžádání)
a v threat modelu v dokumentaci.

### CSP: nonce a atributová kompatibilita

Serverová i Mesh edice používají pro inline `<script>` a `<style>` elementy
náhodný 128bit nonce, nový pro každou odpověď. Hodnota se nevkládá do sdílené
cache: HTML shell se upraví až při obsluze konkrétního požadavku. Direktiva
`script-src(-elem)` a `style-src(-elem)` proto nepovoluje `'unsafe-inline'`.

Jednosouborové UI zatím generuje řadu atributů `onclick=`, `onchange=` a
`style=` dynamicky. Nonce se podle CSP3 vztahuje na script/style **elementy**,
ne na jejich atributy; ty řídí samostatné direktivy
[`script-src-attr`](https://www.w3.org/TR/CSP3/#directive-script-src-attr) a
[`style-src-attr`](https://www.w3.org/TR/CSP3/#directive-style-src-attr).
Proto jsou atributy dočasně a výslovně povolené jen v těchto dvou direktivách.
Je to omezený kompatibilní dluh, nikoli tvrzení o úplném odstranění inline
atributů. Odstranění vyžaduje převod dynamicky generovaných handlerů na
`addEventListener`/delegaci a inline stylů na třídy; do té doby se zákaz
`'unsafe-inline'` vztahuje na spustitelné elementy, ne na atributy.

HTML dokumenty hlavního UI a embedded OAuth mají navíc
`Cross-Origin-Opener-Policy: same-origin` a
`Cross-Origin-Resource-Policy: same-origin`. JSON API, `/mcp` a discovery
metadata tyto hlavičky záměrně nedostávají: nejsou browsing contexts a externí
konektory je musí číst bez politiky dokumentu. `Cross-Origin-Embedder-Policy`
zatím nezapínáme — UI podporuje zákaznické logo z externí HTTPS adresy a
`require-corp` by ho bez CORS/CORP spolupráce cizího hostitele zablokovalo.

---
*Yggnet Labs s.r.o.*
