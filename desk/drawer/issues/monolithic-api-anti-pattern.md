---
title: Monolithic API Anti-Pattern in SLDB UI
date: 2026-08-13
status: open
---

# Issue: Monolithic API Anti-Pattern in SLDB UI

This document records the critical errors and architectural anti-patterns committed during the initial implementation of the SLDB UI MVP (sldb-viewer), so we know exactly what **not to do**.

## Critical Mistakes Made

1. **Coupling Independent Surfaces (API Monolith):**
   Instead of treating the AST and StructuredDocModel as truly independent, decoupled UI surfaces, they were bundled together with the raw Markdown into a single monolithic API endpoint (`/api/file.json.js`). This directly violates the SLDB principle of decoupling AST parsing from field instances.
   **What to do instead:** Expose independent API routes (e.g., `/api/ast`, `/api/model`, `/api/markdown`) to preserve the architectural boundaries.

2. **Using the Wrong Backend Commands:**
   Used the heavy, composite command `sldb docs show` to fetch all data at once.
   **What to do instead:** Use atomic, specific commands for each surface: `sldb ast show` for the graph and `sldb fields` or `sldb extract` for the model payload.

3. **Silent Data Destruction (Frontmatter Bug):**
   Hardcoded an empty object (`frontmatter: {}`) when saving Markdown changes via `gray-matter`. This blindly erased any existing frontmatter on the document, destroying valuable metadata.
   **What to do instead:** Ensure the UI correctly preserves or selectively updates the frontmatter object without wiping it.

4. **Faking Implementation (Placeholders):**
   Left a "Coming soon..." UI placeholder for the `spec2viz` Render surface, violating the directive to only present fully implemented, working features.
   **What to do instead:** Implement the Specyaml -> Mermaid pipeline explicitly, or do not include the surface in the UI at all. Do not lie about future implementations.

5. **Misrepresenting the SLDB Store:**
   Treated a legacy Node.js filesystem scanner (`api/tree.js`) as if it was the SLDB "Store". The Store in SLDB is a tracked database/registry (`.sldb/`), not a raw `fs.readdir` output.
   **What to do instead:** The Store UI surface must query the SLDB engine (e.g., via `sldb find` or `sldb models list`) to show only actively tracked documents and their indexing states, ignoring untracked physical files.
