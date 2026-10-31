REFORMULACION

Propósito: validar con una persona el recorrido manual completo —UF02, UF03 edición, UF04, UF05 y UF01 con entradas authored de WS17— sobre el corpus de ejemplo. Resultado: acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/manual/acta.md` y resolución del gate G_HUMAN_MANUAL. Repo dueño: `graph_ui`; `output_scope` coincide con la evidencia del gate. Límites: nodo solo de validación, no implementa; un fallo de guion bloquea el gate y abre tarea en el nodo causante; una observación solo se registra; no declarar “ready” por tests; promoción no autorizada.

AMBIGUEDADES

1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08» — WS08 no figura en `depends_on` ni se suministra su guion. Obligaría a inventar esos escenarios o a asumir un artefacto no disponible. Es una dependencia que falta.

2. «un fallo de guion bloquea el gate y abre tarea en el nodo que lo causó» — no se define canal, actor ni repo para abrir esa tarea, y `output_scope` solo cubre `runs/subagents/workspace-documental-acceptance/manual/`. Obligaría a inventar la operación de creación y su destino, o a exceder el alcance declarado.

DRY-RUN

- Lecturas: nodo WS30 y contratos de vecinos WS17/21/22/23/24/25/26/28/42; gate G_HUMAN_MANUAL; brief, alcance, decisiones, cobertura, validacion-humana, user-flows y guía.
- Cambios previstos: ninguno durante esta revisión. En ejecución futura, acta y evidencia bajo `output_scope`; sin tocar repos ni mutar el desk de desarrollo.
- Dependencias: directas según DAG; transitivas WS40 (corpus), WS16 y gates G_HUMAN_READ/G_WRITE_CONTRACT vía dependientes; WS08 no declarada. Decisiones humanas P04 (source_mode) y P08 (participante) condicionan la ejecución.
- Validaciones futuras: protocolo de validacion-humana, acta versionada con commit verificable, gate G_HUMAN_MANUAL, variante P04 aplicable y prohibición de etiquetar disponible solo por tests.

FUTURO

WS07/humano resuelve P01, P04 y P08; WS08 produce el guion referido; WS40 genera el corpus; WS17 aporta plantillas; WS43 publica navegación real; WS31 redacta el manual. La autorización de promoción y el TaskDoc de WS30 corresponden a un humano, no a este revisor.
