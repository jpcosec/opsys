# UC-08: Closeout — "Did we cover everything?"

A task or phase is done. Before calling it complete, the user runs a closeout ritual to validate that all knowledge surfaces are covered.

**Interaction flow:**

1. Run `deskops closeout` — or some named ritual
2. System checks:
   - Are all atoms still consistent with each other?
   - Are materializations up to date?
   - Is the graph coherent?
   - Are there drift items that need attention?
3. Gets a pass/fail with details
4. If pass: marks the phase as truly done
5. If fail: gets a list of what to fix before closing

**What this user is trying to do:**
Closeout is a quality gate. They want confidence that finishing a piece of work doesn't silently leave the knowledge base in a broken state.

**When this breaks:**
- Closeout passes but the desk is actually broken (false confidence)
- Closeout fails with vague reasons ("something is wrong") — can't act on it
- Takes too long or requires too much setup
- No incremental closeout — can only check at the end, not along the way
- Bypassing closeout is too easy (rubber stamp)
