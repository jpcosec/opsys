## REFORMULACION

**Propósito:** integrar en el workspace de graph_ui una búsqueda navegable sobre la API real de sldb, sin parser propio.

**Resultado:** búsqueda por texto/campos/semántica solo si la API la ofrece; resultados que abren el documento con identidad y ruta de origen; tres estados distintos —sin resultados, error de backend y degradación por capacidad parcial—; con teclado, buscar, abrir y volver conserva consulta y foco; teclear no debe provocar carga completa del grafo.

**Repo:** `graph_ui`, con `output_scope` en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.

**Límites:** depende de WS13 y, transitivamente, del contrato WS11 y del inventario WS03; requiere G_UI_READ por delta. No se exige debounce ni umbral nuevos: el mecanismo queda para el TaskDoc. No se promete semántica ausente en la API real.

## AMBIGUEDADES

ninguna

## DRY-RUN

Un ejecutor futuro, sin ejecutar ahora, leería `dag.yaml` (WS14, arista WS13, gate G_UI_READ), el contrato WS11, el inventario WS03 y las salidas de WS13. Inspeccionaría `frontends/mindmap/source/`, `views/workspace/` y las rutas reales de `sldb find`/`GET /find`.

Cambios previstos: cliente de búsqueda y estados de UI en `source/` y `views/workspace/`; pruebas en `tests/` que cubran teclado, conservación de consulta/foco, los tres estados y que teclear no dispara una petición de carga completa del grafo. Consumiría las operaciones de búsqueda de sldb ya inventariadas, sin crear parser propio.

Dependencias y gates: WS13 debe entregar el lector con identidad/ruta; G_UI_READ debe tener recibo del delta concreto. Si falta contrato, API o dato, aplicaría la regla común: detenerse, registrar el hueco con repo dueño y no crear sustituto. Validación esperada: recorrido de teclado, distinción visible de estados y comprobación de peticiones; la aceptación humana de lectura corresponde a WS16.

## FUTURO

WS03 aporta el inventario de infraestructura; WS11 fija el contrato de navegación y la forma de abrir resultados; WS13 entrega el lector y sus rutas; WS40 prepara el corpus y WS16 realiza la validación humana. El receptor P01 en graph_ui emite el acta de G_UI_READ para este delta concreto.
