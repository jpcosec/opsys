## REFORMULACION
Propósito: implementar en `graph_ui` la captura interna con destino explícito —candidato de drawer o protoátomo— sin exigir tarea. Resultado: captura persistente tras recarga, con origen tipado (ruta o mensaje) visible, permisos y colisiones según el contrato WS12; cada destino se prueba por separado. Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. Límites: no diseñar API/modelo, no asumir el canal de drawer, no crear tarea implícita, no revisar nodos vecinos; WS12 fija representación y operaciones; si falta contrato se detiene y registra hueco.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas: WS25.2, WS12, WS25, gates, guía, brief, alcance, decisiones y cobertura. Cambios previstos: UI de captura en `capture/` y pruebas; uso exclusivo de operaciones autorizadas por WS12; sin tocar API/modelo. Dependencias: contrato WS12; G_WRITE_CONTRACT y G_UI_WRITE por delta; G_HUMAN_READ para uso de mutaciones en UI, sin bloquear desarrollo/pruebas aisladas de API. Validaciones futuras: persistencia tras recarga en drawer y protoátomo; origen ruta/mensaje mostrado; ausencia de tarea; permisos aplicados; colisión no sobrescrita en silencio; prueba separada por destino. Sin ejecutar nada.

## FUTURO
WS12 produce la comparación/canal y la representación de origen; el receptor P01 emite acta por delta para G_UI_WRITE; WS16 produce G_HUMAN_READ. La promoción está no autorizada: el TaskDoc fijará archivos, pills y pruebas. Si falta contrato o canal, se detiene y registra el hueco con repo dueño. WS25 cierra cuando WS25.1 y WS25.2 cumplan su aceptación.
