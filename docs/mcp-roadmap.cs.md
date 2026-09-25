# Roadmapa MCP

[English](mcp-roadmap.md) · [Nástroje a meze](mcp-tools.cs.md)

**Bez termínů, záměrně.** Slíbit datum, které neumíme doložit, je horší než mlčet. Pořadí ale
říct umíme a držíme se ho.

## Dnes — řada 1.0

56 nástrojů (33 čtení, 23 zápis), vlastní OAuth, mandáty s výchozí platností a okamžitou revokací,
omezení na třídy dat, potvrzení u šesti high-impact akcí, doklad o výdeji dat v bezpečnostním
logu. Úplný seznam i meze jsou v [nástrojích a mezích](mcp-tools.cs.md).

## Nejbližší dávka po vydání

Jedna dávka, ne postupné kapání. Obsahuje dvě věci:

**1 · Úplnější zápis u zakázek.** Dnes největší mezera: novou zakázku asistent založí a v existující
pracuje s jejími částmi (brány, milníky, rizika, výstupy, zápisy z porad), ale samotné údaje
zakázky, třeba název, klienta nebo vedoucího, nezmění.
Chystáme změnu základních údajů zakázky, úpravu milníku, nahrání souboru a schválení verze
dokumentu.

**2 · Průvodce pro připojenou AI.** Aby asistent uměl nového správce provést nastavením —
jak založit bránu, jak z ní udělat šablonu, jak nastavit práva — a nemusel to člověk hledat
v dokumentaci. Mechanismus na to už existuje (`search_docs` nad dokumentací uvnitř binárky);
chybí obsah průvodce a zápis u bran a šablon.

## Jak se MCP liší od chystaného Yggaro Lite AI

Tohle se plete, tak to říkáme rovnou. **MCP není „Yggaro Lite AI".**

- **Yggaro Lite (dnes, řada 1.0)** — produkt vystavuje rozhraní MCP. AI si připojíte **vy**,
  je **vaše**, běží na vašem účtu a na vaše náklady. Uvnitř produktu žádný model není.
- **Yggaro Lite AI (chystáme)** — **tentýž produkt**, ve kterém navíc pracují **agenti
  uvnitř**: automatizují rutinu, vyhodnocují a navrhují. MCP zůstane k dispozici, takže
  půjde mít obojí — vlastního klienta i vnitřní agenty.

Není to tedy jiný produkt, ale vyšší stupeň téhož. Termín neslibujeme.

## Co se v 1.x nechystá

- **Edice Mesh** — jedna aplikace na počítači bez serveru. Jiná edice, odložená, bez termínu.

## Co platí vždy

Každý nový nástroj respektuje **práva uživatele**, pod jehož účtem je klient připojen. Správa
instance zůstává vyhrazená superadministrátorovi a přes MCP se nezpřístupní. Tohle není
doporučení, je to vynucené v kódu — nástroj nemůže vzniknout nezařazený do čtení/zápisu.
