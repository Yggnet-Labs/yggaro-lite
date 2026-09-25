# MCP — tool list and the limits of the 1.0 releases

[English](mcp-tools.md) · [Čeština](mcp-tools.cs.md) · [Connecting a client](mcp.md) · [Permissions](mcp-permissions.md) · [Roadmap](mcp-roadmap.md)

The 1.0 releases expose **56 tools**: 33 read-only and 23 that write. This page is the complete
list and, more importantly, an honest account of **what the interface cannot do**. A limit you
discover after deployment costs more than a limit written down in advance.

In Yggaro Lite an **order and a project are the same thing** — one record that the interface and
the tool names refer to by both words.

## How access is narrowed

Three independent layers, not one:

1. **Scope.** Writing requires `mcp.write`. A client holding a read-only mandate **does not even
   see** the writing tools — they are hidden from the tool listing, not merely refused on call.
2. **Confirmation on six actions.** See "high-impact" below: they pass only with per-action
   confirmation (a human in the loop) or with the pre-approved `mcp.write.high` scope.
3. **Data classes.** A mandate can be restricted to *order · document · directory · instance ·
   product knowledge · discussion* (six classes). A tool outside the permitted classes is both
   refused and hidden. The headings below say which class each tool belongs to.

Beyond that, access always follows the permissions of **the user the client connects as** —
there is no separate "AI account" with rights of its own. Every successful call writes a
disclosure record to the security log (tool, class, object count, byte count, hash — never the
content). Every write lands in the change audit together with the mandate identifier.

## Read (33)

**Order** — orders and projects: `list_orders` · `get_order` · `get_project_health` ·
`get_portfolio_health` · `get_scope_status` · `get_agile_flow_health`; tasks and work: `list_tasks` ·
`get_task` · `my_tasks` · `get_timesheet` · `get_my_attention` · `get_changes_since`; governance:
`list_gates` · `list_milestones` · `list_risks` · `list_decisions` · `list_dependencies` ·
`list_journal_entries`
**Document:** `list_documents` · `get_document` · `list_files` · `get_file_content` ·
`list_sharepoint_files` · `get_sharepoint_file_content`
**Directory:** `list_users` · `list_roles`
**Instance:** `instance_info` · `capabilities` · `list_types` · `list_templates`
**Product knowledge:** `search_docs` (documentation shipped with the product, not your data)
**Discussion:** `list_threads` · `get_thread`

## Write (23)

**Order** — creating: `create_project`; tasks: `create_task` · `update_task` · `set_task_progress` ·
`log_work` · `delete_task` ⚠; governance: `create_milestone` · `create_risk` · `update_risk` ·
`check_gate_item` ⚠ · `record_meeting_outcome`; deliverables and decisions: `create_deliverable` ·
`accept_deliverable` ⚠ · `propose_decision` · `decide_decision` ⚠
**Document:** `create_document` · `propose_document_version`
**Discussion:** `create_thread` · `post_message` · `edit_message` · `delete_message` ⚠ ·
`toggle_reaction` · `resolve_thread` ⚠

⚠ = **high-impact** (6 actions): deletions, a blocking gate transition, decisions and accepting a
deliverable. They require per-action confirmation or the pre-approved `mcp.write.high` scope.

## What the 1.0 releases do NOT do

- **The core details of an existing order cannot be changed over MCP.** `create_project` creates a
  new order, and `list_orders` and `get_order` list and read it. Inside an order the assistant can
  work (tasks, gates, milestones, deliverables, risks, decisions, meeting notes). No tool changes
  the name, code, client, manager, sales owner, team or process, though; there is no `update_order`
  in this series.
- **A milestone cannot be edited after creation, and files cannot be uploaded.** `create_milestone`
  exists, editing a milestone does not; there is no file-upload tool.
- **No AI inside the product.** Yggaro Lite proposes and evaluates nothing on its own. You bring
  your own model, on your own account and at your own cost.
- **The interface sees one instance.** It joins nothing across instances or organisations.

What we intend to add, and in what order, is in the [roadmap](mcp-roadmap.md). It deliberately
carries no dates — promising a date we cannot stand behind is worse than saying nothing.
