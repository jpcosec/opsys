# Desk Source Graph Vocabulary

ID: desk-source-graph-vocabulary

## Purpose

This document defines the first controlled vocabulary for connecting desk artifacts to source files in a KGDB-backed property graph. The vocabulary is intentionally small: it names node kinds, edge role families, relation direction rules, and confidence/provenance fields before any extractor, fixture, CLI command, or graph runtime exists.

## Boundary

SLDB remains the source of truth for modeled Markdown, semantic tags, document sections, and document payloads. Deskops may derive graph facts from those SLDB-owned surfaces, but it must not reimplement SLDB parsing or semantic tag derivation.

KGDB owns graph persistence, snapshots, and traversal. Deskops owns workflow-specific graph vocabulary and relation extraction rules. The graph is a property graph contract first; OWL or ontology mappings are deferred until the property graph is useful.

## Node Kinds

Node kinds are lower-case strings stored as `kind`. The first vocabulary uses file-level source nodes only; symbol-level nodes are out of scope until file-level extraction is validated.

| Kind | Meaning | Stable identity source |
|---|---|---|
| `atom` | Curated one-question knowledge atom under `desk/atoms/`. | Atom `ID` field. |
| `task` | Active routed work item under `desk/tasks/`. | Task `ID` field. |
| `issue` | Deferred or inbox/drawer work item under `desk/drawer/issues/` or owning repo inbox/drawer. | Issue title slug or explicit `ID` when present. |
| `doc` | Durable human-facing Markdown document that is not a spec, diagram, task, issue, atom, or ritual. | Repository-relative path. |
| `diagram` | Rendered or source diagram document, including Mermaid-backed diagram docs. | Repository-relative path. |
| `spec` | Contract/specification artifact under `spec/` or docs that explicitly define expected structure or behavior. | Repository-relative path plus spec id when present. |
| `primitive` | Operational primitive or runtime behavior unit exposed by deskops. | Repository-relative path plus primitive name when available. |
| `sldb_model` | SLDB model or document schema used as graph input. | Model name or repository-relative `.sldb` path. |
| `cli_command` | User-facing deskops command surface. | Command token path, for example `deskops atoms check-tags`. |
| `source_file` | Implementation source file that is not primarily a test or config file. | Repository-relative path. |
| `test_file` | Test source file. | Repository-relative path. |
| `config_file` | Configuration, registry, or policy file that changes behavior without being executable source. | Repository-relative path. |

## Node Identifiers

Every graph node id uses the format `<kind>:<identity>`, where `<kind>` is one node kind from this vocabulary and `<identity>` is the smallest stable identifier available for that kind. Identifiers are deterministic, project-local, and stored as plain strings.

Use explicit document ids when the modeled artifact owns one. Use project-root-relative POSIX paths for file-backed nodes whose identity is the file itself. Do not include absolute paths, working-directory prefixes such as `./`, generated line numbers, content hashes, or symbol locators in file-level ids.

Path identities are normalized before prefixing:

- Use `/` as the separator.
- Keep the path relative to the project root.
- Preserve filename case as stored in git.
- Remove redundant `.` path segments.
- Do not add a trailing slash.

Identifier stability follows the identity source. Nodes backed by explicit ids remain stable across file moves as long as the explicit id remains unchanged. Path-backed nodes intentionally change id when the project-root-relative path changes; a future graph migration or equivalence edge may record continuity, but this vocabulary does not create aliases. Command-token ids change when the user-facing command path changes. Primitive ids change when the primitive's declared name changes, or when a path-only primitive moves and has no declared name.

