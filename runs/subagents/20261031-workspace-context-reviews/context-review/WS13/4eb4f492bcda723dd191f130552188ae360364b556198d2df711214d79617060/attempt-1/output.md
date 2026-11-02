REFORMULACION
WS13 es agregado no ejecutable: integra en graph_ui el lector del workspace con historia y foco sobre la base a1b2b22. Resultado: salidas conjuntas de WS13.1 (documento/fuente, contexto, enlaces, foco), WS13.2 (explorador modelados/no modelados) y WS13.3 (pestañas/divisiones/historia). Repo: graph_ui. Límites: solo lectura, sin índices nuevos, sin segundo workspace, rutas del host, registro de vistas existente. Depende de WS11 y de sus hijos; aceptación = la de los hijos.

AMBIGUEDADES
1. «Se reutiliza el registro de vistas existente en shell/registry.js; organización de contenido procede de documentos/consultas.» Ningún hijo incluye shell/registry.js en output_scope ni acepta «organización de contenido»/«consultas»; WS24 sí incluye ese archivo. Fuerza inventar si WS13 exige modificarlo, quién lo hace y qué consulta/organización se valida.
2. «requires: G_UI_READ» con gate per_delta y WS13 en scope_nodes, frente a «Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación.» No se aclara si el recibo del agregado son los de sus hijos o una acta propia; fuerza inventar evidencia para un nodo sin efecto.

DRY-RUN
Sin ejecutar: se leerían WS13, WS11, WS13.1-3, reconciliacion.md y G_UI_READ. WS13 no cambia archivos. WS13.1 produciría lector/foco en views/workspace/; WS13.2, tras WS13.1, explorer/; WS13.3, tras WS13.1, layout/. WS13.2 y WS13.3 no se transfieren entre sí. Cada hijo consume WS11 y su recibo G_UI_READ; si faltan, se detiene y registra el hueco, sin sustituto. Validación conjunta: aceptaciones de los tres hijos, mismo workspace, foco/origen compartidos, sin índice nuevo ni copia; el agregado cierra con ellos. Errores: WS11 ausente, recibo pendiente, base distinta de a1b2b22 (verificar estado real, no asumir hash).

FUTURO
WS11 produce el contrato de navegación; WS09 el catálogo; P01/receptor produce las actas G_UI_READ por delta; la promoción fija TaskDoc y archivos. WS14/15/22/23/24/27/39/41 consumen WS13; WS16 valida humanamente. No es ambigüedad de WS13.
