# Round 03 — Add task y advance rotos

**Source:** ST-add-task

## add task

| Aspect | Resultado |
|---|---|
| `add task --title "X" --goal "Y"` | Crea el archivo, **pero exit code 1** |
| Auto-generación | Crea routine, checklists, conditions, edges, operators automáticamente |
| Error en stdout | Pydantic errors sobre `id` / `status` requeridos aparecen en stdout a pesar de que el archivo se creó bien |

**BUG (medium):** exit code 1 con errores de validación de Pydantic a pesar de crear el archivo exitosamente. `id` y `status` son auto-generados pero el sistema no los pasa al modelo antes de validar.

## advance task — CRITICAL

| Comando | Resultado |
|---|---|
| `advance task --help` | No tiene flag `--to` |
| `advance task <id>` | Dice "has no routine" |
| `advance task <id> --to in_progress` | `--to` no existe como flag |

**BUG (critical):** `advance task` no funciona. La causa raíz: el campo `routine` en el archivo de task es sobreescrito por el primer checklist item durante la creación/extracción. Cuando `_load_routine` busca `routine-task-*` no lo encuentra y retorna None.

Además, `advance task` no tiene `--to` — el help no documenta cómo se supone que funcione.

## add otros tipos

| Tipo | Comando | Exit | Archivo |
|---|---|---|---|
| ritual | `--title "X" --purpose "Y"` | 0 | `desk/rituals/ritual-X.md` |
| board | `--title "X" --scope "Y"` | 0 | `desk/tasks/board-X.md` (en tasks!) |
| condition | `--title "X"` | 0 | `desk/primitives/conditions/condition-X.md` |
| checklist | `--title "X"` | 0 | `desk/primitives/checklists/checklist-X.md` |
| hook | `--title "X"` | 0 | `desk/primitives/hooks/hook-X.md` |
| step | `--title "X"` | 0 | `desk/steps/step-X.md` |
| atom | `--title "X"` | 0 | `desk/atoms/atom-X.md` |
| faq-doc | `--title "X"` | 0 | `desk/faq/faq-X.md` |
| repository | `--name "X" --path "/tmp"` | 0 | `desk/registry/repo-X.md` |

## Inconsistencias de flags

- `condition` usa `--title`, NO `--name` (pero el help sugiere `name`)
- `repository` usa `--name`, no `--title`
- Todos los demás usan `--title`

## board va a desk/tasks/

`add board` escribe en `desk/tasks/` (compartido con tasks), no en `desk/boards/`. Hay colisión de namespace.

## list commands rotos por artifacts incompletos

- `list tasks` falla si existe `task-item.md` con campos vacíos
- `list rituals` falla si existe `ritual-item` con campos vacíos
- `list pills` falla si existe `pill-none.md` con campos vacíos

**BUG (medium):** artifacts pre-existentes incompletos rompen `list` con errores de validación Pydantic no manejados. El sistema debería skipearlos en vez de crashear.
