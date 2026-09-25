# MCP — seznam nástrojů a meze vydání řady 1.0

[English](mcp-tools.md) · [Připojení klienta](mcp.cs.md) · [Oprávnění](mcp-permissions.cs.md) · [Roadmapa](mcp-roadmap.cs.md)

Vydání řady 1.0 vystavují **56 nástrojů**: 33 jen ke čtení a 23 zapisujících. Tenhle dokument je
úplný seznam a hlavně **poctivý výčet toho, co rozhraní neumí**. Mez, kterou zjistíte až po
nasazení, stojí víc než mez napsaná předem.

V Yggaro Lite jsou **zakázka a projekt totéž** — jeden záznam, který se v rozhraní i v názvech
nástrojů jmenuje oběma slovy.

## Jak se rozsah omezuje

Tři nezávislé vrstvy, ne jedna:

1. **Oprávnění (scope).** Zápis vyžaduje `mcp.write`. Klient s pouze čtecím mandátem zapisující
   nástroje **vůbec neuvidí** — jsou skryté ve výpisu nástrojů, nejen odmítnuté při volání.
2. **Potvrzení u šesti akcí.** Viz „high-impact" níže: projdou jen s potvrzením u konkrétní akce
   (člověk v cyklu), nebo s předem schváleným rozsahem `mcp.write.high`.
3. **Třídy dat.** Mandát lze omezit na třídy *zakázka · dokument · adresář lidí · instance ·
   znalosti o produktu · diskuse* (šest tříd). Nástroj mimo povolené třídy je odmítnutý i skrytý.
   Ke které třídě nástroj patří, říkají nadpisy níže.

Navíc: rozsah přístupu je vždy dán právy **uživatele, pod jehož účtem je klient připojen** —
žádný zvláštní „AI účet" s vlastními právy neexistuje. Po úspěšném volání nástroje (`tools/call`)
server zapíše do bezpečnostního logu doklad o výdeji dat (nástroj, třída, počet objektů, počet
bajtů, otisk — obsah ne). Neúspěšné volání zapíše záznam o odmítnutí; výpis nástrojů a další
protokolové zprávy záznam nevytvářejí. Zápis do logu výsledek volání neblokuje: když se nepodaří,
volání se nezastaví a chyba skončí jen v diagnostice serveru. Každý zápis dat je v auditu změn
s identifikátorem mandátu.

## Čtení (33)

**Zakázka** — zakázky a projekty: `list_orders` · `get_order` · `get_project_health` ·
`get_portfolio_health` · `get_scope_status` · `get_agile_flow_health`; úkoly a práce: `list_tasks` ·
`get_task` · `my_tasks` · `get_timesheet` · `get_my_attention` · `get_changes_since`; řízení:
`list_gates` · `list_milestones` · `list_risks` · `list_decisions` · `list_dependencies` ·
`list_journal_entries`
**Dokument:** `list_documents` · `get_document` · `list_files` · `get_file_content` ·
`list_sharepoint_files` · `get_sharepoint_file_content`
**Adresář lidí:** `list_users` · `list_roles`
**Instance:** `instance_info` · `capabilities` · `list_types` · `list_templates`
**Znalosti o produktu:** `search_docs` (dokumentace dodaná s produktem, ne vaše data)
**Diskuse:** `list_threads` · `get_thread`

## Zápis (23)

**Zakázka** — založení: `create_project`; úkoly: `create_task` · `update_task` · `set_task_progress` ·
`log_work` · `delete_task` ⚠; řízení: `create_milestone` · `create_risk` · `update_risk` ·
`check_gate_item` ⚠ · `record_meeting_outcome`; výstupy a rozhodnutí: `create_deliverable` ·
`accept_deliverable` ⚠ · `propose_decision` · `decide_decision` ⚠
**Dokument:** `create_document` · `propose_document_version`
**Diskuse:** `create_thread` · `post_message` · `edit_message` · `delete_message` ⚠ ·
`toggle_reaction` · `resolve_thread` ⚠

⚠ = **high-impact** (6 akcí): mazání, blokující přechod brány, rozhodnutí a převzetí výstupu.
Vyžadují potvrzení u konkrétní akce, nebo předschválený rozsah `mcp.write.high`.

## Co vydání řady 1.0 NEUMÍ

- **Základní údaje existující zakázky přes MCP nezměníte.** Novou zakázku založí
  `create_project` a vypíšete ji přes `list_orders` a `get_order`. Uvnitř zakázky asistent pracuje
  (úkoly, brány, milníky, výstupy, rizika, rozhodnutí, zápisy z porad). Název, kód, klienta,
  vedoucího, obchodníka, tým ani proces ale žádný nástroj nemění; `update_order` v téhle řadě není.
- **Milník po založení neupravíte a soubor nenahrajete.** `create_milestone` existuje, úprava
  milníku ne; nástroj pro nahrání souboru není.
- **Žádná AI uvnitř produktu.** Yggaro Lite sám nic nenavrhuje ani nevyhodnocuje. Model si
  připojujete vlastní, na vlastní účet a náklady.
- **Rozhraní vidí jednu instanci.** Napříč instancemi ani napříč organizacemi nic nespojuje.

Co s tím chystáme a v jakém pořadí, je v [roadmapě](mcp-roadmap.cs.md). Termíny tam nejsou
záměrně — slibovat datum, které neumíme doložit, je horší než mlčet.
