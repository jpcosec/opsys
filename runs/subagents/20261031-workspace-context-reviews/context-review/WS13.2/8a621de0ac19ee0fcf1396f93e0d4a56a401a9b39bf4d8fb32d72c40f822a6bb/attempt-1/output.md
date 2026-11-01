## REFORMULACION

WS13.2 encarga, en `graph_ui`, un explorador para listar y abrir documentos reales del store y Markdown no modelado del desk sin exigir conocer IDs. Resultado: pieza y rutas bajo `frontends/mindmap/views/workspace/explorer/`, con tests, reutilizando catálogo/filtro para modelados y con API/seguridad de no modelados fijada por WS11. Límites: solo lectura, sin índices nuevos ni otro workspace; las altas deben aparecer tras refresco explícito sin reiniciar servidor ni cambiar código. Depende de WS11 y WS13.1; requiere G_UI_READ por delta.

## AMBIGUEDADES

ninguna

## DRY-RUN

Sin ejecutar: el ejecutor leería el contrato WS11 (`contratos/navegacion.md`), `workspace_routes.py`, `workspace-view.js`, `workspace.mjs` y el catálogo existente; prepararía un store temporal real y un desk de prueba. Cambios previstos: módulo explorador con listado/árbol de modelados y no modelados, selección para abrir, refresco explícito del catálogo/árbol, rutas de lectura de no modelados según WS11, reutilización de `filterCatalog` para modelados y tests en `tests/`. Consumiría el recibo G_UI_READ del delta y el contrato WS11; WS13.1 aporta la base del lector. Si al llegar falta la ruta/API de WS11 para no modelados, se detendría, registraría el hueco con repo dueño en `graph_ui` y dejaría la operación no disponible, sin sustituto. Validación esperada: abrir un modelado y un no modelado sin conocer ID; añadir un documento al store temporal y un Markdown al desk, refrescar y comprobar que ambos aparecen sin reinicio ni cambio de código, sin índices nuevos.

## FUTURO

WS11 produce el contrato de navegación y el receptor P01 emite el acta G_UI_READ del delta concreto. WS13 cierra cuando cumplen WS13.1, WS13.2 y WS13.3. El TaskDoc de promoción fijará archivos exactos y escenarios de prueba.
