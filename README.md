# deskops

Workflow-domain instance built on top of `sldb`.

This repo owns the operational surfaces that should not live inside generic `sldb` infrastructure: `desk/`, deferred drawer work, workflow-native models, pills, rituals, atoms, and materializers.

Understanding `deskops` requires understanding `sldb` first: `sldb` owns structured Markdown infrastructure for querying, writing, and editing modeled documents, while `deskops` owns the workflow-domain instance built on top of it.

## Layout

- `desk/` - active and deferred workflow surfaces
- `docs/` - durable deskops-specific documentation
- `tests/` - workflow-domain tests

Durable guides currently include:

- `docs/how-to-report.md`
- `docs/how-to-test-ux-cli.md`

Repo-local agent guidance includes:

- `.skills/sldb/SKILL.md`

## SLDB Boundary

`sldb` owns reusable structured-document infrastructure:

- `StructuredNLDoc` model contracts
- reversible Markdown templates using `⸢rev•field⸥` markers
- structured document creation and updates
- field extraction from Markdown into model payloads
- field-level query, update, append, clean, create, and remove commands
- section ownership for fields
- store tracking, integrity hashes, recovery, and composition primitives

`deskops` owns workflow-domain surfaces:

- active tasks and boards
- rituals, routines, gates, hooks, and primitives
- transient pills and inbox notes
- durable atoms and materializers
- drawer triage for deferred work

Fields are already first-class in `sldb`. Do not create desk-local field documents just to make fields reusable, queryable, writable, or editable. Use `sldb docs`, `sldb fields`, `sldb sections`, `sldb ast`, and tracked document payloads for that.

Use `sldb` as the preferred write/edit path for modeled Markdown: `sldb docs create`, `sldb docs update`, `sldb fields update`, `sldb fields append`, `sldb fields clean`, and `sldb fields remove` should be preferred over ad hoc file edits whenever the document is tracked by a `StructuredNLDoc` model.

If that SLDB path does not work, capture the failure in the sibling `sldb` repo's inbox with the failing command, expected behavior, actual behavior, and relevant model/document references. Do not silently bypass SLDB or reimplement the missing field/document behavior inside `deskops` before the SLDB issue is recorded.

`spec/fields/` may define artifact schema vocabulary for the deskops compiler, but `desk/fields/` should not become a human-facing workflow surface or duplicate SLDB's field model.

Model changes should use SLDB's model workflow where possible:

- `sldb models add <model-ref> --store .sldb --pythonpath .`
- `sldb models template edit <ModelName> --input <template.md> --store .sldb --pythonpath .`
- `sldb models fields add <ModelName> <field> --type <type> --description <text> --store .sldb --pythonpath .`
- `sldb models fields remove <ModelName> <field> --store .sldb --pythonpath .`
- `sldb models validate <ModelName> --store .sldb --pythonpath .`
- `sldb models validate <ModelName> --promote --store .sldb --pythonpath .`

Use physical search for concrete names, paths, field paths, document names, and section titles:

```bash
sldb find title --in physical --store .sldb --pythonpath .
sldb find desk/atoms --in physical --store .sldb --pythonpath .
```

Use semantic search for model semantics, document tags, and meaning-oriented discovery:

```bash
sldb find topic:atoms --in semantic --store .sldb --pythonpath .
sldb find type.knowledge.atom --in semantic --store .sldb --pythonpath .
```

Use `--in both` when unsure, and `--global` when the local store should include linked/federated stores.

Maintain the semantic store with:

```bash
sldb stores check --store .sldb
sldb stores update --store .sldb --pythonpath .
```

## Spec2viz Boundary

`spec2viz` owns structured diagram generation in the same way `sldb` owns structured Markdown operations.

Use `spec2viz` when a diagram has or should have a structured YAML source. The YAML spec is the source of truth; Mermaid, PlantUML, SVG, or other rendered outputs are projections.

Use `spec2viz` for:

- validating structured diagram specs
- rendering human-facing diagrams from semantic YAML
- keeping diagrams aligned with their underlying architecture/process model
- avoiding hand-maintained duplicate Mermaid or PlantUML surfaces

Common commands:

```bash
spec2viz validate <diagram-spec.yaml>
spec2viz render <diagram-spec.yaml> --backend mermaid --out <output-dir>
spec2viz render <diagram-spec.yaml> --out <output-dir>
spec2viz schema --out spec2viz.schema.json
```

For `docs/diagrams/`, prefer this rule:

- structured YAML specs are editable source
- `.mmd`, PlantUML, SVG, or rendered diagram files are generated projections
- if a generated diagram is wrong, fix the YAML source or the renderer, not only the generated output
- if `spec2viz` cannot express or render the needed diagram, capture the gap in the sibling `spec2viz` repo's inbox before creating a deskops-specific workaround

The intended parallel is:

- `sldb`: structured data plus model contract -> Markdown document and field/query/edit surface
- `spec2viz`: structured diagram spec plus diagram contract -> rendered visual artifact

Both exist to reduce drift by making the structured source explicit and regenerating the human-facing projection from it.

## Install

Install `deskops` from this repo checkout:

```bash
pip install -e .[dev]
```

If `sldb` is not already available on the machine, `deskops` can bootstrap it from the sibling checkout at `../sldb`.

Recommended first-use flow:

```bash
deskops bootstrap
deskops init .
```

`deskops bootstrap` will:

- install or repair `sldb` from the sibling checkout when it is missing
- initialize the global store at `~/.sldb` when needed
- register the `deskops` models into that global store

`deskops init <path>` will:

- ensure the bootstrap prerequisites are ready
- create a local `.sldb/` store under the target repo when missing
- scaffold `desk/` when missing

## CLI

Run the installed entrypoint as `deskops`, or use the module form from this repo checkout.

```bash
deskops --help
python -m deskops --help
```

Current commands:

- `deskops about`
- `deskops bootstrap`
- `deskops init`
- `deskops faq`
- `deskops inbox`
- `deskops repo register`
- `deskops desk install`

## Testing

```bash
pytest
```
