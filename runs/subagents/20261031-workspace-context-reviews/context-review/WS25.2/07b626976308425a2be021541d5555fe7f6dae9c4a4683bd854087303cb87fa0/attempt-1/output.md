## REFORMULACION
WS25.2 es un nodo de implementación, no un agregado. Encarga construir en `graph_ui` la captura interna con destino explícito —candidato de drawer o protoátomo— usando solo operaciones autorizadas por el contrato WS12, sin exigir tarea. Resultado: cada destino, probado por separado, persiste tras recargar, conserva un origen tipado (ruta o mensaje) y no crea tarea implícita; aplica permisos del contrato y controla colisiones sin sobrescritura silenciosa. Límites: no crear API ni modelo por reflejo; si falta el canal, detenerse y registrar hueco con dueño; el uso de mutaciones en UI queda tras G_HUMAN_READ.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el contrato WS12, el TaskDoc de promoción y las vistas/endpoints existentes de captura. Verificaría por separado el canal de drawer —composición de API SLDB/DrawerService o wrapper Deskops— y el canal de protoátomo —whitelist o hueco con dueño—. Cambiaría vistas/controladores en `frontends/mindmap/views/workspace/capture/` y pruebas en `tests/`; no tocaría otras rutas. Consumiría G_HUMAN_READ para habilitar uso en UI, G_WRITE_CONTRACT por delta y G_UI_WRITE por recibo concreto. Implementaría primero drawer y probaría persistencia tras recarga, origen mostrado, ausencia de tarea y colisión controlada; después protoátomo, con prueba separada. Si falta contrato, API o permiso, se detendría, registraría el hueco y dejaría la operación no disponible, sin sustituto. Validaría con store temporal real o corpus WS40, recarga de UI y verificación de que no se crea tarea activa.

## FUTURO
WS12 debe publicar el contrato por delta: composición permitida para drawer y canal o hueco para protoátomo. El receptor P01 en `graph_ui` produce el acta G_UI_WRITE del delta concreto; WS16 produce G_HUMAN_READ. La promoción fijará archivos, textos y pruebas en TaskDoc. WS25 cierra cuando WS25.1 y WS25.2 cumplan; WS25.1 cubre mensaje/ack y WS25.2 aporta la captura con origen mensaje. Ningún recibo autoriza Scion, dispatch ni API nueva.
