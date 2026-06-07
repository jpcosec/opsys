# UC-09: Self-reflection — "What does the system think about itself?"

After building the graph, the user runs a self-reflection routine. The system looks at its own knowledge graph and asks questions about coverage, gaps, and patterns.

**Interaction flow:**

1. `deskops graph build` → fresh snapshot
2. `deskops graph reflect` → system analyzes its own graph
3. Gets findings:
   - "Atom X has no incoming references — is it orphaned?"
   - "Topic Y has only one atom — may need expansion"
   - "These 3 atoms reference each other in a cycle — review for redundancy"
4. User reviews findings, takes action (archive atom, write new ones, break cycles)

**What this user is trying to do:**
Meta-cognition. The knowledge graph isn't just for querying — it can reflect on its own shape. This surfaces blind spots the human might not notice.

**When this breaks:**
- Findings are trivial or always the same → noise, ignored
- Never finds anything useful → user stops running it
- Findings are too abstract to act on
- Self-reflection itself is undocumented (how does it work? what questions does it ask?)
- Orphan detection flags atoms that are intentionally standalone
