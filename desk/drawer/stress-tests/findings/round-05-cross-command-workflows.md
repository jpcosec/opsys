# Round 05 — Cross-command workflows

**Source:** round-05-subagent-04

## Dos sistemas de FAQ separados

`deskops faq` lee de `docs/faq.md` (preguntas estáticas). `deskops add faq-doc` / `list faq-docs` / `show faq-doc` operan en `desk/faq/`. Ambos sistemas **nunca interactúan**:
- `deskops faq "deploy"` falla aunque exista un faq-doc con ese título
- `deskops faq` (sin args) lista 14 preguntas estáticas, no los faq-docs creados
- El usuario no tiene forma de descubrir faq-docs via `faq` command

## Dos comandos para registrar repos

`deskops repo register deskops .` → ID: `deskops` (sin `repo-` prefix)
`deskops add repository --name "deskops-alt"` → ID: `repo-deskops-alt`
Inconsistente. Además `repo register` no crea tags, `add repository` sí.

## list inbox-notes vs inbox --list

`list inbox-notes` muestra 2 notas. `inbox --list` muestra 13. Dos commands para la misma operación con resultados distintos y formatos distintos.

## Ritual y step no se pueden linkear

`add step` no tiene `--ritual` flag. `add ritual` no acepta step IDs. Steps quedan huérfanos.

## board y task no se linkean

Board se crea con tasks vacío. Task se crea pero no se asocia al board. No hay flag `--board` en `add task` ni `--task` en `add board`.

## `show board` mislabel

El output de `show board` muestra tags bajo la label `rituals:`:
```
rituals: workspace:desk, artifact:board
```
(son tags, no rituals)

## Filenames vs directorios esperados

- `desk/pills/` no existe → pills están en `desk/contexts/`
- `desk/boards/` no existe → boards están en `desk/tasks/`
- `desk/repositories/` no existe → repos están en `desk/registry/`

## Created artifacts no aparecen en graph edges

Después de crear tasks, rituals, boards, atoms, steps: `graph neighbors` muestra 0 edges para todos. 286 nodos, 0 edges.
