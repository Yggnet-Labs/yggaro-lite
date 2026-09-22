# Bezpečnostní model

[English](security.md) · [Čeština](security.cs.md) · [Hlášení zranitelnosti](../SECURITY.md)

Jedna serverová instance patří jedné organizaci. Důvěryhodný je správce OS, ovládání DNS/TLS a držitel hesla databáze. Uživatelé jsou omezeni rolí a členstvím v zakázce. MCP klient jedná jako namapovaný uživatel a nemůže překročit jeho RBAC práva.

- TLS končí ve vestavěném ACME nebo ve výslovně nastavené reverse proxy.
- Hodnoty databáze jsou šifrované v klidu; klíč leží mimo datový adresář. Přílohy a provozní metadata potřebují také ochranu disku/filesystemu.
- Tajemství patří do root-only env souboru nebo správce tajemství, nikdy do Gitu, issues či logů.
- První správce potřebuje bootstrap token.
- MCP omezuje expirovatelný mandát, scopes, capability, datové třídy, RBAC, potvrzení rizikové akce a revokace.

Netvrdíme, že máme externí penetrační test nebo certifikaci. Provozovatel odpovídá za aktualizace OS, firewall, DNS, TLS/proxy, offsite zálohy a tajemství.
