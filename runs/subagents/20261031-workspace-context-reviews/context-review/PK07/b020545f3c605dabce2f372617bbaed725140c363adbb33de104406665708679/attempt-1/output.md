REFORMULACION  
PK07 es una agrupación no ejecutable, con repo dueño `deskops`, cuyo resultado sustantivo es dejar dos extensiones independientes —Changes/impacto (WS29) e inspección/edición de modelos (WS39)— con evidencia propia e integración en el lector y el manual, sin convertirlas en prerrequisito del lector/manual básico ni autorizar tareas. Límites: no ejecuta, no añade aristas, no presume CST/Kimun y no repara automáticamente.

AMBIGUEDADES  
ninguna

DRY-RUN  
Un ejecutor futuro no ejecutaría PK07 como tarea: consumiría/ordenaría sus hijos. WS29 usaría salidas de WS15/WS24 (lectura y vecindad) y produciría la vista Changes, pruebas sobre store temporal y evidencia de mutación real, relaciones a 1 hop y hallazgos de check/doctor/drift, enlazando los comandos documentados. WS39 usaría el contrato WS12 y el panel Context de WS13, y produciría el punto de entrada a Schema/editor existente, pruebas UF09, comprobación de errores del contrato y acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md`. No hay arista WS29↔WS39: pueden ir en paralelo o en cualquier orden; no existe artefacto de transferencia entre ambos. La integración consistiría en verificar ambas evidencias y que el manual (WS31) etiquete cada extensión según evidencia. Gates: WS29 `G_UI_READ`; WS39 `G_HUMAN_READ`, `G_UI_WRITE`, `G_WRITE_CONTRACT`. Errores: contrato/API/gate faltante → detener y registrar hueco en repo dueño, sin sustituto; prueba fallida → hijo no completado. Validación esperada: mutación real con documento afectado, relaciones 1 hop y errores; UF09 con inspección/mutación y errores declarados; acta humana; manual sin presumir CST/Kimun.

FUTURO  
WS31 publica el manual; el receptor P01 registra actas por delta; el participante P08 acepta la prueba humana de modelos.
