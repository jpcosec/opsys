REFORMULACION
Revisar WS20 como encargo de planificación: comprobar si propósito, resultado, repo dueño, límites, dependencias y aceptación se entienden sin inventar. Resultado: ambigüedades y dry-run, no dictamen de producto. Repo dueño: `sldb`. Límites: no ejecutar, no revisar contratos vecinos, no resolver Pxx, no promover ni autorizar código.

AMBIGUEDADES
1. «Si falta: intake/tarea sldb propia y roundtrip, conflicto y recuperación reales antes de cerrar G_SOURCE.» No queda claro si WS20 debe implementar la capacidad faltante o solo abrir intake/tarea. Obligaría a inventar el resultado y si el cierre exige código o solo handoff.
2. «Si capacidad existe: evidencia de contrato suficiente, no código duplicado.» “Suficiente” no es comprobable y contrasta con G_SOURCE: «API pública y tests roundtrip/conflicto/campos protegidos». Obligaría a inventar qué evidencia basta y si la rama “existe” también exige esas pruebas.
3. «roundtrip, conflicto y recuperación reales» no define escenarios, resultados esperados ni criterio de recuperación. Obligaría a inventar casos y umbrales de aceptación.
4. «guardado fuente reversible» no concreta qué reversibilidad se prueba (¿roundtrip, conflicto, deshacer?). Obligaría a inventar el criterio; P04 solo dice «API reversible probada».

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura y fragmentos de `dag.yaml` (parámetro, nodo, gate). Cambios previstos: ninguno; es revisión de solo lectura. Dependencias: WS12 precede a WS20; `G_SLDB_WRITE` y `G_WRITE_CONTRACT` están pendientes; `source_mode: pending` y WS20 solo se habilita con `editable`. Validaciones futuras: evidencia de gates, criterio de “capacidad existe”, pruebas de G_SOURCE y coherencia con P04.

FUTURO
WS12 produce contrato y gates; WS07/P04 y P01 requieren decisión humana sobre `source_mode` y responsable `sldb`; la promoción de WS20 y la elección implementar frente a intake corresponden a un nodo o humano posterior. No son ambigüedades de este input.
