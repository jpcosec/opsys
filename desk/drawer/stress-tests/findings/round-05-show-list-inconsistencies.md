# Round 05 — Show/list: 13/15 tipos leakean paths, glob bug

**Source:** round-05-subagent-03 + round-05-subagent-04

## CRITICAL: `_resolve_glob` returns WRONG artifact

`show <type>` usa `f"{doc_id}*.md"` glob. Si `task-board` existe y `task-board-task-2` también, el glob `task-board*.md` matchea AMBOS. El que se muestra es el primero alfabéticamente, que suele ser el **sufijo** (no el exacto).

Ejemplos:
- `show task task-board` → muestra `task-board-task-2` (es el que querés pero hay otros)
- `show repository repo-deskops` → muestra `repo-deskops-alt` (el equivocado)
- `show operator operator-task` → muestra `operator-task-aaaauniquetitle999-activate`

Esto es un **data safety bug**: podes pedir un artifact y que te muestren otro sin advertencia.

## CRITICAL: `list inbox-notes` muestra 2 de 13

`list inbox-notes` solo muestra 2 notas. `inbox --list` muestra las 13. Causa: `list inbox-notes` usa un glob pattern `inbox-note-{slug}*` que no matchea los date-prefixed filenames (`20260604-171903-unclear-bug-found.md`).

## CRITICAL: `show <type> ""` matchea todo

`show task ""` → `*.md` glob, matchea `Board.md`, crash con Pydantic error.
`show pill ""` → crash similar.
`show condition ""` → devuelve la primera condition alfabética (no es un error, pero es silencioso).

## CRITICAL: `list tasks` crash por un archivo inválido

`task-item.md` con `# ` (título vacío) → `list tasks` entero crashea con Pydantic traceback. Idem `list pills` con `pill-none.md`.

## 13/15 show types leakean paths absolutos

`show`, `show routine` están bien ("No task found").
Los otros 13 tipos muestran:
```
Unexpected: No artifact.pill file found for id 'nonexistent' in /home/jp/.../desk/contexts
```

## 3 formatos de output distintos en list

- `list tasks`: `id | status | current_node`
- `list conditions/operators/checklists/hooks/edges`: `id | status | title`
- `list pills/rituals/boards/atoms/repositories/inbox-notes/faq-docs/steps`: `id | title` (sin status)

Sin `--format` flag en ningún list/show.

## Rituales invisibles: closeout.md, execution.md, testing.md

Existen en `desk/rituals/` pero tienen filenames que no empiezan con `ritual-`. `list rituals` los ignora. `show ritual ritual-closeout` falla. `show ritual closeout` funciona (filename stem match, no ID).

## Board.md invisible

`board-001` en `Board.md` (capital B). `list boards` lo ignora porque busca `board-*.md`.

## show: filename stem vs internal ID inconsistency

- `show ritual` busca por internal `ID:` field
- `show pill` busca por filename stem
- Combinación: `show ritual closeout` funciona pero `show ritual ritual-closeout` falla

## Error messages van a stdout, no stderr

`deskops show task nonexistent 2>/dev/null` → mensaje aparece. Debería ir a stderr.
