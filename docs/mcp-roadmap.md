# MCP roadmap

[English](mcp-roadmap.md) · [Čeština](mcp-roadmap.cs.md) · [Tools and limits](mcp-tools.md)

**No dates, deliberately.** Promising a date we cannot stand behind is worse than saying nothing.
The order, however, we can state — and we hold to it.

## Today — the 1.0 series

56 tools (33 read, 23 write), built-in OAuth, mandates with a default expiry and immediate revocation,
restriction to data classes, confirmation on six high-impact actions, a disclosure record in the
security log. The complete list and the limits are in [tools and limits](mcp-tools.md).

## The next batch after release

One batch, not a drip. It contains two things:

**1 · Fuller writing for orders.** Today's largest gap: the assistant can create a new order and
work with the parts of an existing one (gates, milestones, risks, deliverables, meeting notes), but
cannot change the order's own details, such as its name, client or manager. We intend to add changing an order's core details, updating a milestone, uploading a
file and approving a document version.

**2 · A guide for the connected AI.** So that an assistant can walk a new administrator through
setup — how to create a gate, how to turn it into a template, how to set permissions — instead of
the person hunting through documentation. The mechanism already exists (`search_docs` over the
documentation embedded in the binary); what is missing is the guide's content and writing for
gates and templates.

## How MCP differs from the forthcoming Yggaro Lite AI

This gets confused, so we say it plainly. **MCP is not "Yggaro Lite AI".**

- **Yggaro Lite (today, the 1.0 series)** — the product exposes an MCP endpoint. **You** connect the
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
