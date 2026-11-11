## REFORMULACION

**Propósito:** que `deskops desk update --apply` repare, no solo reporte, las tareas no terminales con `history` vacía de desks pre-CC31 (hoy "Invalid task documents (not written)"), migrándolas a `draft` en el nodo de entrada y dejando nota en `summary`, y siga con el resto de reparaciones.
**Resultado:** rama nueva en `legacy_state_migration` (`deskops/models/task_lifecycle.py`), nota + línea de reporte vía la escritura de frontmatter existente (`deskops/workspace.py`), tests sobre `tmp_path`, doc en `docs/operator-manual.md` y entrada Fixed en `CHANGELOG.md`.
**Repo:** deskops; el caso que desbloquea es el desk de Governance, pero la reproducción va en desk desechable.
**Límites:** fuera `history` no vacía incoherente, el validador y los status terminales; nada a mano en `desk/`/`.sldb/`, nunca `git add -A`.
Es un nodo ejecutable (task.debug), no un agregado.

## AMBIGUEDADES

1. "un status no terminal" / "los status terminales siguen con su tabla": no enumera qué status son terminales; obligaría a inventar el conjunto (¿`CLOSEOUT_STATES`? ¿`complete`?).
2. "una línea fija: "Migrada a draft … (<fecha ISO>)."": formato exacto de la fecha y forma de anteponerla ("Si summary ya tenía texto, se conserva después") — ¿salto de línea, separador? Habría que inventarlo.
3. "si current_node no está vacío y no es ya ese nodo": no dice qué hacer con status no terminal y `current_node` vacío, cuando la validación exige "nodo de entrada".
4. "rc 0": la reproducción da "rc 1"; no aclara si rc 0 vale solo cuando no queda otra tarea inválida.
5. "4 pasos del workflow de deskops": no se enumeran.
6. "Goldens de salida de desk update solo si cambia una línea existente": no nombra los goldens ni si cambia la línea "Invalid task documents" de la reproducción.

## DRY-RUN

**Lecturas:** `legacy_state_migration`, `lifecycle_errors`, `lifecycle_table().entry_node`; `legacy_task_states`, `rewrite_task_fields`, `migrate_legacy_task_states`, `_migrated_frontmatter`; tests de estados heredados y goldens; `docs/operator-manual.md`; CHANGELOG.
**Cambios previstos:** rama que devuelve `{status: (antes,"draft"), current_node: (antes, entry), summary: (antes, nota+texto)}` validada con `lifecycle_errors`; `summary` multilínea obliga a revisar `_migrated_frontmatter`; tests nuevos `tmp_path`; doc y CHANGELOG.
**Dependencias:** migración antes de registrar modelos; `TaskDoc` debe aceptar el `summary` anotado; idempotencia en segunda corrida.
**Validaciones futuras:** pytest de a uno con `TMPDIR=/dev/shm` y guarda `pgrep`; `sldb stores check`; goldens de ayuda/salida; 4 pasos en clon limpio.

## FUTURO

Los 4 pasos del workflow los corre el coordinador; el informe `runs/subagents/nonterm-worker-report.md` lo produce el ejecutor; la decisión del overlord es revisable por un humano; el desbloqueo efectivo de Governance y la migración de los otros desks (shared_llm-gateway, Chatbot_Infra, labchile) ocurren en sus repos.
