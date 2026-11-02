REFORMULACION
WS41 implementa en graph_ui la lectura segura entre desks: resuelve aliases/roots autorizados por WS11 y usa APIs públicas de stores, conservando por petición el proyecto/store sin cambiar `SLDB_STORE` global. Resultado: rutas de lectura, lectura del segundo desk y vuelta, y errores visibles (alias no autorizado, path escapado, store ausente). Repo: graph_ui (`frontends/mindmap/source/`, `views/workspace/`, `tests/`). Límites: solo lectura; sin mutaciones cruzadas, federación por copia ni ampliar sldb; depende de WS11, WS13 y WS40; gate `G_UI_READ`; promoción `not_authorized`.

AMBIGUEDADES
1. «Una petición sin alias usa el desk del proceso, y el alias que lo designa se devuelve en la respuesta» (3.2.1), frente al conjunto cerrado del operador y `local` reservado (3.2.2). Obliga a inventar el alias del desk del proceso y si debe figurar en la configuración.
2. «volver por la historia» (acceptance), frente a «cuando WS13.3 la entregue» (5.3) y «historia en WS13.3» (H-12). Obliga a decidir si WS41 implementa el volver o solo conserva el alias para WS13.3.
3. «output_scope: frontends/mindmap/source/» frente a las citas `GU/workspace_routes.py` con `GU/ = ../UIs/graph_ui/frontends/mindmap/` (0). Obliga a inventar si se crea `source/` o se modifican los archivos existentes en la raíz.

DRY-RUN
El ejecutor leería el contrato WS11, los extractos WS41/WS40 y los archivos citados de graph_ui (`workspace_routes.py`, `serve.py`, `deskops_routes.py`, `views/workspace/`, `tests/`). Añadiría configuración cerrada alias→(root,store), resolución por petición sin tocar `SLDB_STORE`, proyecciones con alias/store, composición de enlaces 5.2 (`parse_links`+`split_anchor`+`doc_status(store,"local:"+resto)`), guardias 3.3 y errores E-MD1..4; pruebas contra los dos stores de WS40. Dependencias: WS11 (borrador), WS13, WS40 (candidate), configuración del operador. Gates: `G_UI_READ`, promoción `not_authorized`, preflight. Validación futura: UF08, identidad/origen visibles, enlaces entre desks y vuelta, rechazos y ausencia de mutaciones. Sin ejecutar.

FUTURO
WS11 debe superar Tester independiente y revisión root; WS40 debe generar los dos desks y su manifiesto; WS13.1-3 deben entregar lectura, explorador e historia; WS17 aporta enlaces authored; el operador suministra los aliases; P01/receptor registra el acta `G_UI_READ` y autoriza la promoción.
