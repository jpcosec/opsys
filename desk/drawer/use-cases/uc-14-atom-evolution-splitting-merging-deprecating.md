# UC-14: Atom evolution — splitting, merging, deleting

Knowledge evolves. An atom becomes too broad. Two atoms overlap. An idea is obsolete. The user needs to refactor the atom graph.

**Interaction flow:**

1. `deskops atoms split atom-big-idea --into new-atom-a --into new-atom-b` → splits content, preserves cross-references
2. `deskops atoms merge atom-alpha atom-beta --into atom-gamma` → merges two atoms
3. `deskops atoms delete atom-old-idea` → removes the obsolete atom
4. `deskops graph build && deskops graph missing` → validates the refactored graph

**What this user is trying to do:**
Refactor the knowledge model like code. Atoms aren't static — they evolve. The tool should support that lifecycle without manual file surgery.

**When this breaks:**
- Split/merge loses tag metadata
- Deprecated atoms still show as active by default
- Cross-references break silently during split/merge
- No dry-run mode — can't preview what will happen
- Git history becomes incomprehensible (mass rename detected as delete+create)
- Can't undo a split/merge without manual recovery
