REFORMULACION
Encargo: nodo de implementación en `graph_ui` para que la persona elija explícitamente el destino de una captura interna —candidato de drawer o protoátomo— y la realice mediante operaciones autorizadas por WS12, sin crear tarea. Resultado: captura persistente tras recarga en el destino elegido, con origen tipado (ruta o mensaje) visible, permisos del contrato aplicados y colisión no silenciosa. Repo dueño: `graph_ui`; alcance: `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. Límites: no crear API/modelo por reflejo, no tarea implícita, no sustituir la capacidad de WS46, no habilitar uso de mutaciones en UI sin G_HUMAN_READ; desarrollo y pruebas aisladas de API pueden avanzar con contratos/gates técnicos.

AMBIGUEDADES
ninguna

DRY-RUN
Un ejecutor leería WS12 (canal, permisos, representación de origen, colisión), WS46 (inventario y pruebas de captura con origen por destino), WS48 (admisión común), el TaskDoc promovido y las vistas/tests existentes. Cambiaría solo `capture/` y `tests/`: control de destino explícito, llamada al endpoint autorizado pasando por la admisión de WS48, origen tipado y su visualización tras recarga, y manejo de colisión. Probaría por separado drawer y protoátomo, con orígenes ruta y mensaje, persistencia, permisos, ausencia de tarea en Board/list tasks y colisión sin sobrescritura. Consumiría G_WRITE_CONTRACT y G_UI_WRITE por delta; G_HUMAN_READ antes de habilitar uso real de la mutación en UI. Si falta contrato, endpoint, capacidad de WS46 o admisión de WS48, se detiene y registra el hueco con repo dueño, sin sustituto. Validación: aceptación UF02 por destino, pruebas en store temporal o corpus WS40, sin ejecutar nada.

FUTURO
WS12 fija contrato, canal, representación y permisos; WS46 produce y prueba la capacidad; WS48 aporta la admisión; WS16 y el humano emiten G_HUMAN_READ; el receptor P01 emite G_UI_WRITE por delta; WS12 emite G_WRITE_CONTRACT; la promoción fija archivos, textos y escenarios; WS25 cierra cuando WS25.1 y WS25.2 cumplen.
