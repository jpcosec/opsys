## REFORMULACION
PK01 es un agregado de planificación, no una tarea ejecutable. Propósito: fijar una base factual y una matriz de deltas verificables para evitar duplicar código. Resultado del paquete: brief/glosario, auditorías de Deskops, infraestructura y UI, inventario Scion y `reconciliacion.md` con correspondencia por repo y delta. Repo dueño: deskops. Límites: no implementa, no acepta producto, no ejecuta probes vivos, no modifica Board/tareas externas, no añade aristas ni autoriza trabajo; el `context_review` es solo comprensión.

## AMBIGUEDADES
Ninguna. Las salidas, dependencias y aceptaciones de cada hijo están delimitadas en `dag.yaml`; la integración queda asignada a WS06 y el inventario Scion separado a WS05.

## DRY-RUN
PK01 no se ejecuta: termina cuando terminan sus hijos. Hipotéticamente:
1. WS01 verifica/consume `brief.md` y glosario, enlaza `decisiones.md` sin editarlo y entrega vocabulario/acuerdos a WS02–WS05. No reescribe si no cambió el encargo.
2. WS02–WS05 corren en paralelo tras WS01. WS02 lee superficies deskops, comandos/modelos y store local; escribe `auditoria/deskops.md` con ubicación, operación y estado comprobado/no comprobado. WS03 lee sldb/pron/spec2viz; escribe `auditoria/infraestructura.md` distinguiendo API comprobada, ausencia y hueco. WS04 lee Board, tareas, código graph_ui y SPEC externo; escribe `auditoria/ui.md` con mapeo por nodo, commit/hash, solapamientos y sesiones. WS05 lee código/documentación de deskops y Scion sin endpoints vivos ni credenciales; escribe `auditoria/scion.md` separando identidad, dispatch, mensaje, conversación y permisos.
3. WS06 consume WS02–WS04 —no WS05— y escribe `reconciliacion.md`: matriz por delta/capacidad y repo dueño, clasificación ya cubierto/extender ticket/nuevo delta, atomización propuesta y límites de evidencia. No firma recibos ni crea gates.

Validación esperada: cada auditoría cumple su aceptación; las citas son archivo:línea, hash/listado read-only o comando de solo lectura; lo ausente se marca con causa. WS06 cubre todos los deltas/nodos aplicables y no presenta recepción ficticia. WS05 se valida por separado y queda para el ramal E. No se comprueban solo hashes/status: se revisa correspondencia sustantiva y ausencia de duplicación. Errores esperados: evidencia inaccesible o store ausente se registran “no comprobado”, sin inventar capacidades.

## FUTURO
WS11/WS12 consumirán la matriz como fuente de contrato; WS32/WS33 consumirán el inventario Scion. El coordinador/humano decidirá disposición y promoción; WS44 hará el probe Scion. Nada de esto autoriza implementación ni aceptación de producto.
