REFORMULACION
PK04 es un agregado de revisión, no ejecutable: agrupa entregables authored y representaciones navegables sobre identidad común. Busca que lista/tablero/dependencias, procedimiento y conocimiento abran los mismos documentos/soportes sin escribir estado ni marcar pasos por lectura, y que los índices sigan sus fuentes. Resultado: salidas de WS17, WS18, WS22, WS23 y WS24 más su integración; no es producto entregado. Repo dueño: deskops; hijos en deskops, graph_ui y spec2viz. Límites: no ejecuta, no crea tareas/aristas, no autoriza mutaciones; WS18 es opcional y no bloquea WS24; esta revisión solo comprueba comprensión.

AMBIGUEDADES
ninguna.

DRY-RUN
Agregado no ejecutable: termina cuando terminan sus hijos. El DAG no fija orden entre hermanos; solo productores compartidos. WS22/23/24 avanzan en paralelo tras WS13 y WS09: WS22 produce vista Board y pruebas; WS23 vista de procedimiento y pruebas; WS24 conocimiento/grafo, registro y pruebas. No se pasan artefactos; integran en lector/UI. WS17, tras WS11/WS40, produce ejemplo/nav/ y regenera corpus; no entrega a los demás. WS18, tras WS09/WS11 y G_SPEC_VIEW, produce ViewDoc/NotationDoc y pruebas en spec2viz; opcional. Validación conjunta: regenerar WS40 con WS17, comprobar que no duplica el registry real y que cada plantilla resuelve roots/aliases; abrir el mismo TaskDoc desde lista, tablero y dependencias; abrir documentos/transiciones de procedimiento sin auto-marcar ni escribir; comprobar backlinks, clasificación y vecindad de 2 hops; verificar ausencia de escrituras. Si una plantilla no resuelve, corregir la fuente, no el destino; si falta campo/API de WS09/11/13, detenerse y registrar el hueco; sin G_SPEC_VIEW, WS18 no se ejecuta y el resto puede completarse. WS18 se valida aparte comparando su selección con WS09/WS11 vía graph_ui y store real.

FUTURO
WS11 entrega contrato de navegación; WS09 catálogo; WS13 lector; WS40 corpus; WS03 auditoría para WS24. G_UI_READ habilita hijos; G_SPEC_VIEW decide WS18 por delta. Supervisores de graph_ui/spec2viz promueven y reciben sus tareas; P01/receptor humano acepta deltas. WS16/WS30 validan lectura/edición según cobertura.
