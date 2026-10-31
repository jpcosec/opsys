## REFORMULACION

- **Propósito**: nodo agregado de implementación para integrar en la UI de `graph_ui` la lectura de inbox con ack/respuesta local y la captura hacia drawer o protoátomo, usando solo operaciones permitidas por el contrato WS12; ack no equivale a aprobación.
- **Resultado**: no ejecutable por sí mismo. Se cumple cuando WS25.1 y WS25.2 cumplen su aceptación; sus salidas agregadas viven en `frontends/mindmap/views/workspace/inbox/` y `.../capture/`.
- **Repo dueño**: `graph_ui`.
- **Límites**: sin envío interdesk, sin tarea implícita ni cron de triage; mutaciones en UI sujetas a G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT, mientras desarrollo y pruebas aisladas de API pueden avanzar. Promoción no autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

- **Lecturas**: nodo WS25, hijos WS25.1/WS25.2, guía de revisión, `alcance.md`, `decisiones.md`, `cobertura.md` y bloque de gates. El bloque edge WS12 no se revisa como contrato vecino; solo se registra como dependencia declarada.
- **Cambios previstos**: ninguno por este revisor; el nodo no se ejecuta. La promoción futura fijaría archivos, pruebas y textos dentro de las rutas de los hijos.
- **Dependencias**: WS12 como contrato de operaciones, más WS25.1 y WS25.2. Los gates están pendientes de forma intencional y se evalúan `per_delta`.
- **Validaciones futuras**: aceptación de ambos hijos; recibo de G_WRITE_CONTRACT y G_UI_WRITE por delta concreto; acta G_HUMAN_READ antes de habilitar uso de mutaciones; recorrido UF02 en WS30.

## FUTURO

- WS12 debe publicar el contrato técnico por operación (canal, campos, errores, pruebas).
- El receptor P01 en `graph_ui` emite el acta de recepción del delta para G_UI_WRITE.
- WS16 produce el acta humana de lectura para G_HUMAN_READ.
- La promoción decide TaskDoc y autorización; WS30 valida el recorrido UF02.
