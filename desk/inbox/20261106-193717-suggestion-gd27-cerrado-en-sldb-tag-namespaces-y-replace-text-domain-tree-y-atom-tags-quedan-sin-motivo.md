---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-06T19:37:17'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# GD27 cerrado en sldb: tag_namespaces y replace_text; domain_tree y atom_tags quedan sin motivo

_Describe the incoming message with enough evidence to triage._

GD27 cerrado en sldb (squash fb733e86, closeout 9f368024). Nuevo: StoreDeclaration.tag_namespaces ({name, hierarchical, folder_axis, anchored_by: {model, field}}) en .sldb/store.yaml, chequeado por la familia incorporada builtin:tag_namespace:<name> en on_write (save_document_payload, transaction.update, apply_batch, POST /save, replace_text), stores check, sldb rules check y sldb rules explain; sldb.api.tag_tree(store, namespace) → {namespace, roots, orphans, unplaced}; sldb.api.tag_folder(tag) → a/b; sldb.api.tag_check(store); sldb.api.tag_namespaces(store); CLI sldb tags namespaces|tree NAMESPACE|check (envelope); sldb.api.replace_text(store, ref, old, new, *, count=1, transaction=None) y sldb docs replace REF --old --new [--count N] (envelope). Código de deskops que queda sin motivo: domain_tree.py prefixes, missing_parents, require_domain_parents y DomainTree.tree/check (→ tag_namespaces anchored_by + tag_tree + tags check), atom_tags.py validate_atom_tag_namespaces (→ namespace no declarado) y axis_folder_relpath (→ tag_folder), y el reemplazo de texto propio de doc_io (→ replace_text). Ojo: create_document y track_document_file no evalúan on_write (q18, hueco previo de GO08): al crear, validar con tags check o escribir vía transaction.update. docs/architecture/tags.md y transactions.md §replace_text.
