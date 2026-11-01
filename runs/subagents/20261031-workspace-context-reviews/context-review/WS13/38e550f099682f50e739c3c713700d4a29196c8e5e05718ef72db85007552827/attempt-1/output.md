## REFORMULACION
Propósito: integrar en graph_ui el lector del workspace con documento/fuente de solo lectura, contexto, enlaces, Code local, explorador de documentos modelados y no modelados, pestañas/divisiones e historia/foco por documento. Resultado: nodo agregado no ejecutable; se cumple cuando WS13.1, WS13.2 y WS13.3 cumplen su aceptación, y los dependientes siguen dependiendo de WS13. Repo dueño: graph_ui. Límites: delta conciliado sobre a1b2b22, sin otro workspace ni índices nuevos; mantener rutas del host y Code local; reutilizar registro de vistas; promoción no autorizada.

## AMBIGUEDADES
Ninguna. La aceptación del agregado está definida por la aceptación de sus hijos y no asigna ejecución propia; archivos exactos, pruebas y textos quedan en la promoción/TaskDoc.

## DRY-RUN
WS13 no se ejecuta: es agregado. Las lecturas y cambios se reparten entre sus hijos:
- WS13.1 consume WS11 y G_UI_READ; implementa en `views/workspace/` lectura de documento/fuente, contexto, enlaces, Code y foco. Transfiere a WS13.2 y WS13.3 el lector y el modelo de foco.
- WS13.2 consume WS13.1 y WS11; añade `explorer/` y refresco de catálogo. Transfiere la apertura de documentos sin ID a WS13.3.
- WS13.3 consume WS13.1 y WS11; añade `layout/` con pestañas, dos divisiones e historia. Valida abrir/cambiar/cerrar y volver conservando foco.

Validación conjunta: WS13 no tiene acta ni gate propio; cada hijo usa su recibo G_UI_READ `per_delta` y el agregado se declara completo solo con las tres aceptaciones. En promoción debe comprobarse que «Se reutiliza el registro de vistas existente en shell/registry.js» y «organización de contenido procede de documentos/consultas» no exigen trabajo hijo no asignado. Si falta WS11 o el recibo del delta, el hijo se detiene y registra el hueco; no se sustituye.

## FUTURO
WS11 produce el contrato de navegación; el receptor P01 emite actas G_UI_READ por delta; WS09 fija representaciones soportadas; WS40 aporta corpus; WS16 valida lectura humana y WS30 habilita edición. La promoción a TaskDoc y la autorización de implementación las decide un humano.
