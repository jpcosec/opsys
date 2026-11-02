REFORMULACION
Propósito: implementar en la UI la captura con destino elegido explícitamente —candidato de drawer o protoátomo— usando solo operaciones autorizadas por WS12, sin crear tarea. Resultado: cada destino persiste tras recargar con origen tipado (ruta o mensaje), permisos de contrato, sin tarea implícita y con colisión no silenciosa; ambos destinos se prueban por separado. Repo dueño: graph_ui; salida en `frontends/mindmap/views/workspace/capture/`, endpoints que autorice WS12 y `tests/`. Límites: no crear API, modelo ni conducta de workflow; el canal de drawer está pendiente de WS12; no vale declarar la captura no disponible; G_HUMAN_READ solo habilita uso de mutaciones en UI. No es agregado: es un nodo de implementación ejecutable.

AMBIGUEDADES
Ninguna. Las dependencias pendientes tienen productor nombrado —WS12 fija contrato, canal y representación del origen; WS46 prueba o completa la capacidad en deskops; WS48 aporta la admisión de escritura— y el nodo remite a ellas sin exigir al ejecutor inventar sustituto. «Permisos del contrato aplicados» se resuelve con la whitelist WS12. No hay frase que obligue a inventar resultado, aceptación, repo, actor o límite.

DRY-RUN
Lecturas: contrato WS12, inventario/pruebas WS46, API de admisión WS48, vistas de captura existentes y tests de graph_ui.
Cambios previstos: implementar la entrada de captura en el scope, con selector explícito de destino y llamada a la operación autorizada; mostrar el origen; añadir tests por destino con origen ruta y mensaje, persistencia tras recarga, ausencia de tarea y colisión controlada.
Dependencias y gates: consumir WS12, WS46 y WS48; G_WRITE_CONTRACT y G_UI_WRITE por delta; G_HUMAN_READ para habilitar uso, no para pruebas aisladas.
Errores: si falta contrato o capacidad WS46, detenerse y registrar hueco con repo dueño, sin crear sustituto; si falta admisión WS48, lectura/handoff; colisión rechazada sin sobrescribir.
Validación futura: pruebas en store temporal, por destino, con reload y comprobación de origen, ausencia de tarea y colisión; suite de graph_ui sin tocar el desk real.

FUTURO
WS12 publica contrato; WS46 entrega inventario/pruebas o conducta faltante; WS48 entrega admisión; el receptor P01 produce acta G_UI_WRITE por delta; WS16 produce acta G_HUMAN_READ; la promoción fija TaskDoc, archivos y pruebas; los dependientes de WS25 consumen el agregado.
