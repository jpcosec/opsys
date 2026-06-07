# Round 04 — Spec YAML structure

**Source:** ST-fields-primitives

## Directory layout

| Directorio | Archivos |
|---|---|
| `spec/artifacts/` | 9 (atom, board, faq, inbox_note, pill, repository, ritual, step, task) |
| `spec/fields/` | 42 (title, goal, status, what, why, when, where, how, how_not, etc.) |
| `spec/primitives/` | 10 (6 operators, 3 checklists, 1 edge_set) |

## Schema uniforme

Todos los specs siguen `{id, title, type, version, data}`.

## Task artifact incompleto

Es el **único** artifact sin `doc.model`. Todos los demás declaran su modelo Pydantic (`TaskDoc`, `PillDoc`, etc.). Task no.

## 6 campos huérfanos

Definidos en `spec/fields/` pero no referenciados por ningún artifact:
- `category`, `distinct_from_pills`, `for_whom`, `materializes_into`, `related_atoms`, `stabilized_in`

Probablemente reservados para uso futuro.

## Sin validation rules

0 rules de validación en 61 archivos YAML. La única constraint es `value_type` (string, markdown, enum, list) y `required` (true/false). No hay `description`, `pattern`, `min`, `max`, ni ningún otro metadata.

## Template system

El syntax `⸢...⸥` está declarado en AGENTS.md pero no aparece en ningún spec YAML. Los primitives usan `{braces}` style (`{task_id}`).

## Task lifecycle state machine

```
execution → [checklist: execution_ready] → operator: activate
  → [checklist: testing_ready] → operator: mark_ready_for_testing
  → [checklist: closeout_ready] → operator: close → complete
```

6 operators, 3 checklists, 6 edges. Definido en `spec/primitives/`.
