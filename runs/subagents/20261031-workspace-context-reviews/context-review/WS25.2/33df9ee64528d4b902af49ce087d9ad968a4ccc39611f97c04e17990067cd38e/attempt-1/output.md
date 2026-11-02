REFORMULACION

Propósito: habilitar en la UI una captura interna cuyo destino elige explícitamente la persona —candidato de drawer o protoátomo— usando solo operaciones permitidas por el contrato WS12 y sin exigir ni crear tarea.

Resultado: pieza de captura en graph_ui y pruebas que demuestran, por cada destino, persistencia tras recarga, origen tipado (ruta o mensaje) visible, ausencia de tarea implícita, permisos aplicados y colisión controlada sin sobrescritura silenciosa.

Repo dueño: graph_ui, con salidas en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`.

Límites: no crear API ni modelo por reflejo; el canal de drawer está pendiente de WS12 y su capacidad probada la aporta WS46; toda escritura pasa por la admisión de WS48; G_HUMAN_READ solo habilita el uso de mutaciones en UI; el nodo es candidato y su promoción no está autorizada.

AMBIGUEDADES

Ninguna.

DRY-RUN

Lecturas: contrato WS12 (canal de drawer/protoátomo, permisos, representación del origen, colisiones), inventario y pruebas de WS46, módulo de admisión de WS48, y este nodo con su aceptación.

Cambios previstos: módulo/vistas de captura dentro de `output_scope`, llamadas a los endpoints que autorice WS12, y pruebas separadas para drawer y protoátomo.

Dependencias: WS12 define canal y representación del origen; WS46 entrega la capacidad probada de captura con origen para cada destino; WS48 debe consultarse antes de invocar la escritura.

Validaciones futuras: con store temporal, comprobar por destino persistencia tras recarga, origen ruta y mensaje registrado y mostrado, ninguna tarea activa creada, colisión rechazada sin sobrescribir y permisos del contrato aplicados. Verificar G_WRITE_CONTRACT y G_UI_WRITE por delta concreto; G_HUMAN_READ antes de habilitar la UI.

Errores esperados: si falta el canal de WS12 o la capacidad de WS46, detenerse y registrar el hueco sin crear sustituto; si WS48 no admite la escritura, no habilitar la mutación y ofrecer lectura/handoff.

FUTURO

WS12 produce el contrato aplicable; WS46 prueba o completa la captura con origen; WS48 produce la admisión común. El receptor humano P01 emite el acta G_UI_WRITE del delta; WS16 produce G_HUMAN_READ; WS30 decide la aceptación UF02. La promoción autoriza el TaskDoc con archivos y pruebas concretas. WS25 agregará el resultado al completarse sus hijos.
