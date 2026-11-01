REFORMULACION
WS35 es un nodo de implementación en `graph_ui`: mostrar en el workspace la trazabilidad tarea-intento-conversación-resultados-decisión, anidando mensajes, resultados y decisiones bajo su intento y tarea, con enlace a su fuente y apertura de evidencia en el lector WS13. No debe traducir `completed` como aprobado/cerrado. El resultado vive en `frontends/mindmap/views/workspace/execution/` y `tests/`. Límites: no produce el vínculo de mensajes/resultados (WS33.1), ni diff/evidencia (WS27), ni el lector (WS13); su promoción no está autorizada y el TaskDoc debe fijar archivos, pruebas y textos.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería `dag.yaml#node:WS35`, los contratos de WS33/WS33.1/WS33.2 y WS27/WS27.2, el lector WS13 y las recepciones de G_SCION y G_UI_READ. Crearía componentes de vista y pruebas en el `output_scope`, consumiendo de WS33.1 los mensajes/resultados ya vinculados y deduplicados, de WS33.2 las decisiones, y de WS27.2 la evidencia enlazable. Validaría con tests: anidamiento bajo intento y tarea, enlace a fuente por cada elemento, apertura de evidencia en WS13 y que `completed` no se muestre como aprobado/cerrado. G_SCION está `unverified`: si falta el contrato público de WS44, se registra el hueco con repo dueño y no se crea sustituto. G_UI_READ está `pending` con evaluación `per_delta`: para promover/cerrar WS35 hace falta el acta concreta de WS35; su ausencia no se suple. La promoción exige TaskDoc con archivos, pills, átomos y evidencia precisos.

FUTURO
WS33/WS33.1/WS33.2 deben entregar los datos y vínculos; WS27.2, la evidencia; WS13, el lector; WS44, la prueba de G_SCION; el receptor humano P01, el acta per_delta de G_UI_READ. El TaskDoc de promoción fija los detalles de implementación. WS36 consumirá esta vista para intervención humana.
