# Časté otázky

[English](faq.md) · [Čeština](faq.cs.md)

**Je to Mesh?** Ne. Vydává se single-tenant serverová edice. Mesh je odložený.

**Je to open source?** Ne. Produkt je source-available pod FSL-1.1-ALv2. Vlastní self-host je povolený, konkurenční hostovaná služba ne.

**Posílá data do AI?** Uvnitř této edice neběží model. Vlastního AI klienta lze připojit přes MCP a výslovně mu udělit omezený přístup.

**Kde leží data?** V datovém adresáři instance a stromu příloh na vašem stroji. Volitelné integrace posílají jen data pro nastavený účel.

**Lze zálohovat a exportovat?** Ano. Viz [záloha a obnova](backup-restore.md); server umí také čitelný ZIP export.

**Podporovaný self-host?** Ubuntu 24.04 na `linux-amd64` pro 1.0.0, pokud release notes neřeknou jinak.

**Pomoc?** Viz [SUPPORT.md](../SUPPORT.md). Bezpečnostní chyby hlaste soukromě.
