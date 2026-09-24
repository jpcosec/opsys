# Atoms

This guide is a human-facing materialization of these atoms:

- `desk/atoms/atom-protoatoms-are-free-atoms-captured-before-typing.md`
- `desk/atoms/atom-typing-a-protoatom-keeps-a-redirect-stub.md`
- `desk/atoms/atom-atom-folder-axis-is-one-configurable-tag-namespace.md`
- `desk/atoms/atom-atom-lifecycle-includes-validate-and-delete-with-inbound-reference-guard.md`
- `desk/atoms/atom-atom-lifecycle-is-complete-create-from-source-split-merge.md`

## What an atom is

An atom represents a curated raw answer to a single knowledge question, written as one stable unit. 

*(Note: The rule restricting atoms to exactly one 5WH1+ question, chosen from `what, why, how, how_not, when, where, for_whom`, is enforced by the `AtomDoc` model in code.)*

You create an atom with `deskops add atom`.

```bash
$ deskops add atom --title "Example knowledge" \
  --five-wh-one-plus what \
  --answer "This is the answer." \
  --tags topic:atoms

Created atom atom-example-knowledge
Path: desk/atoms/atom-example-knowledge.md
```

Protoatoms are free knowledge units captured before typing. They have a title, free markdown content, and tags, but do not answer a fixed 5WH1+ question. They are the lowest rung of typing, typically captured during a brainstorm or mindmap. Typing a protoatom creates a new document of the target SLDB model, keeping the protoatom as a redirect stub so old IDs keep resolving.

## Tag namespaces and the folder axis

Atoms use namespaced semantic tags for retrieval and grouping (`namespace:value`). The namespaces are controlled but extensible. 

When creating tags, you must use an existing namespace defined in `desk/atoms/tag-namespaces.yaml` (such as `system`, `topic`, `layer`, `domain`, or `pattern`). 

Desks can declare one tag namespace as the physical folder axis for atoms by setting `atom_folder_axis` in `desk/config.json`. The default is `null`, keeping atoms in a flat layout under `desk/atoms/`.
- Only the axis namespace decides folder placement; all other tags are preserved but do not affect paths.
- An atom with exactly one `axis:<value>` tag is placed under `desk/atoms/<value-as-folders>/` (e.g. dot-notation values like `mepu.licitaciones` become `mepu/licitaciones/`).
- An atom with multiple values of the axis namespace is rejected with an explicit error to maintain deterministic physical placement.
- Atoms without an axis tag stay flat.

You can reorganize atoms into their axis folders idempotently. If `atom_folder_axis` was changed in `config.json` to `"topic"`:

```bash
$ deskops atoms reorganize

Folder axis: topic
Moved atom-example-knowledge: desk/atoms/atom-example-knowledge.md -> desk/atoms/atoms/atom-example-knowledge.md
```

### Adding a tag namespace

If existing namespaces do not cover the required knowledge grouping, you can add a new namespace to the registry. The namespace must match `^[a-z][a-z0-9_]*$`.

```bash
$ deskops atoms add-namespace myns \
  --meaning "What this namespace means" \
  --use-when "When to use it" \
  --do-not-use-when "When to use an existing one instead" \
  --example "myns:example"

Added atom tag namespace myns
Path: desk/atoms/tag-namespaces.yaml
```

## Lifecycle operations

The atom lifecycle is complete with support for validation, deletion, splitting, and merging.

### Validation
`deskops atoms validate` checks atom integrity and lifecycle safety.

```bash
$ deskops atoms validate --all

Atom: atom-example-knowledge
Path: desk/atoms/atoms/atom-example-knowledge.md
- valid
```

### Deletion with inbound-reference guard
`deskops atoms delete` removes an atom and untracks it from the store, but only when no inbound references exist. 

```bash
$ deskops atoms delete atom-example-knowledge

Deleted atom atom-example-knowledge
Path: desk/atoms/atoms/atom-example-knowledge.md
Store untracked: yes
```
*(Use `--force` to delete even when inbound references exist.)*

### Split, Merge, and Create-from-source
- **Split**: Divides one atom into new atoms while keeping the original as a redirect stub (provenance-safe rerouting, inbound-reference guard).
- **Merge**: Merges a source atom into an existing target atom, rewriting inbound references and preserving provenance.
- **Create-from-source**: Creates an atom from a pill, graph finding, or diagram source, maintaining exact provenance back to the source surface.

These mutating operations block on ambiguity unless forced, and typically run as deferred drawer work.
