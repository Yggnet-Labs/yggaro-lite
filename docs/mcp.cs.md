# Připojení AI klienta přes MCP

[English](mcp.md) · [Čeština](mcp.cs.md) · [Seznam nástrojů a meze](mcp-tools.cs.md) · [Oprávnění](mcp-permissions.cs.md)

MCP dovolí vlastnímu AI klientovi zákazníka pracovat s Yggaro Lite. Není to „AI uvnitř Yggaro Lite“: žádný model není součástí produktu a server sám data modelu neposílá.

**Je to zcela volitelné a ve výchozím stavu vypnuté.** Yggaro Lite funguje naplno i bez jakékoli AI: nic z toho, co je tady popsané, není k provozu produktu potřeba a tím, že MCP nezapnete, nepřijdete o žádnou jinou funkci. Zůstane vypnuté, dokud ho správce výslovně nezapne.

## Zapnutí endpointu

Přidejte `YGGARO_MCP=1` do prostředí služby a restartujte ji. Streamable HTTP endpoint je `https://vase-domena.cz/mcp`. Vestavěné OAuth je volitelné přes `YGGARO_MCP_OAUTH=1`; jinak vydejte opaque bearer mandát lokálně:

```bash
yggaro-admin -mcp-token admin@example.cz -mcp-scopes 'mcp.read'
```

`yggaro-admin` spustí příkaz pod účtem služby ([instalace, krok 6](install.cs.md#6-údržbové-příkazy-pod-účtem-služby)). Token se ukáže jen jednou. Uložte ho do úložiště tajemství AI klienta, nikdy do Gitu nebo chatu. Klient potřebuje MCP URL a `Authorization: Bearer <token>`. Začněte read-only a před nástroji si nechte vypsat capability.

Každý přístup se mapuje na místního uživatele a mandát. Mandát s tokenem je ve výchozím stavu jen pro čtení a platí 90 dní (maximum 365); mandát navázaný na přihlašovací identitu (OIDC) v řadě 1.0 nevyprší a je potřeba ho odvolat výslovně. Superadmin může kterýkoli mandát okamžitě odvolat. RBAC aplikace platí dál. Po nastavení ověřte povolené čtení, odmítnutý zápis a skutečnou revokaci. Viz [oprávnění](mcp-permissions.cs.md).

## Známé omezení 1.0.5: odvolání přístupu připojeného AI klienta (OAuth)

*Doplněno 17. 10. 2026, po vydání 1.0.5. Kód ani vydané soubory verze 1.0.5 se nemění.*

**Co se může stát.** V přehledu „Aktivní přístupy“ lze odvolat přístup AI klienta, který se připojil přes OAuth (řádek „OAuth tokenová rodina“). Odvolání této položky **může selhat**, když u rodiny už nezůstal žádný záznam přístupového tokenu. Přístupové tokeny platí 15 minut a systém vypršelé záznamy průběžně uklízí, takže do tohoto stavu se dostane hlavně klient, který delší dobu jen drží dlouhodobý obnovovací token. Při selhání se u řádku zobrazí „×“ a hlášení „Část odvolání selhala“. Přístup klienta tím odvolán **není** a klient ho může dál obnovovat.

**Jak to obejít.** Odvolejte celý mandát (oprávnění) tohoto klienta. Dělá to jen superadministrátor:
1. Přihlaste se jako superadministrátor.
2. V levém menu otevřete **Administrace**.
3. Vyberte záložku **Nastavení**.
4. V panelu **MCP mandáty** najděte řádek mandátu klienta (sloupce Principál, Oprávnění, Třídy dat, Platnost do, Stav, Poznámka).
5. Klikněte na **Odvolat** a potvrďte „Opravdu odvolat tenhle mandát? Klient přestane fungovat okamžitě.“

Mandát lze odvolat i v **Administrace → Práva → Aktivní přístupy**: zaškrtněte řádek typu „MCP mandát“, klikněte na **Odvolat vybrané** a zadejte své aktuální heslo. Filtr **„Jen účty bez lokálního TOTP“** je ve výchozím stavu zaškrtnutý a skrývá uživatele s lokálním TOTP. Pokud řádek mandátu nevidíte, zaškrtnutí zrušte.

**Na co dát pozor.** Řádek OAuth rodiny a řádek mandátu spolu rozhraní verze 1.0.5 nespáruje (u rodiny se identifikátor mandátu nezobrazuje); poznáte je podle uživatele, oprávnění a poznámky. Má-li uživatel více mandátů a nepoznáte, který patří danému klientu, odvolejte všechny jeho mandáty a ostatní klienty připojte znovu.

**Co po odvolání mandátu platí.** Klient už nemůže obnovit přístup a požadavky s dosud platným přístupovým tokenem jsou odmítnuty. Ověřeno testem nad zdrojem verze 1.0.5 (obnovení po odvolání mandátu nelze provést, položka zmizí z přehledu) a čtením kódu ověření přístupového tokenu; neověřeno na běžící instanci.

**Oprava:** plánována pro verzi 1.0.6.
