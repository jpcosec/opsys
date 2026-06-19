# Workflow Model Atoms

This diagram document is a human-facing materialization of these atoms:

- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-rendered-diagrams-are-projections.md`
- `desk/atoms/workflow-model/atom-spec2viz-mirrors-sldb-for-diagrams.md`

This diagram maps the first curated atoms for the deskops workflow model.

```mermaid
flowchart TB
    core["Why\ndivide and conquer through persisted operations"]
    atom_shape["What\natoms answer one raw question"]
    doc_refs["How\ndocuments point to atoms"]
    no_copy["How-not\npills reference, do not copy"]
    transient["What\npills are transient context"]
    phases["Where\ntask phases live inside board"]
    ambiguity["When\nsubagent returns ambiguous task"]
    auto["How\nautomatic routines differ from LLM tasks"]
    diagrams["What\ndiagrams generate operational models"]
    surfaces["How\ncodebase surfaces generate atom candidates"]

    core --> atom_shape
    atom_shape --> doc_refs
    doc_refs --> no_copy
    no_copy --> transient
    core --> phases
    phases --> ambiguity
    ambiguity --> auto
    diagrams --> surfaces
    surfaces --> atom_shape
    diagrams --> phases
    diagrams --> auto
```

## Atom Files

- `desk/atoms/workflow-model/atom-divide-and-conquer-persisted-operations.md`
- `desk/atoms/workflow-model/atom-atoms-answer-one-question.md`
- `desk/atoms/workflow-model/atom-documents-point-to-atoms.md`
- `desk/atoms/workflow-model/atom-pills-reference-not-copy.md`
- `desk/atoms/workflow-model/atom-pills-are-transient.md`
- `desk/atoms/workflow-model/atom-task-board-phases.md`
- `desk/atoms/workflow-model/atom-clean-subagent-ambiguity-review.md`
- `desk/atoms/workflow-model/atom-automatic-routines-vs-llm-tasks.md`
- `desk/atoms/workflow-model/atom-diagrams-generate-operational-models.md`
- `desk/atoms/workflow-model/atom-codebase-surfaces-generate-atom-candidates.md`

## Questions Raised

- How should large documents declare their sldb composition from atoms?
- Is `5WH1+` the final field name for the single question answered by each atom?
- Which codebase relations are strong enough to become curated atoms now?
