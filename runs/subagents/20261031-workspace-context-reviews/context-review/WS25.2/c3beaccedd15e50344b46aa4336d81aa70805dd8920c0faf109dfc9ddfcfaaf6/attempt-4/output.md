REFORMULACION
Propósito: permitir captura interna de drawer/protoátomo sin exigir tarea. Resultado: una captura persiste tras recargar, con origen y permisos de contrato aplicados. Repo dueño: graph_ui. Límites: solo operaciones autorizadas por WS12; alcance en `frontends/mindmap/views/workspace/capture/`, endpoints autorizados y `tests/`; promoción no autorizada. No reviso nodos vecinos.

AMBIGUEDADES
1. «Capturar en drawer o protoátomo» / «drawer/protoátomo». No fija si hay que implementar ambos destinos, uno de ellos o una elección del usuario; tampoco qué distingue drawer de protoátomo. Obligaría a inventar el alcance funcional y si la aceptación («una captura persiste») se cumple con cualquiera de los dos.
2. «Origen = ruta o mensaje del que nace la captura.» No aclara si deben soportarse y validarse ambos orígenes o solo uno, ni cómo se representa el origen. Obligaría a inventar el modelo de origen y la matriz de aceptación.

DRY-RUN
Lecturas: nodo WS25.2, guía, brief, alcance, decisiones y cobertura suministrados. Cambios previstos: UI de captura en graph_ui y pruebas en `tests/`; sin ejecutar. Dependencias: contrato WS12 (`G_WRITE_CONTRACT`), validación humana WS16 (`G_HUMAN_READ`) y aceptación de delta `G_UI_WRITE`. Si falta contrato/API/permiso, aplica la regla común: detenerse y registrar hueco. Validaciones futuras: persistencia tras recarga, origen, ausencia de tarea implícita y permisos del contrato.

FUTURO
WS12 produce whitelist, canal y efectos; WS16 produce acta humana; un humano resuelve decisiones y `G_UI_WRITE`; el TaskDoc de promoción fija archivos, escenarios y textos dentro de la aceptación. WS30 figura como gate posterior de UF02.
