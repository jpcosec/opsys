REFORMULACION
Propósito: implementar en graph_ui la lectura segura entre desks fijada por WS11. Resultado: rutas y proyecciones que resuelven por petición alias→(root,store) desde configuración cerrada, leen el segundo desk, siguen enlaces authored y vuelven por historia, con E-MD1–E-MD4 y sin federación por copia. Repo: graph_ui (`frontends/mindmap/source/`, `views/workspace/`, `tests/`). Límites: solo lectura; no tocar `SLDB_STORE` ni abrir stores por ruta del cliente; sin alias/roots reales; no ampliar sldb; gate `G_UI_READ`; `promotion: not_authorized`.

AMBIGUEDADES
1. «Parámetro con ruta, `..`, ruta absoluta o fuera del criterio 3.3» (E-MD2) choca con «nunca con una ruta ni con un store» (3.2): ninguna petición transporta rutas. Obliga a inventar un parámetro o ruta no previstos, o a probar E-MD2 solo con alias manipulado.
2. «al arrancar o al seleccionar el despliegue» frente a «no hay estado compartido entre peticiones»: no se fija si la configuración es inmutable por proceso ni qué es «seleccionar». Obliga a inventar recarga, invalidación y efecto sobre peticiones en curso.
3. El enlace entre desks se lee «con la lectura protegida de WS13.1/13.2», pero WS41 declara sus propias «rutas de lectura por store»: no se delimita si reutiliza el lector de WS13.1 —¿parametrizado por desk?— o lo duplica. Obliga a inventar la frontera y asumir dos lectores.

DRY-RUN
Lecturas: contrato WS11, nodos WS41/WS40 del dag, manifiesto de WS40, rutas de WS13. Cambios: cargador de configuración cerrada; resolución por request; rutas de lectura con `parse_links`/`split_anchor`, autorización antes de leer y `doc_status(store, "local:"+resto)`; guardias 3.3; mapeo E-MD1–4; alias en URL/estado; tests. Dependencias: WS11 (sintaxis, errores), WS40 (dos desks y manifiesto), WS13 (lectura e historia); gate `G_UI_READ`. Validación futura: arrancar servidor; alias válido lee B y vuelve; alias no autorizado E-MD1; ruta escapada E-MD2; store ausente E-MD3; documento ausente E-MD4; enlaces cruzados; hash/versión del store igual antes/después; `SLDB_STORE` sin cambio. Riesgo: stores WS40 no canónicos y `open_store` migra (H-14) → bloquear, no workaround.

FUTURO
WS40 entrega corpus y manifiesto; WS13.1/13.3, lector protegido e historia; el operador, la configuración real de aliases (H-11); P01/root registra el acta `G_UI_READ`; WS17 aporta plantillas y enlaces authored; si la API pública no sostiene la lectura sin mutaciones, intake en sldb antes de workaround.
