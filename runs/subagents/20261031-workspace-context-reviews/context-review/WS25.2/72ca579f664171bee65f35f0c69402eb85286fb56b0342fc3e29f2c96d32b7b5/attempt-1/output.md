REFORMULACION
Propósito: encargar la captura interna del workspace con destino explícito a candidato de drawer o protoátomo, sin crear tarea. Resultado: capturas persistidas tras recarga, con origen tipado —ruta o mensaje— visible y permisos del contrato aplicados; cada destino se prueba. Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/capture/`, `tests/` y endpoints autorizados por WS12. Límites: solo operaciones del contrato WS12; nada de tarea implícita; no revisar vecinos ni ejecutar.

AMBIGUEDADES
1. «destino elegido explícitamente por la persona usuaria» no se refleja en «una captura persiste tras recargar con origen...». Falta criterio para comprobar la elección explícita o rechazar un destino por defecto; obligaría a inventar cómo se evidencia y si un default cumple.
2. «cada destino se prueba por separado» no se concreta en la aceptación, que habla de «una captura». Obligaría a inventar si drawer y protoátomo deben pasar ambos persistencia/origen tras recarga o si basta uno, y qué resultado distinto se espera.

DRY-RUN
Lecturas futuras: contrato WS12, acta/G_HUMAN_READ de WS16, código y tests actuales de captura, TaskDoc de promoción. Cambios previstos: UI de captura y tests; sin backend fuera de endpoints autorizados ni creación de tareas. Dependencias: WS12 (G_UI_WRITE, G_WRITE_CONTRACT) y WS16 (G_HUMAN_READ); si falta contrato/dato, detenerse y registrar hueco. Validaciones futuras: recarga con origen ruta/mensaje visible, ausencia de tarea, permisos y prueba separada por destino; no ejecutadas.

FUTURO
WS12 produce whitelist/contrato y evidencias de gates; WS16 produce aprobación humana; el solicitante/WS07 resuelve decisiones y designa responsables; el TaskDoc fija archivos, escenarios y textos. WS25 cierra cuando ambos hijos cumplen. Nada de esto es ambigüedad de este nodo.
