## REFORMULACION

**Propósito:** implementar en `graph_ui` la vista de inbox para leer mensajes, registrar ack y, solo si el contrato WS12 define la operación, respuesta local dentro del mismo desk. **Resultado:** UI en `frontends/mindmap/views/workspace/inbox/` con tests, consumiendo endpoints autorizados por WS12. **Repo:** `graph_ui`. **Límites:** sin envío interdesk; ack no equivale a aprobación; sin tarea implícita ni cron de triage; mutaciones en UI sujetas a gates.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas:** nodo WS25.1; aristas WS12/WS25 y gates; guía de revisión; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`. **Cambios previstos:** vista de inbox y tests dentro del `output_scope`; no se modifica el contrato WS12. **Dependencias:** contrato/endpoints de WS12; `G_WRITE_CONTRACT` por delta; `G_HUMAN_READ`; `G_UI_WRITE` por delta; padre agregado WS25. **Validaciones futuras:** ack persiste tras recarga mostrando el mensaje origen; respuesta local disponible solo si WS12 la define, y si no se declara no disponible; permisos del contrato aplicados; no se crea tarea implícita ni cron de triage.

## FUTURO

WS12 publica el contrato técnico y endpoints, y resuelve `G_WRITE_CONTRACT` por delta. El receptor humano P01 emite el acta `G_UI_WRITE` del delta concreto en `graph_ui`. WS16 produce el acta `G_HUMAN_READ`. El TaskDoc de promoción fija archivos exactos, escenarios de prueba y textos de pantalla. WS25 termina cuando cumplen WS25.1 y WS25.2. Nada de esto lo decide este revisor ni se ejecutó aquí.
