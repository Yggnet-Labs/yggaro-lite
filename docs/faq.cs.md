# Časté otázky

[English](faq.md) · [Čeština](faq.cs.md)

**Je to Mesh?** Ne. Vydává se single-tenant serverová edice. Mesh je odložený.

**Je to open source?** Ne. Serverová binárka je pod FSL-1.1-ALv2. Zdroj aplikace v tomhle repozitáři není. Vlastní self-host té binárky je povolený, konkurenční hostovaná služba ne.

**Posílá data do AI?** Uvnitř této edice neběží model. Vlastního AI klienta lze připojit přes MCP a výslovně mu udělit omezený přístup.

**Kde leží data?** V datovém adresáři instance a stromu příloh na vašem stroji. Volitelné integrace posílají jen data pro nastavený účel.

**Lze zálohovat a exportovat?** Ano. Viz [záloha a obnova](backup-restore.md); server umí také čitelný ZIP export.

**Podporovaný self-host?** Ubuntu 24.04 na `linux-amd64` pro vydání 1.0.x, pokud release notes neřeknou jinak.

**Posílá vám to něco?** Ne. Žádná telemetrie, žádná analytika, žádná kontrola aktualizací — a ani volba, která by to zapnula. Jediné spojení, které produkt naváže sám, je na Let's Encrypt kvůli certifikátu. Viz [data a soukromí](data-and-privacy.cs.md).

**Jak dostaneme data ven?** ZIP s obyčejným JSONem a vašimi přílohami, z aplikace nebo z příkazové řádky — druhá cesta funguje i nad zastavenou instancí. Je čitelný bez tohohle softwaru. Viz [data a soukromí](data-and-privacy.cs.md).

**Co když produkt přestanete vyvíjet?** Data máte u sebe a exportují se do obyčejného JSONu. Licence navíc každou verzi dva roky po jejím zpřístupnění převádí na Apache-2.0 — to je součást licence, kterou dostáváte dnes, ne slib do budoucna. Viz [LICENSING.md](../LICENSING.md).

**Jak velký stroj je potřeba?** Malý: 2 vCPU a 4 GB RAM obslouží běžný tým. Tahle edice roste tak, že každá organizace dostane vlastní instanci, ne tak, že by se jedna clusterovala.

**Co ve verzích 1.0.x zatím není?** Zakázky se v aplikaci zakládají i mění, ale přes MCP jsou zatím jen ke čtení a projekty jde založit, ne vypsat či upravit — [roadmapa MCP](mcp-roadmap.cs.md) říká, co přijde dál a v jakém pořadí. Mesh a Lite AI jsou samostatné produkty bez data vydání. Binárky mají kontrolní součty, ne podpis kódu.

**Pomoc?** Viz [SUPPORT.md](../SUPPORT.md). Bezpečnostní chyby hlaste soukromě.
