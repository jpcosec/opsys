# UC-04: "I think the graph is missing something"

The user has been adding atoms. They run `deskops graph build` and then `deskops graph missing` to see if the graph is coherent.

**Interaction flow:**

1. Add a new atom file manually in `desk/atoms/`
2. `deskops graph build` → rebuilds the snapshot
3. `deskops graph missing` → finds references to things that don't exist as nodes
4. User sees a missing reference report:
   - `broken_link: atom-my-new-idea -> atom-something-that-doesnt-exist`
   - provenance points to the exact line in the broken atom
5. User fixes the broken reference or creates the missing atom
6. Re-runs `graph missing` → clean

**What this user is trying to do:**
Quality check. They want the knowledge model to be internally consistent. The `graph missing` command is a linter for their atom relationships.

**When this breaks:**
- `graph missing` doesn't catch obvious broken links
- Provenance points to the wrong file or line
- False positives — flags things that are actually fine
- Output is too noisy (hundreds of "missing" things that aren't real problems)
- The check is slow enough that the user stops running it
