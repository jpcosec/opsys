## REFORMULACION

**Propósito:** que `deskops desk update --apply` repare las tareas no terminales con `history` vacía de desks pre-CC31, migrándolas a `draft` en el nodo de entrada y dejando nota en `summary`, sin abortar el resto de reparaciones.

**Resultado:** n1–n5 en `task_lifecycle.py`, `workspace.py`, tests, docs y CHANGELOG, más informe de causa raíz.

**Repo:** deskops/SLDB_1; el nodo es una tarea ejecutable (TaskDoc en `desk/`).

**Límites:** fuera history no vacía incoherente, validador y estados terminales; nada manual en `desk/` ni `.sldb/`; nunca `git add -A`.

## AMBIGUEDADES

1. Goal: «migra a draft, en el nodo de entrada» frente a n1: «si current_node no está vacío y no es ya ese nodo». Con `current_node` vacío no se dice si se escribe el entry_node; obliga a inventar ese caso.
2. Goal: «las tareas no terminales con history vacía» frente a n1: «un status no terminal que no es entrada». Un status de entrada no terminal con history vacía cae fuera de n1 pero dentro del Goal; hay que decidir cuál manda.
3. n2: «antepone al campo summary una línea fija… Si summary ya tenía texto, se conserva después». El summary es escalar de una línea (`summary: ''`); no se indica si unir con salto, bloque YAML o espacio.
4. n2: «(<fecha ISO>)»: no se fija instante, zona ni precisión (¿hora de la corrida, `at` de la tarea?).
5. n5: «una en otro nodo (ritual-testing con history vacía)»: no indica el status de esa tercera tarea (¿active, ready_for_testing?).

## DRY-RUN

**Lecturas:** TaskDoc; `task_lifecycle.py` (`legacy_state_migration`, `ENTRY_STATUSES`, `OUTSIDE_LIFECYCLE_STATUSES`, `lifecycle_table`, `lifecycle_errors`); `workspace.py` (escritura de frontmatter y reporte); tests y goldens de `desk update`; docs y CHANGELOG.

**Cambios previstos:** rama n1 antes del `return None`; nota n2 al escribir; línea n3 en el reporte; tests n5 en `tmp_path`; doc y CHANGELOG.

**Dependencias:** tabla de ciclo de vida, escritor de frontmatter, formato de líneas b4, goldens.

**Validaciones futuras (sin ejecutar):** pytest con `TMPDIR=/dev/shm` y guarda pgrep anclada; `sldb stores check`; segunda corrida sin cambios; goldens; 4 pasos del workflow en clon limpio.

## FUTURO

El coordinador ejecuta los 4 pasos del workflow en clon limpio y produce `runs/subagents/nonterm-worker-report.md`. El overlord (humano) puede revisar su decisión del 2026-11-11. La reproducción vive en un desk desechable externo.
