## REFORMULACION
Propósito: revisar WS25.2 como encargo de planificación para una captura interna con destino explícito —candidato de drawer o protoátomo—, sin exigir tarea. Resultado: una captura que persiste tras recargar en el destino elegido, con origen tipado y sin tarea implícita. Repo dueño: `graph_ui`, bajo `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. Límites: no crear API/modelo por reflejo; usar solo operaciones permitidas por WS12; probar cada destino por separado; la colisión con candidato existente no se sobrescribe en silencio y se rige por contrato.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas previstas: esta guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS25.2 y contratos vecinos dados; sin ejecutar comandos ni abrir repos.

Cambios previstos: implementación de UI de captura en `graph_ui`, más pruebas en `tests/`, limitadas al `output_scope`. No se prevé tocar otros repos ni crear endpoints fuera de lo autorizado por WS12.

Dependencias: contrato WS12 para canal, permisos, origen y colisión; gates `G_WRITE_CONTRACT`, `G_UI_WRITE` y `G_HUMAN_READ`; cierre agregado de WS25 cuando sus hijos cumplan. Si falta contrato/API/permiso, aplica la regla común: detenerse y registrar el hueco, sin sustituto.

Validaciones futuras: persistencia tras recarga en drawer y protoátomo por separado; origen ruta y mensaje registrado y mostrado; ausencia de tarea implícita; permisos del contrato; colisión no silenciosa según WS12. Desarrollo y pruebas aisladas pueden avanzar con contratos técnicos; habilitar mutaciones de uso en UI espera `G_HUMAN_READ` y el recibo por delta de `G_UI_WRITE`.

## FUTURO
WS12 debe producir el contrato aplicable y, si falta conducta de workflow, registrar el productor Deskops antes de WS25.2. El receptor P01 produce el acta de recepción por delta en el repo dueño. WS16 produce el acta de `G_HUMAN_READ`. La promoción fijará archivos, escenarios de prueba, textos de pantalla y preflight task-only. La aceptación final y cualquier decisión de habilitar uso corresponden al humano designado, no a este revisor.
