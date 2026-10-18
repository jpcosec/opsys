# task-canonical-atom-reference-metadata — result

## Changed files and functions

- `deskops/atom_references.py` (new)
  - Constants: `CANONICAL_FIELD="atoms"`, `LEGACY_FIELDS=("related_atoms",)`, `MATERIALIZATION_FIELD="source_atoms"`, `ALLOWED_ROLES=("references","documents","specifies","constrains","validates")`, `DEFAULT_ROLE="references"`.
  - `ParsedAtomReference` dataclass (`atom_id`, `role`, `field_name`, `violation`, `as_tuple()`).
  - `parse_atom_reference(value, field_name=...)`: string -> `references`; `{id, role}` -> declared role; unknown role -> `violation="invalid_atom_reference_role"` without rewriting.
  - `iter_atom_reference_values(value)` list/scalar normalizer.
- `deskops/graph/extract_edges.py`
  - Replaced local `ALLOWED_ATOM_ROLES`/`DEFAULT_ROLE` and literal field tuple with imports from `deskops.atom_references`.
  - `_declarations_from_mapping` now iterates `(CANONICAL_FIELD, MATERIALIZATION_FIELD, *LEGACY_FIELDS)`.
  - `_atom_declarations_from_value` still maps an invalid role to `references` so extraction continues.
- `deskops/graph/checks.py`
  - Added `AtomReferenceFinding` dataclass and `find_atom_reference_violations(root)`.
  - Reads Markdown frontmatter only under `desk/` and `docs/`; skips dot-parts and fenced YAML.
  - Emits `invalid_atom_reference_role` per invalid item and one `legacy_atom_reference_field` per `related_atoms` field. Validates top-level `atoms`, top-level `source_atoms`, and `materialization.source_atoms`.
- `deskops/graph/self_reflection.py`
  - `drift_check_knowledge_surfaces` appends `atom-reference: <path>#<locator> <reason>` findings from `find_atom_reference_violations`.
- `docs/knowledge-graph/desk-source-graph-vocabulary.md`
  - `references` role row now names `atoms` as canonical and the five roles.
  - New "Atom Reference Field And Roles" subsection documents `atoms`, five roles, default, legacy `related_atoms`, `source_atoms`, and drift finding kinds.
- `tests/test_atom_reference_convention.py` (new)
  - Valid five roles pass; unknown role yields exactly one finding; `related_atoms` yields one legacy finding; bare string/mapping-without-role map to `references`; fenced YAML examples are not scanned.

## Validation commands and final result lines

- `PYTHONPATH=/tmp/rw/wt/atomref python -m pytest tests/test_atom_reference_convention.py -q`
  - `6 passed in 0.19s`
- `PYTHONPATH=/tmp/rw/wt/atomref python -m pytest tests/test_graph_extract_edges.py tests/test_graph_self_reflection.py -q`
  - `5 passed in 0.26s`
- `PYTHONPATH=/tmp/rw/wt/atomref python -m pytest tests -q`
  - `477 passed, 3 skipped in 754.19s (0:12:34)`
- `PYTHONPATH=/tmp/rw/wt/atomref python -m pytest -q` (pytest `testpaths = ["tests"]`)
  - `477 passed, 3 skipped in 782.04s (0:13:02)`
- `ruff check deskops/atom_references.py deskops/graph/checks.py deskops/graph/extract_edges.py deskops/graph/self_reflection.py tests/test_atom_reference_convention.py`
  - `All checks passed!`
- `PYTHONPATH=/tmp/rw/wt/atomref python -m deskops drift check --root .` (read-only)
  - exit 1 with pre-existing unrelated findings (role-doc mismatch and unrouted source-file findings); zero `atom-reference:` lines.

An initial 600s full-suite attempt timed out at ~75% because this environment takes ~13 minutes; re-run with a longer timeout passed as above.

## Tests against unfixed code

- None run. Pre-fix behavior was verified by reading `deskops/graph/extract_edges.py`: unknown roles were silently coerced to `references`, and `related_atoms` was accepted without reporting.

## Task issues / ambiguities

- The task says the parser returns `(atom_id, role, field_name)`. Implementation returns `ParsedAtomReference` with those attributes plus `.violation` (and `.as_tuple()`), because an explicit violation has to travel with the parsed value.
- "Make `atoms` the only structured artifact field" conflicts with keeping extractor behavior stable. Resolution: extractor still reads `source_atoms` and `related_atoms`; only drift reports the legacy field. `source_atoms` is only treated as the materialization field (top-level or nested under `materialization`), never as legacy.
- `related_atoms: []` still emits one legacy finding, since the field itself is legacy.
- The task cites no concrete line numbers, so there was nothing to re-verify beyond the named functions.
- No sldb bug observed.
