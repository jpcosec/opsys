## REFORMULACION

**Objetivo:** consolidar los ajustes A–F de `review-source.md` en `brief.md`, `dag.yaml`, `reconciliacion.md` y `canonical-adjustments.md`; añadir el nodo planificado WS45; regenerar proyecciones; dejar `build_plan.py --check`, `validate_plan.py --check` y `context_review.py status` en verde, sin implementar nada.

**Alcance:** solo planificación documental en deskops. Archivos permitidos: los cuatro citados, proyecciones de `build_plan.py`/`render_diagram.py` (incluidas fichas en `desk/drawer/tasks/workspace-documental/`) y helpers locales solo si son imprescindibles. WS45 queda planificado en sldb, no implementado.

**Repo:** `SLDB_1/deskops`, plan `workspace-documental`.

**Límites:** no WS07, WS08–12, WS05, código, auditorías, reapertura de cierres, push ni P01–P09. `execution_authorized` sigue `false`; estado final `final_plan_reviewed`. Executor edita y regenera sin commits ni `context_review.py run`; Supervisor congela, revisa, dispone, registra y hace commits/closeout.

## AMBIGUEDADES

1. «Helpers locales del plan solo si son imprescindibles»: no se define el criterio de «imprescindible» ni quién lo autoriza; obligaría a inventar umbral y permiso.
2. «las proyecciones que build_plan.py y render_diagram.py generan»: `render_diagram.py` no aparece en Validation ni se indica si sus salidas deben regenerarse o commitearse; obligaría a inventar alcance y comando.
3. «Tester independiente de solo lectura»: no se especifica identidad, procedimiento ni formato del PASS; obligaría a inventar quién califica y cómo se registra.
4. «WS45 … lleva owner, prerrequisitos, entregable, aceptación y revisión real»: no se dan valores de owner ni lista de prerrequisitos; obligaría a inventar propiedad (¿sldb?) y dependencias.
5. «re-review barato de todos los inputs y contratos afectados»: «barato» y el conjunto «afectado» quedan abiertos; obligaría a inventar método y qué nodos de los 25+ requieren revisión.
6. «context_review.py run --stale y disposiciones» bajo Supervisor con «execution_authorized sigue false»: no se aclara si ejecutar `context_review` cuenta como ejecución; obligaría a inventar el límite de autorización.
7. «git diff --name-only 6d41f301..HEAD -- deskops/ …»: con cwd `deskops`, la base y el prefijo `deskops/` admiten lectura ambigua; obligaría a inventar el mapeo de rutas.
8. C-50 «nuevo delta de autoría de ViewDoc y NotationDoc concretos definidos por WS09/WS11»: no se concreta el contenido del delta; obligaría a inventar su especificación.

**Tareas futuras asignadas, no lagunas:** contrato WS12 (representación/precondición/escritores), productor Deskops condicional antes de WS25.2, comparación API/composición/wrapper, y no activar WS07/WS08–12 ni UI.

## DRY-RUN

**Fuentes a leer:** `review-source.md`, `handoff.md`, `canonical-adjustments.md`, `dag.yaml`, `brief.md`, `reconciliacion.md`, `context-review.md`, pills referenciadas y scripts validador (solo lectura).

**Entregable:** `result-summary.md` con antes/después, archivos A–F corregidos, WS45 completo, proyecciones regeneradas y `tester-result-summary.md`.

**Comandos posteriores (sin ejecutar):** `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`, `git diff --name-only 6d41f301..HEAD -- deskops/ tests/ docs/ …`. **Esperado:** exit 0, «all reviews current», diff protegido vacío, WS45 presente, sin código ni P01–P09 modificados.
