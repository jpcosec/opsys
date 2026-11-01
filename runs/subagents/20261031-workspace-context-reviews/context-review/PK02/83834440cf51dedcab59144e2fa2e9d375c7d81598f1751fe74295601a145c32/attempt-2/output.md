**REFORMULACION**

PK02 es un paquete no ejecutable: agrupa entregables de planificación que fijan decisiones, user-flows, convención del manual, catálogo de vistas y contratos de navegación y de operaciones/escritura. Su resultado son seis artefactos en deskops: `decisiones.md`, `borradores/user-flows.md`, `borradores/manual.md`, `borradores/vistas.md`, `contratos/navegacion.md` y `contratos/operaciones.md`, con huecos y productores asignados y enlaces a actas externas por delta. Repo dueño: deskops; graph_ui, sldb y spec2viz solo como receptores por delta. Límites: no implementa UI/API, no muta, no autoriza Scion ni dispatch, no aprueba contratos ni asume editable sin G_SOURCE; la recepción técnica es externa y por delta.

**AMBIGUEDADES**

Ninguna.

**DRY-RUN**

Lecturas: `dag.yaml`, brief, alcance, decisiones, cobertura, `reconciliacion.md` (WS06), auditorías WS02–04, `owner-decisions.json`.

Orden por aristas:
1. WS07 (←WS06): verifica P01–P09 con tipo/actor/fuente/nodos/gates; escribe `decisiones.md`; no cambia `baseline_proposal` ni `source_mode` sin decisión nueva. Entrega registro a WS08/10/11/12.
2. WS10 (←WS02,WS07) y WS08 (←WS07), sin arista entre sí: WS10 fija índice, esquema de capítulos, ejemplo futuro Taller y etiquetas de disponibilidad; WS08 fija UF01–UF10 con operación, error, nodo y gate, marcando huecos. Ambos entregan a WS09.
3. WS09 (←WS07,WS10,WS08): cruza auditorías, UFs y estados del manual; escribe filas con origen, contrato o «sin contrato», renderer, acción/dueño, error y estado; no definidos con productor WS11/12. Entrega a WS11 y WS12.
4. WS11 (←WS09,WS08): contrato de identidad, foco, enlaces, historia y multidesk read-only; clasifica huecos y mapa de deltas con recepción. Entrega a WS12.
5. WS12 (←WS11,WS08): whitelist campo/operación/canal/actor/revisión/efectos, adapter existente o hueco, representación de precondición, fallos parciales y closeout fuera de UI. No habilita mutaciones.

Validación integrada: trazar UF→operación→whitelist/hueco; vista→contrato→navegación; Pxx→nodo/gate; todo hueco con productor; etiquetas del manual compatibles con vistas; G_PRODUCT y G_WRITE_POLICY verificados, no ficticios. Errores: falta de WS06 o auditoría → «no comprobado» o parada con dueño; contrato ausente → hueco, nunca sustituto; gate pendiente → bloqueo del hijo. La recepción por delta no bloquea el cierre del paquete.

**FUTURO**

El receptor P01 emite actas por delta en su repo; WS16/30/37/39 y WS40 aportan pruebas y corpus; WS20/WS45 producen G_SOURCE/G_PAYLOAD_PRECONDITION; los nodos de implementación consumen los contratos; el humano decide aceptación de producto.
