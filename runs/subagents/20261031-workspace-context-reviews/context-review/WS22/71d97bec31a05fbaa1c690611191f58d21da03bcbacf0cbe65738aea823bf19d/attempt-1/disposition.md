# Disposición WS22, revisión 9, tras la corrección de procedencia

Supervisor Claude Opus 5.5, pane `w3Y:p1`, 2026-10-31. Comparé `output.md` completo de attempt-1 con title, scope, acceptance, depends_on, requires, output_scope, output_base y children del nodo. No hubo agente preparatorio. No leí el bundle completo del intento.

**Fidelidad.** Fiel: propósito, repo dueño, límites y dependencias coinciden con el contrato. El dry-run describe lecturas, cambios, dependencias, errores y validación.

**Ambigüedades.**

1. «tablero agrupado por estado» junto a «estados y condiciones de lifecycle leídos de deskops (Board, lifecycle)». No fija qué campo o conjunto de estad… Clase: `detalle de promoción`. Las columnas vienen de los estados de deskops; el campo exacto lo fija el TaskDoc con WS09.
2. `output_scope: frontends/mindmap/views/workspace/board/; tests/` frente a «selección y links comunes con lector». Si la selección y los enlaces comune… Clase: `detalle de promoción`. El ejecutor consume selección y enlaces del lector WS13; si exigiera tocar el lector, hueco. Anotado para promoción.
3. «no duplicar tareas» no aclara si prohíbe crear tareas desde esta vista, repetir una misma tarea en varias representaciones o duplicar datos; obliga a… Clase: `no es ambigüedad`. En contexto prohíbe duplicar el dato de tarea: el Board sigue siendo la fuente.

**Disposición.** Aceptada, sin cambio de contrato.
