**REFORMULACION**  
Propósito: fijar el paquete de decisiones y contratos que habilita preparar cada delta del workspace documental. Resultado: conjunto integrado —registro P01–P09, matriz UF01–UF10, catálogo de vistas, convención del manual, contrato de navegación/identidad y whitelist de operaciones/escritura— trazable entre sí y contra las auditorías. Repo dueño: `deskops`. Límites: PK02 no ejecuta ni autoriza tareas; es agrupación sin ejecución propia. No implementa, no muta otros repos, no acepta APIs/UI/Scion, no supone edición sin `G_SOURCE` ni convierte gates pendientes en defectos.

**AMBIGUEDADES**  
Ninguna. El encargo define resultado, hijos, orden de transferencia, aceptación y límites; los detalles delegados a promoción o a contratos de hijos no obligan al ejecutor de PK02 a inventar.

**DRY-RUN**  
Lecturas hipotéticas: `decisiones.md`, `owner-decisions.json`, auditorías WS02–WS04 vía WS06/WS07, `cobertura.md`, `dag.yaml` y esta guía.  
Orden/aristas: WS07 tras WS06 → `decisiones.md` y `source_mode`; WS08 tras WS07 → `user-flows.md`; WS10 tras WS02/WS07 → `manual.md`; WS09 tras WS07/WS08/WS10 → `vistas.md`; WS11 tras WS08/WS09 → `navegacion.md`; WS12 tras WS08/WS11 → `operaciones.md`. WS10 y WS08 pueden avanzar en paralelo tras WS07; WS09 consume ambos.  
Integración futura: contrastar que cada Pxx tenga actor/fuente/gates; cada UF, operación/error/nodo/gate; cada vista, origen/contrato/renderer/estado/error; el manual distinga disponible/propuesto/bloqueado; navegación clasifique huecos con productor; operaciones separen comprobado/faltante y precondiciones. Validación integrada: revisión humana contra auditorías y gates, sin ejecutar productos ni mutaciones.

**FUTURO**  
WS06 entrega reconciliación/auditorías base; los hijos de PK02 producen sus borradores y contratos. P01 registra recibos por delta en el repo receptor; WS20 produce `G_SOURCE`; WS45, `G_PAYLOAD_PRECONDITION`; WS40, el corpus del manual. WS16/30/37/39 aportan validaciones humanas. La promoción fijará TaskDoc, archivos y pruebas. Nada de ello se ejecuta aquí.
