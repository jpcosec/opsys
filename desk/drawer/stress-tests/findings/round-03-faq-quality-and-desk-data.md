# Round 03 — FAQ quality and desk data inventory

**Source:** ST-faq

## FAQ

- 14 preguntas con respuestas sustantivas (ejemplos de código, tablas de flags, cross-references)
- **`faq --topic` no existe** — error `unrecognized arguments`
- `faq <valid-slug>` funciona, retorna Q&A completo
- `faq <invalid-slug>` error claro: `Unknown FAQ question: X`
- Gap: no hay FAQ entry sobre `deskops graph` o `deskops atoms`

## Desk directory file counts

| Directorio | Archivos | Notas |
|---|---|---|
| `desk/atoms/` | 5 + 60 anidados | Solo 4 visibles via CLI |
| `desk/contexts/` (pills) | 13 | 11 pills numbered + index + readme |
| `desk/inbox/` | 11 | Notas con timestamp |
| `desk/models/` | 17 | Model docs |
| `desk/rituals/` | 3 | closeout, execution, testing |
| `desk/routines/` | 2 | Task routines |
| `desk/steps/` | 1 | step-document-the-cli |
| `desk/tasks/` | 3 | Board.md + tasks |
| `desk/registry/` | 1 | repo-deskops |
| `desk/primitives/` | 9 | checklists, conditions, edges, hooks, operators |
| `desk/faq/` | 0 | Vacío — FAQ compilado de otra fuente |
| `desk/fields/` | 0 | Vacío |
| `desk/boards/` | 0 | Vacío |

## Pill quality

Los 11 pills reales tienen todos los campos (what, why, when, where, how, how_not, tags). Calidad excelente.
