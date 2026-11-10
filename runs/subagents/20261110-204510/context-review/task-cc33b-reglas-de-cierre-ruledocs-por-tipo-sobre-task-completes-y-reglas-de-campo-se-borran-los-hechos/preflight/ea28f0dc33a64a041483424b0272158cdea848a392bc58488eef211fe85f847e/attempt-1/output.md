## REFORMULACION

**Propósito.** Sustituir el cierre imperativo de deskops por reglas declarativas: una RuleDoc semilla `on_transition` sobre la arista `task_completes` (where `current_node = "ritual-testing"`) que exige los recibos `evidence` de CC33a, y RuleDocs `on_check`/`on_write` alert para las reglas de campo. Borrar los hechos y gates viejos.

**Resultado.** Reglas en `deskops/data/rules/` (semillas escritas en `desk/lifecycle/` por `desk update --apply`); `__closeout_evidence__`, `closeout_evidence_verified`, `pill_graduation_verified` y `_add_closeout_facts` eliminados (grep vacío); los 9 chequeos de CC38 asignados a CC33 convertidos a RuleDoc o con razón escrita; tests de closeout verdes, goldens idénticos, `doctor` limpio en 6 desks, doc, ritual y CHANGELOG.

**Repo.** Worktree de deskops, base origin/main 6d133045, en robocop2. Depende de CC33a (en main); CC33c fuera de alcance.

**Límites.** No cambia formato de `desk/` ni gramática del CLI (goldens de ayuda/salida idénticos, salvo `advance --to` de GC06). Nada a mano en `desk/`; todo vía `deskops`. Nada de Python supliendo una regla: hipótesis + nota a sldb. No toca grafo (CC33c), selectores/escrituras ni API de tags (DO7).

## AMBIGUEDADES

1. **«los 9 chequeos entre documentos que el inventario de CC38 asigna a CC33»** — a6 lista «filas 3, 5, 13, 14, 15, 18, 24, 25»: son 8 filas. Obliga a inventar el noveno chequeo.
2. **«Este nodo decide y deja escrito en el TaskDoc si closeout commit escribe los recibos»** (a2) — no fija la decisión; el ejecutor no sabe qué camino implementar.
3. **«la regla usa el recibo kind goldens de deskops review record (follow-up de CC32) si existe, si no hipótesis»** (a3) — la existencia de CC32 no consta en el input; obliga a inventar el estado.
4. **«si la RuleDoc necesita la API de tags de sldb, quedan como hipótesis»** (a6) — exige un juicio de expresividad no dado; sin él no se sabe si #3/#5 se escriben o se difieren.
5. **«goldens idénticos»** — no nombra el conjunto; a8/regla 4 mencionan desk de prueba y excepción GC06, pero no el listado exacto.
6. **«deskops doctor sin hallazgos nuevos»** — sin línea base ni umbral; obliga a inventar la comparación.

## DRY-RUN

**Lecturas previstas:** `deskops/data/rules/`, `data/lifecycle/closeout-task_completes.md`, `models/task_types.py:41-105`, `services/tasks.py:202-203,307`, `services/closure.py:836-837,1094`, `cli/commands/operations.py:44`, `runs/subagents/cc38-worker-report.md`, `desk/lifecycle/`.

**Cambios previstos:** semillas RuleDoc por tipo; edición de la arista sin `has(closeout_evidence_verified)`; borrado de los cuatro nombres y sus usos; conversión de los chequeos CC38; tests, doc y CHANGELOG.

**Dependencias:** CC33a integrado; CC32 (recibo goldens); DO6/DO7; `desk update --apply` idempotente.

**Validaciones futuras:** grep vacío; `edges_blocked` con `fact = "commit"`; re-bloqueo al editar goal; tests de a uno desde `/dev/shm`; goldens; `doctor` ×6; 4 pasos del workflow en clon limpio; suite completa por el supervisor.

## FUTURO

Decisiones humanas: a2 (¿closeout commit escribe recibos?), a3 (goldens/children), a6 (#3/#5 y #13/#14/#18/#24 como hipótesis). Pendiente de integración CC33c; nota a sldb si el lenguaje no expresa una regla; el supervisor corre la suite completa sobre el resultado integrado.
