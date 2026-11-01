REFORMULACION

WS14 es un encargo de implementación en graph_ui: integrar una búsqueda navegable en el workspace usando la API real de sldb (`sldb find` o su ruta en `sldb serve`), sin parser propio. Debe producir búsqueda por texto/campos/semántica solo según la API disponible, resultados que abren el documento con identidad y ruta de origen, y tres estados diferenciados —sin resultados, error de backend y degradación parcial—, con flujo de teclado que conserva consulta y foco al volver y sin cargar todo el grafo por tecla. Repo dueño: graph_ui, con salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`; depende de WS13 y G_UI_READ por delta; no duplica la implementación existente y su promoción no está autorizada. No es agregado.

AMBIGUEDADES

ninguna

DRY-RUN

Lecturas: WS03 `auditoria/infraestructura.md`, contrato WS11, salidas de WS13/WS13.1–3, `workspace_routes.py`, `workspace-view.js` y la ruta `GET /find` de sldb. Cambios previstos: cliente de búsqueda y estados en `views/workspace/`, lógica en `frontends/mindmap/source/` y pruebas de peticiones/teclado en `tests/`; sin parser propio. Dependencias y gates: consumo del agregado WS13 y su base WS11; recibo G_UI_READ del delta concreto; capacidad sldb `/find`. Validación: teclear no dispara carga completa del grafo; abrir/volver conserva consulta y foco; tres estados distintos; resultados con identidad/ruta. Errores: si falta contrato, API o recibo, detenerse y registrar hueco con repo dueño; no crear sustituto. Todo hipotético, sin ejecutar.

FUTURO

WS03 entrega la auditoría; WS11 el contrato de navegación; WS13 y sus hijos el lector, explorador e historia/foco; sldb expone `/find`; el receptor humano P01 emite el acta G_UI_READ por delta; la promoción fija TaskDoc, archivos, pruebas y preflight; WS16 valida con humano sobre el corpus WS40 y WS40 produce ese corpus. WS14 alimenta la validación de lectura/búsqueda de WS16.