| Kind | Identifier format | Example |
|---|---|---|
| `atom` | `atom:<atom-id>` from the atom `ID` field. | `atom:atom-documents-point-to-atoms` |
| `task` | `task:<task-id>` from the task `ID` field. | `task:task-002-define-graph-node-identifiers` |
| `issue` | `issue:<issue-id-or-title-slug>` from explicit `ID` when present, otherwise the issue title/file slug. | `issue:issue-integrate-kgdb-for-desk-source-knowledge-graph` |
| `doc` | `doc:<project-relative-path>` for durable Markdown docs that are not a more specific kind. | `doc:docs/knowledge-graph/desk-source-graph-vocabulary.md` |
| `diagram` | `diagram:<project-relative-path>` for diagram source or rendered diagram docs. | `diagram:docs/diagrams/codebase/codebase-knowledge-surfaces.mmd` |
| `spec` | `spec:<project-relative-path>` plus `#<spec-id>` only when the file carries multiple explicit specs. | `spec:spec/artifacts/atom.yaml` |
| `primitive` | `primitive:<project-relative-path>#<primitive-name>` when the primitive has a declared name; otherwise `primitive:<project-relative-path>`. | `primitive:deskops/runtime/primitives.py#materialize_atom` |
| `sldb_model` | `sldb_model:<model-name>` for declared SLDB models; use `sldb_model:<project-relative-path>` only when no model name exists. | `sldb_model:AtomDoc` |
| `cli_command` | `cli_command:<space-separated-command-token-path>` using the user-facing command path. | `cli_command:deskops atoms check-tags` |
| `source_file` | `source_file:<project-relative-path>` for implementation source files that are not primarily tests or config. | `source_file:deskops/operations.py` |
| `test_file` | `test_file:<project-relative-path>` for test source files. | `test_file:tests/test_atom_materialization.py` |
| `config_file` | `config_file:<project-relative-path>` for configuration, registry, or policy files. | `config_file:desk/atoms/tag-namespaces.yaml` |

Symbol-level ids are out of scope. The `#<primitive-name>` suffix is allowed only for named operational primitives because `primitive` is already a node kind in this vocabulary; it does not authorize general function, class, method, or variable nodes.

## Edge Roles

The graph reuses the existing document-to-atom role vocabulary where the meaning overlaps. It does not create a competing atom relation model: atoms do not own outgoing relations, and larger surfaces point to atoms or to implementation surfaces.

An edge role is the controlled value stored in the edge `role` property. The role names below are the first allowed vocabulary for deskops graph extraction; later tasks may append roles, but they must not invert these directions or redefine the atom-reference roles tracked by `issue-formalize-atom-reference-role-vocabulary`.

### Direction Rule

Every edge points from the artifact carrying the relation evidence to the artifact being referenced, realized, validated, invoked, routed, or configured. The source node answers "where did this relation claim come from?" and the target node answers "what surface does that claim concern?"

Do not emit duplicate inverse edges for convenience. KGDB traversal should answer reverse questions such as "what implements this atom?" by traversing incoming `implements` edges. A reverse-looking role is allowed only when it has distinct evidence and distinct meaning, such as `source_for` from a source artifact to a generated projection instead of `generated_from` from the generated projection to the source artifact.

### Role Catalog

