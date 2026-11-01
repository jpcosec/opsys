REFORMULACION
Encargo: implementar en graph_ui una vista de lectura que muestre, bajo tarea e intento, mensajes de Scion, resultados y decisiones, cada uno enlazado a su fuente; la evidencia abre en el lector WS13; «completed» no se presenta como aprobado/cerrado. Resultado en `frontends/mindmap/views/workspace/execution/` y `tests/`. Límites: solo lectura; depende de WS33 y WS27; requiere G_SCION y G_UI_READ; promoción no autorizada (el TaskDoc fijará archivos, pruebas y textos).

AMBIGUEDADES
1. «Cada mensaje, resultado y decisión se muestra bajo su intento y tarea» choca con WS33.1: «un mensaje con varios intentos o sin intento resoluble no se vincula y registra la procedencia como hueco». Obliga a inventar si esos mensajes se muestran, dónde y si su falta de intento incumple la aceptación.

DRY-RUN
Un ejecutor leería `task-ws35.md`, los contratos de WS33.1/WS33.2 y WS27.2, las rutas del lector WS13 y las vistas existentes de graph_ui. Crearía componentes en `execution/` y tests. Consumiría registros de WS33.1 (mensaje/resultado con deduplicación y procedencia), evidencia de WS27.2 y la ruta de apertura de WS13. Gates: G_SCION verificado por WS44 y acta G_UI_READ por delta de WS35 emitida por P01/receptor de graph_ui. Si falta, parar y registrar el hueco con repo dueño; operación no disponible. Validaría agrupación por tarea/intento, enlaces a fuente, apertura de evidencia y que «completed» no se pinte como aprobado/cerrado. El caso de mensajes sin intento queda bloqueado por la ambigüedad 1.

FUTURO
WS33.1 produce los vínculos mensaje/resultado; WS33.2 las decisiones; WS27.2 la evidencia; WS13 la ruta de lectura; WS44 el probe de G_SCION; el receptor P01 emite el acta G_UI_READ del delta; la promoción no autorizada fija TaskDoc, archivos y textos; WS36 consume esta vista.
