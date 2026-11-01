REFORMULACION
Encargo: declarar proyecciones de grafo reutilizables en spec2viz mediante ViewDoc y NotationDoc concretos para selecciones y notación ya soportadas, tomando como fuente el catálogo WS09 y el contrato WS11. Resultado: ViewDoc/NotationDoc evaluados con `evaluate_view` y las rutas `/api/views` existentes de graph_ui sobre un store real, con selección coincidente y documentada, más pruebas. Repo dueño: spec2viz (`sldb/views/` y `tests/`). Límites: no portabilidad genérica, servicio/CLI/runtime fuera de graph_ui, extracción o compartición del evaluador, UI declarativa ficticia, ni invención de selección; si WS09 no fija selección mínima, detener promoción y corregir el contrato. Depende de WS09 y WS11; requiere G_SPEC_VIEW; promoción no autorizada; deskops no escribe en spec2viz.

AMBIGUEDADES
1. «Selecciones concretas y notación requerida vienen de catálogo WS09 y contrato WS11» y «si catálogo no fija selección mínima, detener promoción… No inventar selección aquí». La regla de parada cubre la selección, pero no qué hacer si WS09/WS11 no fijan la notación requerida. El ejecutor tendría que inventar qué NotationDoc crear o decidir una parada no prevista, ya que «notación ya soportada por spec2viz» puede admitir varias.

DRY-RUN
Hipotéticamente: leer catálogo WS09, contrato WS11, capacidades WS03 y filas C-37/C-49 de reconciliación; confirmar al promover ruta, registro y TaskDoc. Crear en spec2viz los ViewDoc/NotationDoc y sus tests; consumir el evaluador y las rutas `/api/views` sin modificarlos; usar store temporal real o corpus WS40. G_SPEC_VIEW exige recibo per_delta antes de promover/ejecutar; sin él no hay aceptación. Si falta selección mínima o notación requerida, detener y registrar el hueco sin sustituto. Validar evaluando la selección, comparándola con WS09/WS11, documentándola en el ViewDoc y ejecutando pruebas; no alegar portabilidad por probar dos stores.

FUTURO
WS09/WS11 producen catálogo y contrato; P01/receptor del repo emite el recibo G_SPEC_VIEW por delta; el supervisor/Executor de spec2viz promueve la TaskDoc, fija archivos y pruebas, ejecuta y recibe el delta. WS24 y el manual no esperan este ViewDoc opcional.
