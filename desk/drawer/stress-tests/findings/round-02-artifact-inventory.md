# Round 02 — Artifact inventory and show/add quality

**Source:** ST-11

## Qué tiene datos vs qué está vacío

| Artifact | Items | Notas |
|---|---|---|
| pills | 11 | Datos completos con campos what/why/when/where/how/how_not |
| atoms | 4 | Solo los de raíz, no los 60 anidados |
| repositories | 1 | `repo-deskops` |
| inbox-notes | 2 | |
| steps | 1 | `step-document-the-cli` |
| tasks, routines, conditions, operators, checklists, hooks, edges, rituals, boards, faq-docs | 0 | Modelados en el parser pero sin archivos de datos |

## Pill show

Funciona para los 11. Output verboso pero completo con todos los campos del spec.

## Step show

Funciona. Renderiza campos `action` y `outcome`.

## Repository show

Funciona. Renderiza name/path/status/description.

## Add pill

Crea archivo en `desk/contexts/` (no `desk/pills/`). Imprime path. Slug se genera del `--title`.

## Add flags

Cada `add` subcomando tiene sus propios flags (`--what`, `--why` para pill; `--purpose`, `--trigger` para ritual; etc.). No hay base común (ni `--title` compartido). Todos soportan `--from-yaml` para batch loading.
