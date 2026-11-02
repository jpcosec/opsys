REFORMULACION
Propósito: implementar en graph_ui la lectura segura entre desks de WS11. Resultado: rutas y UI que resuelven aliases de una configuración confiable externa a la petición a `(root, store)`, conservan el par por request sin tocar `SLDB_STORE`, leen el segundo desk de WS40, siguen enlaces authored entre desks y vuelven, muestran identidad/origen y devuelven E-MD1–E-MD4; rechazan roots arbitrarios y paths escapados. Límites: solo lectura; sin federación por copia ni mutaciones cruzadas; los valores de alias/roots son del operador; no amplía sldb ni escribe actas; depende de WS11, WS13, WS40 y G_UI_READ.

AMBIGUEDADES
1. «…volver por la historia». El contrato 5.3/H-12 asigna la historia a WS13.3. Obligaría a inventar si WS41 implementa el «volver» o solo lo integra.
2. «output_scope: frontends/mindmap/source/; rutas de lectura…». El contrato sitúa las rutas en `GU/workspace_routes.py` (GU/=`frontends/mindmap/`), fuera de `source/`. Obligaría a inventar dónde van las rutas nuevas.
3. «La forma JSON sigue la de 7.1 (`{ok:false,error}` + estado HTTP)». No fija el estado de E-MD1–E-MD4. Obligaría a inventar el mapeo error→código.

DRY-RUN
Nodo ejecutable, sin hijos. Lecturas: contrato WS11, DAG WS40/WS13, `GU/workspace_routes.py`, `GU/serve.py`, `GU/deskops_routes.py`, APIs públicas (`open_store`, `doc_status`, `load_edge_index`, `doc_ref`, `parse_links`), corpus/manifiesto WS40. Cambios: cargador y validación de aliases (únicos, `local` reservado, sin duplicados físicos); resolución alias→`(root, store)` por request; rutas del segundo desk; enlaces de texto según 5.2 (pasos 1–9); identidad/origen en respuestas; E-MD1–4 y E5; vista con alias/origen. Dependencias/gates: corpus WS40, lectura WS13.1, historia WS13.3, `include_linked=False`, acta G_UI_READ. Errores: E-MD3 antes de abrir store, sin fallback ni migración. Validación esperada: UF08 sobre dos stores; rechazo de alias/ruta/store; store idéntico antes/después (H-14); `SLDB_STORE` intacto; sin copia.

FUTURO
WS40 produce corpus, manifiesto y enlaces authored; WS13.1/13.3 aportan lectura e historia; el operador suministra la configuración; WS17 aporta plantillas; WS43 publica; WS12 cubre escritura; P01 registra el acta G_UI_READ. La promoción exige changed files/pills/atoms/evidence y preflight task-only: decisión humana. WS18 sigue detenida.
