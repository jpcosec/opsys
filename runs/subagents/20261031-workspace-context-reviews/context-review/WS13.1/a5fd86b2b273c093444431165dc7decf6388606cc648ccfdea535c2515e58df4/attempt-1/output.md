## REFORMULACION

Encargo: preparar en `graph_ui` un delta de lectura sobre el workspace integrado `a1b2b22` para abrir documento/fuente en solo lectura, mostrar contexto (identidad, relaciones y origen), seguir enlaces y compartir foco por documento entre texto, graph y Code local, incluido Markdown sin modelo. Resultado: implementación o delta conciliado con evidencia de aceptación ampliada, no sustituida por commits previos. Repo dueño: `graph_ui`; alcance en `views/workspace/`, reutilizando workspace existente y rutas de lectura del contrato WS11. Límites: no crear otro workspace, no añadir índices, no inventar mapeo texto→código ni copias por representación; WS11 y WS09 delimitan APIs, seguridad y representaciones soportadas; G_UI_READ es por delta.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor futuro leería primero el contrato WS11, el catálogo WS09, `reconciliacion.md`, `workspace_routes.py`, `workspace-view.js`, `workspace.mjs` y pruebas del workspace. Después comprobaría el recibo externo G_UI_READ del delta concreto.

Cambios previstos, solo dentro de `output_scope`: extender la lectura para obtener Markdown no modelado y su origen; añadir la vista de fuente cruda íntegra junto al render; completar el panel de contexto con identidad, relaciones y ruta de origen; conectar enlaces y selección de foco para que texto, graph y Code actualicen el mismo documento abierto; añadir pruebas. No crearía rutas de store ni índices nuevos.

Dependencias consumidas: WS11 —identidad, foco, enlaces, API/seguridad de no modelados—; WS09 —representaciones declaradas—; base `a1b2b22`; G_UI_READ. Si falta el contrato, la API/dato de lectura o el recibo al cierre, debe detenerse y registrar el hueco con repo dueño, sin sustituto. Validaría con store temporal real: render y fuente íntegra con mismo origen, contexto real, navegación por enlace, foco compartido entre representaciones, apertura sin conocer ID y ausencia de workspace duplicado. Los tests no se ejecutan aquí.

## FUTURO

WS11 decide y documenta contrato/API/seguridad y correspondencia de foco; WS09 declara representaciones soportadas. El receptor P01 en `graph_ui` emite el acta G_UI_READ por este delta. La promoción fija TaskDoc, archivos, pills y preflight. El humano responsable acepta el delta. WS13 solo termina cuando cumplen WS13.1, WS13.2 y WS13.3.
