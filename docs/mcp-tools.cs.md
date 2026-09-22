# MCP — seznam nástrojů a meze vydání 1.0.0

[English](mcp-tools.md) · [Připojení klienta](mcp.cs.md) · [Oprávnění](mcp-permissions.cs.md) · [Roadmapa](mcp-roadmap.cs.md)

Vydání 1.0.0 vystavuje **56 nástrojů**: 33 jen ke čtení a 23 zapisujících. Tenhle dokument je
úplný seznam a hlavně **poctivý výčet toho, co rozhraní neumí**. Mez, kterou zjistíte až po
nasazení, stojí víc než mez napsaná předem.

## Jak se rozsah omezuje

Tři nezávislé vrstvy, ne jedna:

1. **Oprávnění (scope).** Zápis vyžaduje `mcp.write`. Klient s pouze čtecím mandátem zapisující
   nástroje **vůbec neuvidí** — jsou skryté ve výpisu nástrojů, nejen odmítnuté při volání.
2. **Potvrzení u šesti akcí.** Viz „high-impact" níže: projdou jen s potvrzením u konkrétní akce
   (člověk v cyklu), nebo s předem schváleným rozsahem `mcp.write.high`.
3. **Třídy dat.** Mandát lze omezit na třídy *zakázka · dokument · adresář lidí · instance*.
   Nástroj mimo povolené třídy je odmítnutý i skrytý.

Navíc: rozsah přístupu je vždy dán právy **uživatele, pod jehož účtem je klient připojen** —
žádný zvláštní „AI účet" s vlastními právy neexistuje. Každé čtení zapisuje do bezpečnostního
logu doklad o výdeji dat (nástroj, třída, počet objektů, počet bajtů, otisk — obsah ne). Každý
zápis je v auditu změn s identifikátorem mandátu.

## Čtení (33)

**Zakázky a projekty:** `list_orders` · `get_order` · `get_project_health` · `get_portfolio_health` ·
`get_scope_status` · `get_agile_flow_health`
**Úkoly a práce:** `list_tasks` · `get_task` · `my_tasks` · `get_timesheet` · `get_my_attention` ·
`get_changes_since`
**Řízení:** `list_gates` · `list_milestones` · `list_risks` · `list_decisions` · `list_dependencies` ·
`list_journal_entries`
**Dokumenty a soubory:** `list_documents` · `get_document` · `list_files` · `get_file_content` ·
`list_templates` · `list_sharepoint_files` · `get_sharepoint_file_content` · `search_docs`
**Diskuse:** `list_threads` · `get_thread`
**Instance a lidé:** `instance_info` · `capabilities` · `list_users` · `list_roles` · `list_types`

## Zápis (23)

**Úkoly:** `create_task` · `update_task` · `set_task_progress` · `log_work` · `delete_task` ⚠
**Projekty a řízení:** `create_project` · `create_milestone` · `create_risk` · `update_risk` ·
`check_gate_item` ⚠
**Výstupy a rozhodnutí:** `create_deliverable` · `accept_deliverable` ⚠ · `propose_decision` ·
`decide_decision` ⚠
**Dokumenty:** `create_document` · `propose_document_version` · `record_meeting_outcome`
**Diskuse:** `create_thread` · `post_message` · `edit_message` · `delete_message` ⚠ ·
`toggle_reaction` · `resolve_thread` ⚠

⚠ = **high-impact** (6 akcí): mazání, blokující přechod brány, rozhodnutí a převzetí výstupu.
Vyžadují potvrzení u konkrétní akce, nebo předschválený rozsah `mcp.write.high`.

## Co vydání 1.0.0 NEUMÍ

- **Zakázku nelze přes MCP založit ani změnit.** Jsou jen `list_orders` a `get_order`; žádný
  `create_order`, žádný `update_order`. Pokud máte v plánu nechat asistenta zakládat zakázky,
  v tomhle vydání to nepůjde.
- **Projekt lze založit, ale ne vypsat ani upravit.** `create_project` existuje, `list_projects`
  ani `update_project` ne. Je to asymetrie a víme o ní.
- **Žádná AI uvnitř produktu.** Yggaro Lite sám nic nenavrhuje ani nevyhodnocuje. Model si
  připojujete vlastní, na vlastní účet a náklady.
- **Rozhraní vidí jednu instanci.** Napříč instancemi ani napříč organizacemi nic nespojuje.

Co s tím chystáme a v jakém pořadí, je v [roadmapě](mcp-roadmap.cs.md). Termíny tam nejsou
záměrně — slibovat datum, které neumíme doložit, je horší než mlčet.
