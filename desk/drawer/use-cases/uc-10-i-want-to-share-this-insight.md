# UC-10: "I want to share this insight"

The user has been working with the desk and wants to communicate what they've learned to someone who doesn't use deskops — a teammate, a reviewer, their future self.

**Interaction flow:**

1. Build understanding in the desk (atoms, graph, materializations)
2. `deskops materialize` → generates human-friendly documents from atoms
3. Output goes to `docs/` — readable in a browser, in markdown, on GitHub
4. User shares a link: "read the materialization at docs/architecture-overview.md"
5. Reader doesn't need deskops installed — just reads the rendered docs

**What this user is trying to do:**
Bridge the gap between desk-internal knowledge and external communication. The desk is for working; materializations are for sharing.

**When this breaks:**
- Materialized docs are just atoms with different formatting — not actually more readable
- Output doesn't include diagrams or cross-references
- Materialization is one-way: reader can't easily feed back into the desk
- Stale materializations with no "last built" date → reader doesn't know if it's current
- Too many steps to produce a simple shareable output