| Role | Family | Canonical direction | Example source kind | Example target kind | Declared evidence | Inferred evidence | First extractor |
|---|---|---|---|---|---|---|---|
| `references` | Knowledge use | Referencing surface -> referenced surface. | `doc` | `atom` | Explicit atom reference metadata, Markdown link, or semantic reference field. | Content scan that recognizes an atom id or stable node id. | yes |
| `documents` | Knowledge use | Explanatory surface -> atom or documented surface. | `doc` | `atom` | Explicit atom reference role, documentation frontmatter, or curated relation map. | Heading/link context that clearly describes the target. | yes |
| `specifies` | Knowledge use | Specifying surface -> specified surface. | `spec` | `cli_command` | Spec section, model declaration, or task output that names the target. | Path or title similarity between a spec and target surface. | yes |
| `constrains` | Knowledge use | Constraint source -> constrained surface. | `doc` | `task` | Ritual, policy, pill, or task dependency that explicitly limits behavior. | Content scan that finds imperative policy language naming a target. | yes |
| `supports` | Knowledge use | Supporting evidence/context -> supported claim or surface. | `doc` | `atom` | Explicit related-atom, evidence, or rationale reference. | Nearby reference text that appears to justify a target. | no |
| `uses` | Knowledge use | Dependent surface -> dependency surface. | `source_file` | `sldb_model` | Import, config declaration, or documented dependency. | Static content scan for model or command names. | no |
| `materializes` | Materialization | Concrete artifact -> abstract atom/spec/task it materializes. | `doc` | `atom` | Materializer output metadata or explicit generated artifact declaration. | Path convention tying a generated artifact to a source atom. | no |
| `implements` | Materialization | Implementation surface -> atom/spec/task/behavior it implements. | `source_file` | `spec` | Explicit code comment, command registry entry, task output, or spec implementation mapping. | Filename or import similarity; filename similarity alone is always low confidence. | no |
| `renders` | Materialization | Rendered projection -> semantic surface it presents. | `diagram` | `doc` | Render metadata, diagram source reference, or projection declaration. | Matching `.md` and `.mmd` path pairs. | no |
| `generated_from` | Materialization | Generated artifact -> generator or source artifact. | `diagram` | `source_file` | Generated-file metadata, materializer output, or build manifest. | Path convention or generated filename pattern. | no |
| `source_for` | Materialization | Source artifact -> generated or derived artifact. | `source_file` | `diagram` | Source manifest, generator registry, or explicit projection declaration. | Paired source/output path convention. | no |
| `validates` | Validation | Validation evidence -> claim, atom, task, source file, or behavior it validates. | `test_file` | `atom` | Test marker, explicit validation metadata, or task validation list. | Test name or assertion text that names the target. | yes |
| `tests` | Validation | Test file -> source file, command, or behavior under test. | `test_file` | `source_file` | Test import, fixture target, or explicit test metadata. | Test filename matching source filename. | no |
| `violates` | Validation | Conflicting artifact -> claim, atom, spec, or policy it violates. | `issue` | `spec` | Explicit issue, finding, diagnostic, or check result naming the violated target. | Content scan that detects likely conflict language. | no |
| `invokes` | Operation | Caller, task, doc, or command -> command or primitive it invokes. | `task` | `cli_command` | Task instruction, CLI registry, script call, or command documentation. | Content scan for command-shaped text. | yes |
| `defines` | Operation | Defining artifact -> model, primitive, command, schema, tag namespace, or vocabulary item it defines. | `config_file` | `sldb_model` | Schema file, registry, model file, or vocabulary document. | Path convention under a known definition directory. | yes |
| `routes` | Operation | Board/index/workflow surface -> task or issue it routes. | `doc` | `task` | Board row, index entry, or routing metadata. | Path convention inside an active task directory. | yes |
| `configures` | Operation | Config file or setting surface -> runtime/source/command surface it configures. | `config_file` | `cli_command` | Config key, registry entry, or documented setting target. | Content scan that associates a setting with a target name. | no |

### Declared And Inferred Roles

Declared roles come from explicit source-owned metadata or authored text that names both the relation and the target. Examples include an atom reference with `role: documents`, a board row routing a task, a task validation section naming tests, or a config/model file defining a schema. Declared edges should use `source_kind` values such as `declared`, `sldb_semantic`, or `manual`, and may be `high` confidence when the target id is stable and unambiguous.

Inferred roles come from extraction rules that interpret evidence rather than directly reading a declared relation. Examples include matching a test filename to a source file, pairing `.md` and `.mmd` diagram paths, or finding command-shaped text in a task body. Inferred edges should use `source_kind` values such as `path_rule`, `content_scan`, or `test_name`; they require a `notes` value when confidence is `medium` or `low`.

Low-confidence inferred roles are provisional graph hints, not workflow truth. They must not be used to mark tasks complete, close issues, or claim implementation coverage without a declared or manually reviewed edge. Filename similarity alone must remain `low` confidence and must not create high-confidence `implements`, `validates`, or `tests` edges.

