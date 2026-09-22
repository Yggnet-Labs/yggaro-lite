# MCP — tool list and the limits of release 1.0.0

[English](mcp-tools.md) · [Čeština](mcp-tools.cs.md) · [Connecting a client](mcp.md) · [Permissions](mcp-permissions.md) · [Roadmap](mcp-roadmap.md)

Release 1.0.0 exposes **56 tools**: 33 read-only and 23 that write. This page is the complete
list and, more importantly, an honest account of **what the interface cannot do**. A limit you
discover after deployment costs more than a limit written down in advance.

## How access is narrowed

Three independent layers, not one:

1. **Scope.** Writing requires `mcp.write`. A client holding a read-only mandate **does not even
   see** the writing tools — they are hidden from the tool listing, not merely refused on call.
2. **Confirmation on six actions.** See "high-impact" below: they pass only with per-action
   confirmation (a human in the loop) or with the pre-approved `mcp.write.high` scope.
3. **Data classes.** A mandate can be restricted to *order · document · directory · instance*.
   A tool outside the permitted classes is both refused and hidden.

Beyond that, access always follows the permissions of **the user the client connects as** —
there is no separate "AI account" with rights of its own. Every read writes a disclosure record
to the security log (tool, class, object count, byte count, hash — never the content). Every
write lands in the change audit together with the mandate identifier.

## Read (33)

**Orders and projects:** `list_orders` · `get_order` · `get_project_health` · `get_portfolio_health` ·
`get_scope_status` · `get_agile_flow_health`
**Tasks and work:** `list_tasks` · `get_task` · `my_tasks` · `get_timesheet` · `get_my_attention` ·
`get_changes_since`
**Governance:** `list_gates` · `list_milestones` · `list_risks` · `list_decisions` ·
`list_dependencies` · `list_journal_entries`
**Documents and files:** `list_documents` · `get_document` · `list_files` · `get_file_content` ·
`list_templates` · `list_sharepoint_files` · `get_sharepoint_file_content` · `search_docs`
**Discussion:** `list_threads` · `get_thread`
**Instance and people:** `instance_info` · `capabilities` · `list_users` · `list_roles` · `list_types`

## Write (23)

**Tasks:** `create_task` · `update_task` · `set_task_progress` · `log_work` · `delete_task` ⚠
**Projects and governance:** `create_project` · `create_milestone` · `create_risk` · `update_risk` ·
`check_gate_item` ⚠
**Deliverables and decisions:** `create_deliverable` · `accept_deliverable` ⚠ · `propose_decision` ·
`decide_decision` ⚠
**Documents:** `create_document` · `propose_document_version` · `record_meeting_outcome`
**Discussion:** `create_thread` · `post_message` · `edit_message` · `delete_message` ⚠ ·
`toggle_reaction` · `resolve_thread` ⚠

⚠ = **high-impact** (6 actions): deletions, a blocking gate transition, decisions and accepting a
deliverable. They require per-action confirmation or the pre-approved `mcp.write.high` scope.

## What release 1.0.0 does NOT do

- **An order cannot be created or changed over MCP.** Only `list_orders` and `get_order` exist;
  there is no `create_order` and no `update_order`. If your plan is to let an assistant open
  orders, this release will not do it.
- **A project can be created but neither listed nor updated.** `create_project` exists;
  `list_projects` and `update_project` do not. It is an asymmetry and we know about it.
- **No AI inside the product.** Yggaro Lite proposes and evaluates nothing on its own. You bring
  your own model, on your own account and at your own cost.
- **The interface sees one instance.** It joins nothing across instances or organisations.

What we intend to add, and in what order, is in the [roadmap](mcp-roadmap.md). It deliberately
carries no dates — promising a date we cannot stand behind is worse than saying nothing.
