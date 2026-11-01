REFORMULACION
PK02 es agrupación no ejecutable, en deskops. Propósito: cerrar el paquete de planificación que habilita deltas. Resultado: seis artefactos integrados —registro de decisiones, user-flows, convención del manual, catálogo de vistas, contrato de navegación/identidad y contrato de operaciones/escritura— con Pxx trazadas, cada UF con operaciones/errores/IDs/gates, cada vista con soporte/origen y APIs/huecos con productor. Límites: no implementa UI/API, no crea tareas/aristas, no firma actas, no habilita mutaciones ni Scion, no supone editable sin G_SOURCE. Termina cuando terminan sus hijos.

AMBIGUEDADES
ninguna.

DRY-RUN
Hipotético: WS07 consume WS06 y reutiliza decisiones.md/owner-decisions.json; actualiza registro/baseline solo por cambio real y lo transfiere a WS08, WS10 y por cadena a WS09/WS11/WS12. WS08 produce borradores/user-flows.md (UF01–UF10) para WS09/WS11/WS12. WS10 consume WS02 y WS07; produce borradores/manual.md para WS09. WS08 y WS10 no tienen arista: no se secuencian ni se entregan. WS09 espera ambos y WS07; produce borradores/vistas.md para WS11. WS11 consume WS09/WS08; produce contratos/navegacion.md y mapa de recibos por delta; puede cerrar sin acta. WS12 consume WS11/WS08; produce contratos/operaciones.md con whitelist, efectos, precondición y huecos. Gates: G_PRODUCT en WS08–WS11; G_WRITE_POLICY en WS12. Falta de contrato/API/dato/permiso: registrar hueco con dueño y bloquear solo el delta afectado, sin sustituto. Validación conjunta: trazar Pxx; recorrer UF contra operaciones/errores/nodos/gates; contrastar vistas con fuentes, manual con estados, navegación con identidad/huecos y operaciones con escritores/recibos; verificar que nada promete funciones no disponibles.

FUTURO
WS06 aporta reconciliación; P01/repos receptores emiten actas por delta; WS20 produce G_SOURCE; WS45 G_PAYLOAD_PRECONDITION; WS18 puede obtener G_SPEC_VIEW; WS40 aporta corpus. Aceptaciones humanas de uso quedan fuera de PK02.