### First-Extractor Allowed Roles

The first extractor may emit only roles marked `yes` in the role catalog: `references`, `documents`, `specifies`, `constrains`, `validates`, `invokes`, `defines`, and `routes`.

These roles are allowed first because they can be read from declared document surfaces, SLDB semantic inputs, explicit task validation text, command references, definition files, and board/index routing without implementing source-code analysis, graph runtime behavior, fixtures, CLI graph commands, or self-reflection. The first extractor must not emit `implements`, `tests`, `materializes`, `renders`, `generated_from`, `source_for`, `uses`, `supports`, `violates`, or `configures` until a later task defines the necessary evidence rules and validation fixtures.

### Required Edge Metadata

Every emitted edge must include `role`, `source_kind`, `confidence`, and `provenance_path`. Declared edges should include a `provenance_locator` whenever the relation comes from a field, section, board row, or task validation line. Inferred edges should include a `provenance_locator` when a rule matched a path pair, filename, test name, command token, or content span, and must include `notes` unless confidence is `high`.

## Relation Direction Policy

Edges should point from the artifact carrying the relation evidence to the artifact being referenced, realized, validated, invoked, routed, or configured. This preserves the existing atom rule: documents and other surfaces point to atoms; atoms do not point outward to every consumer.

Use inverse traversal in KGDB for questions such as "what implements this atom?" rather than storing duplicate reverse edges. Add a reverse edge only when it has a distinct role and distinct evidence, such as `source_for` on a source artifact versus `generated_from` on a generated artifact.

When a relation could be read both ways, prefer the direction that answers "which artifact made this claim?" The source node should be the file or modeled surface where the claim was declared or inferred.

## Confidence And Provenance Policy

Every edge must carry enough metadata to distinguish declared facts from weak inference. The initial required edge properties are:

| Property | Required | Meaning |
|---|---|---|
| `role` | yes | One controlled role from this vocabulary or a later compatible extension. |
| `source_kind` | yes | Extraction source: `declared`, `sldb_semantic`, `path_rule`, `content_scan`, `test_name`, or `manual`. |
| `confidence` | yes | `high`, `medium`, or `low`. |
| `provenance_path` | yes | Repository-relative file path where the relation evidence was found. |
| `provenance_locator` | no | Optional line, section id, frontmatter key, test name, or symbol locator. |
| `extractor` | no | Name/version of the future extractor or manual process that emitted the edge. |
| `notes` | no | Short human-readable reason when confidence is not `high`. |

Declared document metadata, explicit task dependencies, board routes, and explicit config/model declarations may be `high` confidence. Relations inferred from path conventions or filename similarity must not exceed `medium`; filename similarity alone must be `low` and must not create high-confidence `implements` edges.

## Extension Policy

New node kinds and roles may be appended when a task or extractor needs them. Existing names must not be renamed casually because graph snapshots and downstream traversal depend on stable vocabulary. Extensions should document direction, source evidence, confidence expectations, and whether the role overlaps with the atom-reference role vocabulary.

KGDB does not need special built-in knowledge of these names beyond accepting extensible node and edge properties. If a missing KGDB or SLDB capability is discovered while implementing graph extraction or traversal, record it in that system's owning inbox/drawer before continuing.

## Non-Goals

- Do not implement extractors, fixtures, CLI commands, graph build commands, graph neighbor commands, or graph runtime behavior in this task.
- Do not define symbol-level source graph nodes yet.
- Do not make KGDB parse SLDB documents or derive SLDB semantic tags.
- Do not make deskops own graph persistence or traversal semantics.
- Do not formalize OWL, ontology reasoning, or RDF mappings now.
- Do not replace the existing document-to-atom reference convention; reuse it where role meanings overlap.
- Do not close the separate atom-reference role vocabulary issue; this document only avoids conflicting with it.
