# adv-worker: advance y doctor ante semillas del ciclo de vida anteriores a CC31 (task.debug)

TaskDoc: `desk/tasks/task-advance-y-doctor-ante-semillas-del-ciclo-de-vida-anteriores-a-cc31-doctor-las-reporta-y-advance-fall.md` (7392c60a).
Base: origin/main `987dd5b7`, rama `wt/adv-doctor`.
Reproducción del coordinador: `runs/subagents/20261110-repro-advance/repro.log`.

## Causa raíz (escrita antes del arreglo)

### d1: doctor dice "Desk is healthy" con una semilla managed del ciclo de vida desactualizada

`deskops doctor` (`deskops/cli/commands/doctor.py`) mira tres cosas: estructura (Board, drawer,
phase.md), el `sldb stores check` de los documentos trackeados y los modelos registrados.
Ninguna compara el desk con las semillas del paquete:

- `sldb stores check` compara cada documento con **su propio** hash indexado. La arista editada
  vía `sldb fields update` queda reindexada por sldb, así que su nota es `ok`: para el store no
  hay nada que reportar. El store no sabe qué texto trae el paquete de deskops.
- La única comparación con el paquete es la de `seed_desk(root, restore_managed=True)`
  (`deskops/workspace.py:239`), que solo corre en `deskops init` y `deskops desk update --apply`
  (vía `write_lifecycle_graph`). `doctor` llama a `seed_desk(root)` solo con `--repair` y sin
  `restore_managed`, que convierte toda semilla en `if_missing` y por diseño no mira las que
  difieren.

Resultado: una `RelationDoc` de `desk/lifecycle/` sin `attributes.sets` (el ciclo de vida previo a
CC31, migración 2d69e9c6) es invisible para doctor.

### d2: advance falla con un ValidationError de pydantic que no nombra la causa

`deskops/lifecycle.py` `advance` toma la primera transición cuya condición se cumple y aplica sus
efectos tal como el desk los declara (`Transition.sets`, de `edge.effects` o de
`attributes.sets`). Con `attributes: {}` los `sets` quedan vacíos: el payload recibe
`history: [..., task_activates]` y `current_node: ritual-testing` pero `status` sigue `draft`.
`sldb.api.apply_effects` valida el resultado con el modelo del tipo de tarea, y el validador de
CC37 (`deskops/models/task_lifecycle.py`, `lifecycle_errors`) compara contra `lifecycle_table()`,
la tabla **del paquete**, que exige `active` tras `task_activates`. Así el grafo que se ejecuta
(el del desk) y el que valida (el del paquete) divergen, y nadie compara los dos antes de
escribir: el error sale de pydantic dentro de `apply_effects`, envuelto por
`deskops/cli/main.py` como `Validation error:` sin nombrar la arista ni el arreglo. (La tarea no
se escribe porque la excepción salta antes de `write_doc`; el defecto es el mensaje y el punto
de control, no una escritura parcial.)

### Arreglo previsto

- d2 (b6): en `lifecycle.advance`, antes de `apply_effects`, comparar la transición elegida con
  `lifecycle_table()` (cache, sin leer archivos): mismo `relation_type`, mismo target y mismo
  `sets.status`. Si difiere, se lanza un error de ciclo de vida (subclase de
  `LifecycleGraphMissing`, que el CLI de advance ya imprime con exit 1) con el texto de b5.
- d1 (b1, b5): doctor llama a `seed_desk(root, apply=False, restore_managed=True)`; por cada
  `rewritten_paths` compara el frontmatter de la semilla del paquete con el del desk (claves de
  primer nivel que difieren, ordenadas) y emite un hallazgo por archivo.
