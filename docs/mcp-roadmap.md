# MCP roadmap

[English](mcp-roadmap.md) · [Čeština](mcp-roadmap.cs.md) · [Tools and limits](mcp-tools.md)

**No dates, deliberately.** Promising a date we cannot stand behind is worse than saying nothing.
The order, however, we can state — and we hold to it.

## Today — release 1.0.0

56 tools (33 read, 23 write), built-in OAuth, mandates with an expiry and immediate revocation,
restriction to data classes, confirmation on six high-impact actions, a disclosure record in the
security log. The complete list and the limits are in [tools and limits](mcp-tools.md).

## The next batch after release

One batch, not a drip. It contains two things:

**1 · Writing for orders and projects.** Today's largest gap: a product for running client work
exposes the order itself as read-only over MCP. We intend to add creating and changing an order,
listing and updating a project, updating a milestone, uploading a file, closing a risk, rejecting
a delivery and approving a document version.

**2 · A guide for the connected AI.** So that an assistant can walk a new administrator through
setup — how to create a gate, how to turn it into a template, how to set permissions — instead of
the person hunting through documentation. The mechanism already exists (`search_docs` over the
documentation embedded in the binary); what is missing is the guide's content and writing for
gates and templates.

## How MCP differs from the forthcoming Yggaro Lite AI

This gets confused, so we say it plainly. **MCP is not "Yggaro Lite AI".**

- **Yggaro Lite (today, 1.0.0)** — the product exposes an MCP endpoint. **You** connect the
  AI, it is **yours**, it runs on your account and at your cost. No model lives inside the
  product.
- **Yggaro Lite AI (forthcoming)** — **the same product**, with agents working **inside** it:
  automating routine, evaluating, proposing. MCP remains available, so you will be able to
  have both — your own client and the internal agents.

It is not a different product but a higher tier of the same one. We promise no date.

## Not coming in 1.x

- **The Mesh edition** — one application on a computer, no server. A different edition,
  deferred, no date.

## What always holds

Every new tool follows the permissions of **the user the client connects as**. Instance
administration stays reserved to the superadministrator and is not opened over MCP. This is not
a recommendation; it is enforced in code — a tool cannot come into being unclassified as read or
write.
