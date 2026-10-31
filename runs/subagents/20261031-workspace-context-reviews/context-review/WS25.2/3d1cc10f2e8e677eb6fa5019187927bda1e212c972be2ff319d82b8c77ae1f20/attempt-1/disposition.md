# Executor comparison — WS25.2, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
- **Propósito**: permitir captura interna en graph_ui con destino elegido explícitamente por la persona: candidato de drawer o protoátomo, usando solo operaciones autorizadas por el contrato WS12 y sin exigir ni crear tarea.
- **Resultado**: cada captura persiste tras recargar en el destino elegido, conserva un origen tipado —ruta o mensaje— y no genera tarea implícita; ambos orígenes se registran y muestran tras recargar.
- **Repo**: graph_ui; salida en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`.
- **Límites**: cada destino se prueba por separado; los permisos del contrato WS12 se aplican; G_HUMAN_READ habilita el uso de mutaciones en UI, pero no bloquea desarrollo ni pruebas aisladas de API con contratos/gates técnicos.

##

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
