---
name: use-spec2viz
description: Use when working with spec2viz diagrams, Mermaid outputs, diagram specs, or generated diagram projections from specs/atoms/docs.
---

# Use Spec2viz

Spec2viz owns structured diagram rendering and diagram projections.

Use spec2viz when the task involves:

- Generating diagrams from specs or structured inputs.
- Mermaid `.mmd` outputs.
- Diagram documentation under `docs/diagrams/`.
- Keeping generated diagrams synchronized with source specs or atoms.

Boundary:

- Source knowledge belongs in atoms, specs, docs, or code.
- Diagram outputs are projections, not canonical knowledge.
- SLDB owns document structure.
- KGDB owns graph snapshots.
- Deskops may orchestrate workflow, but spec2viz should render diagrams.

Deskops conventions:

- Store diagram docs under `docs/diagrams/`.
- Declare diagram sources in a `## Diagram Sources` section when useful.
- Keep rendered diagram files reproducible from source specs.
- If a diagram changes because an atom/spec changed, update both the source reference and generated projection.

Validation:

```bash
deskops graph build --root .
deskops graph missing --root .
pytest
```

Do not encode durable knowledge only in a diagram. Distill it into atoms/specs first.
