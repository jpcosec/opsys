# Result: task-closeout-verify-tolerates-multi-document-yaml

## Changes

- `deskops/graph/extract_edges.py` — `_atom_declarations`
  - Replaced `yaml.safe_load` of each fenced YAML block with `yaml.safe_load_all`.
  - Skips a block that raises `yaml.YAMLError`, or that does not contain exactly one mapping document.
  - Single-document blocks behave exactly as before.
- `deskops/graph/extract_docs.py` — `_read_yaml_metadata`
  - Catches `yaml.YAMLError` and returns `{}`; a multi-document/invalid YAML file yields no metadata instead of aborting graph extraction.
- `tests/test_closeout.py` — added `test_closeout_verify_tolerates_multi_document_yaml`
  - Builds a throwaway repo, adds a docs Markdown with a two-document fenced YAML block and a two-document `spec/*.yaml`, then drives the real CLI (`python -m deskops closeout verify`) and asserts normal evidence behavior.

## Validation

- `PYTHONPATH=/tmp/rw/wt/verifyyaml python -m pytest tests/test_closeout.py -q`
  - Final: `17 passed in 2.24s`
- `PYTHONPATH=/tmp/rw/wt/verifyyaml python -m pytest tests -q`
  - Final: `349 passed, 3 skipped in 209.00s`
- Real reported repo, read-only:
  - `cd /home/jp/proyectos/SLDB_1/UIs/graph_ui && PYTHONPATH=/tmp/rw/wt/verifyyaml python -m deskops closeout verify --root . --task task-graph-ui-instalable-pyproject-con-dependencias-reales-y-sin-hacks-de-sys-path`
  - Result: `rc=1`, empty stderr, normal JSON evidence report (`missing_tests_evidence`, `missing_atom_or_materialization_link`, `missing_commit_evidence`). No `Unexpected:`.

## Unfixed-code test result

`tests/test_closeout.py::test_closeout_verify_tolerates_multi_document_yaml` failed before the fix:

```
assert 'Unexpected' not in 'Unexpected:...---\n    ^\n'
Unexpected: expected a single document in the stream
  in "<unicode string>", line 1, column 1:
    name: a...
```

The failing read for the reported repo was:

```
deskops/operations.py verify_task_closeout
  -> _build_closeout_graph_context
  -> extract_declared_edges
  -> _atom_declarations
  -> yaml.safe_load (extract_edges.py:253)
```

## Task discrepancies / ambiguity

- Task file list named `deskops/operations.py`; that file contains no raising YAML read. The actual faults were in `deskops/graph/extract_edges.py` (`_atom_declarations`) and `deskops/graph/extract_docs.py` (`_read_yaml_metadata`).
- Implementation Path step 1 claims a standalone `docs/x.vocabulario.yaml` makes verify scan the repo. It does not: `extract_doc_nodes` reads only `docs/**/*.md` and `spec/**/*.{md,yaml,yml}`, and graph extraction reads no arbitrary docs YAML. The real graph-ui failure comes from a two-document fenced YAML block inside `docs/representacion/propuesta-vocabulario-visual.md` (the YAML stream starts `# NotationDoc notation-uml-clases`). The regression test covers that real shape plus a multi-document file under `spec/`.
- No sldb bug found; the `ComposerError` is standard PyYAML behavior, not an sldb defect.
