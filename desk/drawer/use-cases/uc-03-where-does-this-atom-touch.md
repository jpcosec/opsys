# UC-03: "Where does this atom touch?"

A user reads an atom about materialization contracts and wonders: what else references this? What depends on it? What would break if I changed it?

**Interaction flow:**

1. `deskops graph neighbors atom-materialization-contracts-bind-source-output-validation`
2. Sees outgoing links: what this atom references
3. Sees incoming links: what references this atom
4. Sees the role labels: *why* things connect (not just *that* they connect)
5. Follows a connection: `deskops atoms show atom-specs-formalize-atoms-as-contracts`

**What this user is trying to do:**
Trace dependencies. Before editing an atom, they want to know the blast radius. The graph is their navigation tool for the knowledge model.

**When this breaks:**
- Graph hasn't been built or is stale → silent
- Neighbors shows nodes they can't actually open or find
- Roles are too vague ("related to") to be useful
- Missing links that should exist (graph missed edges during extraction)
- Circular path — neighbors just bounce between the same 3 atoms
