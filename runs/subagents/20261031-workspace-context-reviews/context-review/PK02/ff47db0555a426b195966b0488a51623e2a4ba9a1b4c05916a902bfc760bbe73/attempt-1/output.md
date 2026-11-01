REFORMULACION
Propósito: consolidar el paquete de planificación que fija decisiones, user-flows, catálogo de vistas, convención del manual y contratos de navegación/operaciones, para preparar cada delta sin implementarlo. Resultado: salidas hijas coherentes y trazables (`decisiones.md`, `user-flows.md`, `vistas.md`, `manual.md`, `navegacion.md`, `operaciones.md`) con Pxx, UFs, vistas, APIs, huecos, productores y gates; PK02 no produce entregable propio ni ejecuta. Repo dueño: deskops. Límites: agrupación sin ejecución; no autoriza tareas, no aprueba API/UI/Scion, no crea actas interrepo, no implementa producto. Aceptación: trazabilidad y coherencia documental, sin confundir revisión de comprensión con producto entregado.

AMBIGUEDADES
ninguna

DRY-RUN
Hipotético, sin ejecutar. Lecturas: WS07 lee WS06 y `decisiones.md`/`owner-decisions.json`; WS08 lee WS07 y auditorías transitivas; WS10 lee WS02/WS07; WS09 lee WS07/WS08/WS10; WS11 lee WS09/WS08; WS12 lee WS11/WS08. Cambios previstos, solo documentales: WS07 actualiza decisiones/baseline/source_mode; WS08 redacta user-flows; WS10 manual; WS09 vistas; WS11 navegación y enlaces; WS12 operaciones. Orden: WS07→WS08→WS10→WS09→WS11→WS12, respetando WS10 tras WS07 y WS09 tras WS08/WS10. Integración: matriz de trazabilidad Pxx→UF→vista→manual→navegación→operaciones; verificar IDs/gates, estados disponible/propuesto/bloqueado, productores de huecos y que G_SOURCE no se suponga. Validación futura: revisión documental y muestreo de filas; no pruebas de producto ni actas. La recepción técnica por delta queda al receptor P01/repo dueño.

FUTURO
WS20 produce G_SOURCE; WS45 G_PAYLOAD_PRECONDITION; P01 y repos receptores producen actas por delta; WS16/30/37/39 son gates humanos; WS40 genera el corpus Taller y WS43 publica entradas reales. PK02 termina cuando cierran sus hijos; no ejecuta implementación ni recepción.
