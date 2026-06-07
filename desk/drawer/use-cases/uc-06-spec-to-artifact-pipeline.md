# UC-06: Spec to artifact — "I need a thing generated"

The user wants deskops to generate something from a spec. A document, a diagram, a model — they define the spec and expect an artifact.

**Interaction flow:**

1. Define a spec file in `desk/specs/` describing what they want
2. Run `deskops spec build my-spec-id`
3. Deskops compiles the spec, materializes the artifact
4. Output lands somewhere predictable (e.g., `docs/` or `desk/materializations/`)
5. User reviews the artifact, iterates on the spec, re-runs

**What this user is trying to do:**
Treat specs as source of truth. Change the spec, regenerate, get the updated artifact. No manual editing of generated output.

**When this breaks:**
- Spec format is too rigid or too loose — either annoying or useless
- Output location is a mystery
- Re-running doesn't overwrite cleanly (leftover garbage)
- Artifact is wrong but there's no diff to show what changed
- Only available through CLI when user wants editor integration
