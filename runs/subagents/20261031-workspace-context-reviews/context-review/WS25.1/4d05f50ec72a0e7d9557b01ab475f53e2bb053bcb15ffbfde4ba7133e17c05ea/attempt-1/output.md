**REFORMULACION**  
Propósito: entregar en `graph_ui` una UI de inbox del workspace para leer mensajes, registrar `ack` y, solo si el contrato WS12 define la operación, responder localmente dentro del mismo desk. Resultado: vista en `frontends/mindmap/views/workspace/inbox/` con tests; `ack` persistente tras recarga y respuesta condicionada o declarada no disponible. Repo: `graph_ui`. Límites: sin envío interdesk; `ack` no equivale a aprobación; no crear tarea implícita ni cron de triage; solo operaciones y permisos autorizados por WS12; promoción no autorizada.

**AMBIGUEDADES**  
ninguna.

**DRY-RUN**  
Lecturas: guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, y fragmentos de `dag.yaml` de WS25.1, WS25, WS12, WS16 y gates. Cambios previstos: ninguno; no se ejecuta nada. Dependencias: WS12 produce contrato/whitelist y gates `G_UI_WRITE` y `G_WRITE_CONTRACT`; WS16 produce `G_HUMAN_READ`. Validaciones futuras: comprobar que el `ack` persiste tras recargar y muestra el mensaje origen; comprobar que la respuesta local solo existe si WS12 la define y, si no, se declara no disponible; aplicar permisos del contrato; verificar ausencia de tarea implícita y cron de triage; ejecutar tests en `tests/`.

**FUTURO**  
WS12 debe producir el contrato, la whitelist y los gates de escritura; WS16 debe producir `G_HUMAN_READ`; el humano debe designar al responsable de `graph_ui` y resolver las decisiones Pxx aplicables; la promoción fijará TaskDoc, archivos, pills y evidencia. Si falta el contrato, el ejecutor se detiene y registra el hueco según `alcance.md`; no lo sustituye.
