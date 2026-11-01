## REFORMULACION
Propósito: precisar los user-flows UF01–UF10 como encargo de planificación, mapeando cada uno a operaciones reales de las auditorías y a nodos/gates del DAG. Resultado: `borradores/user-flows.md` con entrada/salida, operación, error, nodo y gate humano por UF. Repo dueño: `deskops`. Límites: no prometer funciones fuera de alcance; operación ausente se marca hueco; UF08 solo lectura, sin envío interdesk; delegación condicionada a G_SCION/G_EXEC; no ejecutar ni promover.

## AMBIGUEDADES
1. «Cada UF tiene entrada/salida, operación, error, nodo y gate humano». No se define qué significa «entrada/salida»: ¿precondición y resultado observable de la UF, o entradas/salidas de la operación mapeada? Obliga a inventar semántica y formato, y afecta a que la aceptación sea comprobable.
2. «cubrir manual, captura, revisión…». No identifica qué manual ni cómo debe reflejarse: ¿una UF nueva, un campo de las existentes o una referencia? Como `output_scope` solo admite `borradores/user-flows.md`, el ejecutor debe decidir si amplía el catálogo UF o solo mapea el manual a UFs existentes, con riesgo de exceder alcance.

## DRY-RUN
Lecturas previstas: brief, alcance, decisiones, cobertura, validacion-humana, borrador de user-flows, `dag.yaml` (WS08 y vecinos WS07/WS09/WS11/WS12/WS16/WS40, gates). Cambios previstos: solo `borradores/user-flows.md`; completar por UF los campos exigidos y marcar huecos sin inventar operaciones. Dependencias: WS07 para decisiones; auditorías WS02–WS04 vía WS06/WS07; WS12 para confirmar ack local pendiente. Validaciones futuras: UF01–UF10 completas; operaciones citadas; nodos como IDs del DAG; gates WS16/30/37/39 frente a prueba técnica WS29; ninguna promesa fuera de alcance; promoción sigue no autorizada y requiere preflight task-only con archivos/pills/evidencia.

## FUTURO
WS09 usará los UFs para el catálogo de renderizaciones; WS11 para navegación; WS12 para operaciones y ack; WS16/30/37/39 producirán actas humanas y WS29 su prueba técnica. La promoción la decide un humano tras preflight.
