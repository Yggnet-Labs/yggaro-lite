# Licence Yggaro Lite — co smíte a co ne

> ⚠️ **Závazný je soubor [`LICENSE`](LICENSE).** Tenhle dokument je jen shrnutí
> lidskou řečí, aby se nikdo nemusel prokousávat právním textem kvůli otázce
> „smím to použít u nás ve firmě?". Kde se shrnutí a licence rozejdou, platí licence.

Yggaro Lite je pod **FSL-1.1-ALv2** (Functional Source License). Není to OSI open
source. Rozhodnutí o té licenci schválil vlastník produktu 11. 7. 2026 (ADR, sekce Licence).

**23. 9. 2026, co z toho dnes skutečně máte.** Vlastník 22. 9. rozhodl, že zdrojový
kód aplikace se nezveřejňuje (`oa_4d42c2cd6a`). Vydání je serverová binárka a
dokumentace. Řádky níže, které mluví o čtení a úpravě zdroje, opisují text licence.
Nejsou to soubory, které si z tohohle repozitáře stáhnete. Jestli FSL a dvouletý
přechod na Apache-2.0 sedí na vydání bez zdroje, má říct advokát. Tady se to
nerozhoduje a licence se nepřepisuje.

## Krátce

| | |
|---|---|
| ✅ **Smíte** | používat u sebe ve firmě staženou serverovou binárku, provozovat vlastní instanci pro vlastní potřebu a používat ji k neziskové výuce a výzkumu |
| ✅ **Smíte** | nasadit vydanou binárku jako součást služby zákazníkovi, který má licenci. Úpravu zdrojového kódu tohle shrnutí nepovoluje, protože vydání zdroj neobsahuje |
| ❌ **Nesmíte** | nabízet Yggaro Lite (ani produkt s podstatně stejnou funkcí) **jako komerční službu třetím stranám** — tedy konkurovat nám naším vlastním kódem |
| ⏳ **Za dva roky** | každá verze se **automaticky** stane Apache-2.0. Není to slib do budoucna, je to součást licence, kterou dostáváte dnes |

„Za dva roky" se počítá **od zpřístupnění dané verze**, ne od jednoho pevného data.
Verze vydaná dnes je Apache-2.0 přesně za dva roky ode dneška.

## Proč zrovna tohle

Chceme, aby si kdokoli mohl **stáhnout serverovou binárku, přečíst dokumentaci a provozovat ji u sebe**. Zdroj aplikace k tomu dnes přiložený není.
Nechceme, aby ho někdo vzal a prodával jako vlastní SaaS.

Klasické open source licence to neumí oddělit: buď dovolí obojí, nebo nic.
FSL to odděluje a přitom nedělá ze zdrojáku slepou uličku — časový převod na
Apache-2.0 znamená, že i kdyby Yggnet Labs zítra skončil, **text licence počítá
s tím, že se kód za dva roky uvolní**. To není zjištění, že zdroj dnes někde leží.
U vydání bez zdroje ať to posoudí advokát.

Pro zákazníka je to podstatné: nekupujete si závislost, ze které není cesta ven.

## Kanonická verze × fork

**Kanonická verze** je ta, kterou vydává Yggnet Labs (GitHub release, podepsané
binárky). Jen ta dostává:

- bezpečnostní aktualizace a upgrade cestu,
- podporu,
- **účast ve federaci** — identita uzlu je vázaná na kanonickou verzi.

**Fork** si udělat smíte (licence to dovoluje) a je to legitimní. Platí ale, že:

- fork **není** kanonická verze a nesmí se za ni vydávat (viz odstavec o ochranných
  známkách v licenci — jméno a značka Yggaro nejsou součástí grantu),
- fork **nefederuje** s kanonickou sítí; federace stojí na identitě, a identitu
  nelze udělit něčemu, co nikdo nevydal,
- upgrade z forku zpět na kanonickou verzi není podporovaná cesta.

Není to trest, je to důsledek. Federace znamená, že cizí uzel smí ovlivnit vaše
data — a to jde jen tam, kde je jasné, co ten uzel provozuje.

## Co to znamená pro poskytovatele služeb

Jste-li konzultant nebo integrátor a nasazujete Yggaro Lite **zákazníkovi, který
má licenci**, je to výslovně povolený účel. Nepotřebujete od nás nic navíc.

Chcete-li Yggaro Lite provozovat **jako svou vlastní službu pro víc zákazníků**,
to povolený účel není — ozvěte se a domluvíme se.

## Přiznaná mez tohohle dokumentu

Shrnutí psal vývojář, ne právník. Slouží k tomu, aby čtenář rychle pochopil
záměr — **nenahrazuje právní posouzení** a v žádném sporu se o něj nelze opřít.
Závazné je znění v [`LICENSE`](LICENSE).

---
*Otázky k licenci: Yggnet Labs s.r.o.*
