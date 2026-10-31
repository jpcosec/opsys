## REFORMULACION

**Objetivo:** consolidar el ajuste canónico del plan `workspace-documental` tras WS06, dejando `brief.md`, `dag.yaml`, `reconciliacion.md` y `canonical-adjustments.md` coherentes con la evidencia y con los puntos A–F de `review-source.md`, sin implementar producto ni aceptar deltas.

**Alcance:** solo planificación en `deskops`. Archivos permitidos: los cuatro citados, proyecciones generadas por `build_plan.py` y `render_diagram.py` —incluidas fichas en `desk/drawer/tasks/workspace-documental/`— y helpers locales solo si resultan imprescindibles. Se aplican A (C-50), B (C-41 y WS45), C (C-55), D (C-64), E (coherencia) y F (orden y validación). Fuera de alcance: WS07, WS08–12, WS05, código, auditorías, reapertura de cierres, P01–P09, repos hermanos, Scion, frontends/workspace y push.

**Repo:** `deskops`. El Executor edita y puede regenerar proyecciones; no ejecuta `context_review.py run` ni commitea. El Supervisor congela, revisa, registra disposiciones, commitea y cierra.

**Límites:** `execution_authorized` sigue `false`; estado final `final_plan_reviewed`. Ninguna primitiva nueva se implementa: WS45 y el eventual productor Deskops quedan planificados. Las tareas futuras asignadas —WS45, comparación de contrato en WS12, productor Deskops condicional antes de WS25.2, re-reviews y Tester— no son lagunas del encargo.

## AMBIGUEDADES

1. «Helpers locales del plan solo si son imprescindibles, nunca debilitando un validador». No define qué vuelve «imprescindible» un helper ni su superficie máxima. Obligaría a inventar criterios de admisión y límites de edición. Mitigación: no crear helpers salvo que una validación existente lo exija demostrablemente.
2. «re-review barato de todos los inputs y contratos afectados y de todos los nodos nuevos y agrupadores». «Agrupadores» no enumera qué nodos cuentan ni si los 25 iniciales pueden ampliarse. Obligaría a fijar por juicio el conjunto exacto de revisiones. Mitigación: derivar la lista de `dag.yaml`, contratos modificados y nodos nuevos, y registrarla antes de ejecutar.
3. «Consumidores conectados por efecto real o gate técnico explícito, sin bloquear al lector». No identifica qué aristas concretas deben añadirse o conservarse para WS45, WS20, WS19, WS21 y WS12. Obligaría a inventar dependencias. Mitigación: justificar cada arista desde la matriz y el contrato WS12.

## DRY-RUN

Leería: `review-source.md`, esta TaskDoc, `canonical-adjustments.md`, `brief.md`, `dag.yaml`, `reconciliacion.md`, `decisiones.md`, rituales y pills enlazadas. Contrastaría A–F con las filas C-41, C-50, C-55 y C-64.

Entregable: ediciones acotadas en los cuatro archivos; WS45 con owner, prerrequisitos, entregable, aceptación y review real; glosario C-41; C-50 sin portabilidad genérica; C-55 como canal permitido; C-64 sin recepción ficticia; `runs/subagents/20261031-ajuste-canonico-ws06/result-summary.md` con antes/después.

Después correría, sin ejecutar ahora: `build_plan.py --check` (esperado inicialmente fallo por proyecciones obsoletas; luego 0), `validate_plan.py --check` (esperado inicialmente FAIL por revisiones obsoletas; tras re-reviews, 0), `context_review.py status` (esperado inicialmente `stale`; finalmente «all reviews current»), y el `git diff --name-only` indicado (esperado vacío fuera de superficies permitidas). El Tester independiente produciría `tester-result-summary.md` con PASS.
