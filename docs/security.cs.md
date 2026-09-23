# Bezpečnostní model

[English](security.md) · [Čeština](security.cs.md) · [Hlášení zranitelnosti](../SECURITY.md)

Jedna serverová instance patří jedné organizaci. Důvěryhodný je správce OS, ovládání DNS/TLS a držitel hesla databáze. Uživatelé jsou omezeni rolí a členstvím v zakázce. MCP klient jedná jako namapovaný uživatel a nemůže překročit jeho RBAC práva.

- TLS končí ve vestavěném ACME nebo ve výslovně nastavené reverse proxy.
- Obsah databáze **i obsah příloh** je šifrovaný v klidu týmž klíčem; klíčový materiál leží mimo datový adresář. Identifikátory záznamů a metadata replikace zůstávají čitelné, aby fungovaly indexy — ochrana disku a souborového systému tedy zůstává součástí obrany, ne její náhradou. Viz [data a soukromí](data-and-privacy.cs.md).
- Služba běží pod vlastním neprivilegovaným účtem; jediné oprávnění, které si ponechá, je naslouchat na portech 80/443 (`CAP_NET_BIND_SERVICE`), a sandbox systemd jí dovolí zapisovat jen do jejího datového adresáře. Viz [instalace](install.cs.md).
- Tajemství patří do root-only env souboru nebo správce tajemství, nikdy do Gitu, issues či logů.
- První správce potřebuje bootstrap token. Od 1.0.2 server s prázdnou databází bez tokenu nenastartuje a bez passphrase k databázi nenastartuje vůbec — místo aby potichu běžel nechráněný.
- MCP omezuje expirovatelný mandát, scopes, capability, datové třídy, RBAC, potvrzení rizikové akce a revokace.

Netvrdíme, že máme externí penetrační test nebo certifikaci. Provozovatel odpovídá za aktualizace OS, firewall, DNS, TLS/proxy, offsite zálohy a tajemství.
