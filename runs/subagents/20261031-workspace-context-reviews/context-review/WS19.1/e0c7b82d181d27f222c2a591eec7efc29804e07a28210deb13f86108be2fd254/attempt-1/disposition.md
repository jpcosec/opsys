# Executor comparison — WS19.1, final per-effect contract input

State: accepted_current

## Reformulación examinada

REFORMULACION
- **Propósito:** revisar WS19.1 como encargo de planificación: edición de campos en el workspace, no implementación.
- **Resultado:** delta en graph_ui que edita campos consumiendo endpoints del contrato WS12 sin modificarlo, con revisión CAS y conflicto visible; campos workflow-protected fuera de este canal; mutación limitada a desk en modo manual exclusivo.
- **Repo:** `graph_ui` (`frontends/mindmap/views/workspace/fields/`, `tests/`).
- **Límites:** no ejecutar, no promover, no cambiar contratos ni revisar los bloques edge vecinos; gates pendientes son intencionales.

## Hallazgos/disposición contra intención

Modo exclusivo y autoridad provienen contrato WS12 («policy coordinador», canal/actor/permisos y no lock UI contra CLI) y principio P03. Por tanto UI no inventa señal: sin contrato/garantía comprobada no habilita escritura; lectura/handoff. FUTURO del propio reviewer reconoce WS12 produce política/canal. No falta productor ni permiso nuevo; TaskDoc fija caso y pruebas antes uso.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
