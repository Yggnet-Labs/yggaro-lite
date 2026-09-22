# Připojení AI klienta přes MCP

[English](mcp.md) · [Čeština](mcp.cs.md) · [Seznam nástrojů a meze](mcp-tools.cs.md) · [Oprávnění](mcp-permissions.cs.md)

MCP dovolí vlastnímu AI klientovi zákazníka pracovat s Yggaro Lite. Není to „AI uvnitř Yggaro Lite“: žádný model není součástí produktu a server sám data modelu neposílá.

**Je to zcela volitelné a ve výchozím stavu vypnuté.** Yggaro Lite funguje naplno i bez jakékoli AI: nic z toho, co je tady popsané, není k provozu produktu potřeba a tím, že MCP nezapnete, nepřijdete o žádnou jinou funkci. Zůstane vypnuté, dokud ho správce výslovně nezapne.

## Zapnutí endpointu

Přidejte `YGGARO_MCP=1` do prostředí služby a restartujte ji. Streamable HTTP endpoint je `https://vase-domena.cz/mcp`. Vestavěné OAuth je volitelné přes `YGGARO_MCP_OAUTH=1`; jinak vydejte opaque bearer mandát lokálně:

```bash
YGGARO_DB_PASSPHRASE='…' /opt/yggaro/yggaro-server \
  -data /var/lib/yggaro -mcp-token admin@example.cz -mcp-scopes 'mcp.read'
```

Token se ukáže jen jednou. Uložte ho do úložiště tajemství AI klienta, nikdy do Gitu nebo chatu. Klient potřebuje MCP URL a `Authorization: Bearer <token>`. Začněte read-only a před nástroji si nechte vypsat capability.

Každý přístup se mapuje na místního uživatele a mandát. Výchozí mandát je read-only, platí 90 dní (maximum 365) a superadmin ho může okamžitě odvolat. RBAC aplikace platí dál. Po nastavení ověřte povolené čtení, odmítnutý zápis a skutečnou revokaci. Viz [oprávnění](mcp-permissions.cs.md).
