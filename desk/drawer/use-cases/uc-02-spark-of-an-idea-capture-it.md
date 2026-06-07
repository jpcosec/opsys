# UC-02: Spark of an idea — capture it before it disappears

Working on something else, the user gets an idea. They need to dump it somewhere safe before returning to their flow.

**Interaction flow:**

1. `deskops inbox add "we should have a way to auto-tag atoms based on their content"` → saved
2. Later: `deskops inbox list` → sees the idea sitting there
3. `deskops inbox show 1` → reads the full note
4. Decides it has legs: routes it to the drawer or promotes it to a task

**What this user is trying to do:**
Low-friction capture. No file editing, no context switch. The inbox is their "pocket notebook" for the project.

**When this breaks:**
- `inbox add` requires too many flags or structured input
- The note gets saved but `inbox list` shows nothing
- No way to categorize or tag the note at capture time
- The note goes into a black hole — no way to find it later
