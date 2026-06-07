# Round 05 — --from-yaml para todos los tipos

**Source:** round-05-subagent-06

## Comportamiento inconsistente: empty YAML `{}`

8 tipos (pill, ritual, board, atom, repository, inbox-note, faq-doc, step) → **exit 0, crean basura** con `id: *-none`, `title: "None"`.
7 tipos (task, condition, operator, checklist, hook, edge, routine) → **exit 1, KeyError** en `'title'`. Clean failure.

Causa raíz: los primeros usan `.get("title")` (devuelve `None` → `str(None)` → `"None"`), los segundos usan `payload['title']` (KeyError).

## BUG en `_normalize_task_payload`: list() vs _coerce_list()

`_normalize_task_payload` usa `list(payload.get("pills") or [])` que para un string como `pills: single-pill-ref` lo splitea en **caracteres**: `['s', 'i', 'n', 'g', 'l', 'e', ...]`.

Afecta: `references`, `depends_on`, `pills`, `files`, `validation`, `history`, `tags` en task.

`_coerce_list()` existe pero se usa solo en `compile_task_bundle_spec` (post-normalize).

## YAML type coercion bug

- `created_at: 2026-01-01` → YAML lo parsea como `datetime.date`, Pydantic espera `str` → crash
- `scope: no` → YAML boolean `False` → `False or ""` → `""` (inconsistente con `done_when: true` que da `"True"`)

## Custom `id` en YAML funciona para task

`id: task-my-custom-id` → exit 0, ID respetado.

## Extra fields silenciosamente ignorados

Todos los tipos. Sin warning, sin error. Pydantic models sin `model_config = {"extra": "forbid"}`.

## Errores siempre wrapped en "Unexpected:"

KeyError, FileNotFoundError, YAML parse error, Pydantic validation error — todos con prefijo `Unexpected:`.

## clean failure property

Para la mayoría de los casos de fallo, no se escriben archivos. Excepción: `create_task_bundle` puede escribir task + primitives y luego fallar en `_append_task_to_board`, dejando archivos huerfanos.
