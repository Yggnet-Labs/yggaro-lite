# Oprávnění MCP

[English](mcp-permissions.md) · [Čeština](mcp-permissions.cs.md)

Autentizace (OAuth nebo bearer token) jen určí MCP mandát. Oprávnění je průnik:

1. platnosti a stavu revokace mandátu;
2. RBAC a členství namapovaného uživatele;
3. obecných scopes (`mcp.read`, starší `mcp.write`, `mcp.write.high`);
4. doménových capability pro úkoly, chat, dokumenty, rozhodnutí a výstupy;
5. volitelných datových tříd;
6. `confirm:true` pro rizikové akce, pokud mandát výslovně nemá `mcp.write.high`.

Bezpečný výchozí stav je pouze čtení. Doménové capability udělujte jednotlivě. Pro běžné klienty nepoužívejte `all` ani `mcp.write.high`. Návrh a rozhodnutí/přijetí mají záměrně oddělená oprávnění.

Tokeny se ukládají jako hash a plaintext se ukáže jednou. Mandát má výchozí platnost 90 dní, maximum 365. Smazání tokenu z klienta není revokace: odvolejte mandát na serveru a ověřte, že další volání selže. Vydání, změna tříd a revokace se bezpečnostně auditují.
