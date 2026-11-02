REFORMULACION
Propósito: ejecutar WS13.1 «Leer documento, contexto y enlaces» en graph_ui. Resultado: delta de solo lectura sobre a1b2b22 con fuente cruda y render del Markdown de mismo origen, panel de contexto (identidad, relaciones, origen), enlaces y foco compartido solo donde WS11 lo declare. Repo graph_ui; scope `frontends/mindmap/views/workspace/` reutilizando `node/workspace-view.js` y componentes, más tests. Límites: sin escritura, índices nuevos, mapeo texto→código ni otro workspace; cierre con recibo externo, no por commits.

AMBIGUEDADES
1. «Identidad = par `(repo, ruta)` donde `repo` es el alias del desk» frente a «Sin configuración confiable no se habilita la lectura cruzada»: los aliases son de WS41 y no existen. Obliga a inventar un placeholder o a mostrar solo la ruta.
2. «seleccionar en Code, texto o graph actualiza ese foco» frente a «no hay mapeo texto→código» (C12): obliga a decidir si una línea Code propaga foco al texto (mapeo inventado) o solo la tarjeta de referencia.
3. «las representaciones que el catálogo WS09 (borradores/vistas.md) y el contrato WS11 declaren soportadas», cuando F17 dice «Estado: bloqueado»: obliga a inventar qué representaciones cuentan como declaradas.
4. «las relaciones que declare el contrato WS11» frente a C8/C9/H-03b (la ruta deduplica y omite el campo): obliga a decidir si el panel incluye procedencia de arista o solo `source`/`target`.

DRY-RUN
Leería contrato y hash, `GU/workspace_routes.py`, `GU/sldb_adapter.py`, `workspace-view.js/.mjs`, `shell/api.js`. Cambios: ruta de fuente propia con guardias 3.3 y una lectura de bytes compartida con IR y revisión; preservar campo y posición de `files`/`references`; exponer metadata de arista con `load_edge_index(include_linked=False)`; cliente con texto por líneas y foco por documento (sección/span, campo, referencia, arista `schema`), sin resaltado texto-código; tests. Dependencias: contrato WS11, base a1b2b22. Gate: G_UI_READ. Errores: E5 y guardias (`no_existe`, `fuera_del_repo`, `protegido`). Validación: revisión de fuente e IR coincidentes; store sin cambios (H-14); sin segundo workspace.

FUTURO
P01 emite el acta G_UI_READ del delta; Tester independiente valida; WS40 aporta corpus, WS41 aliases, WS13.3 clave de sesión; WS12/WS20 habilitan edición.
