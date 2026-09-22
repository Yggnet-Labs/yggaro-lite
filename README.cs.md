# Yggaro Lite

[English](README.md) · [Čeština](README.cs.md)

Yggaro Lite drží práci pro zákazníky, rozhodnutí, rizika a výstupy na jednom místě. Malý tým tak vidí, co postupuje, co stojí a kdo má rozhodnout dál.

Tento repozitář obsahuje **serverovou edici**. Jedna instance slouží jedné organizaci, má vlastní databázi a běží na vlastním stroji. Můžete ji provozovat sami nebo využít naši službu na [yggarolite.cz](https://yggarolite.cz).

> **Rozsah produktu:** Yggaro Lite Server směřuje k první produkční verzi `1.0.0`. Mesh (peer-to-peer edice pro desktop/LAN) a Lite AI (AI uvnitř aplikace) jsou jiné, odložené produkty. U žádného neslibujeme termín.

## Proč ho týmy používají

- práce je uspořádaná kolem projektů, milníků, bran, rizik a převzatých výstupů;
- rozhodnutí a změny zůstávají dohledatelné místo toho, aby zmizely v chatu;
- každá organizace má oddělenou instanci a může svá data exportovat;
- zákazník může připojit vlastního AI klienta přes hlídané MCP; Yggaro Lite sám data aplikace žádnému modelu neposílá.

## Self-host stručně

Podporovaný cíl prvního vydání je Ubuntu 24.04 na `linux-amd64`, veřejná doména a porty 80/443. Stáhněte binárku vydání a `SHA256SUMS`, ověřte je a pokračujte [českým instalačním návodem](docs/install.cs.md).

```bash
sha256sum -c SHA256SUMS
./yggaro-server -version
```

Nenasazujte náhodnou větev ani automatický zdrojový archiv GitHubu. Po vydání `1.0.0` používejte jeho artefakty s kontrolními součty.

## Dokumentace

**Rozjet** — [Instalace](docs/install.cs.md) · [Konfigurace](docs/configuration.md) · [Architektura](docs/architecture.md)

**Provozovat** — [Provoz](docs/operations.md) · [Záloha a obnova](docs/backup-restore.md) · [Aktualizace](docs/upgrade.md) · [Když něco nejde](docs/troubleshooting.cs.md)

**Důvěřovat** — [Bezpečnostní model](docs/security.cs.md) · [Data a soukromí](docs/data-and-privacy.cs.md) · [Ověření vydání](docs/release-verification.md) · [Hlášení zranitelností](SECURITY.md)

**Připojit vlastní AI** — [MCP](docs/mcp.cs.md) · [Oprávnění](docs/mcp-permissions.cs.md) · [Nástroje a jejich meze](docs/mcp-tools.cs.md) · [Roadmapa](docs/mcp-roadmap.cs.md)

**Ostatní** — [FAQ](docs/faq.cs.md) · [Podpora](SUPPORT.md) · [Verzování](VERSIONING.md) · [Pravidla chování](CODE_OF_CONDUCT.md)

## Licence

Yggaro Lite je **source-available, nikoli OSI open source**, pod FSL-1.1-ALv2. Vlastní interní provoz, studium a úpravy jsou povolené; nabízet konkurenční komerční službu třetím stranám ne. Čtěte [LICENSE](LICENSE) a [NOTICE](NOTICE). Rozhoduje úplný text licence, ne toto shrnutí.

## Vývoj

Zdrojový strom zatím v tomhle repozitáři není — najdete tu dokumentaci a vydání. Než přibude, jsou issues a dotazy vítané, ale pull request nemá co přeložit.

Jak budeme příspěvky přijímat, popisuje [CONTRIBUTING.md](CONTRIBUTING.md). Zranitelnosti hlaste soukromě podle [SECURITY.md](SECURITY.md).
