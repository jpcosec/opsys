## REFORMULACION
PK01 es una agrupación no ejecutable de planificación. Su propósito es fijar una base factual y una matriz de deltas verificables para evitar duplicar código: brief/glosario, auditorías de Deskops, persistencia/consultas/notaciones, UI y Scion, y la correspondencia por repo dueño. El resultado sustantivo es el paquete documental formado por `brief.md`, `auditoria/deskops.md`, `auditoria/infraestructura.md`, `auditoria/ui.md`, `auditoria/scion.md` y `reconciliacion.md`, con evidencias actuales y límites explícitos. Repo dueño: `deskops`. Límites: no implementa, no ejecuta probes vivos, no acepta producto, no autoriza tareas, no modifica Boards ni añade aristas.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
PK01 no se ejecuta como unidad: termina cuando terminan sus hijos. Hipotéticamente, WS01 consolida `brief.md` y entrega brief/glosario a WS02–WS05. En paralelo, WS02 lee superficies Deskops y produce `auditoria/deskops.md`; WS03 lee sldb/pron/spec2viz y produce `auditoria/infraestructura.md`; WS04 lee Board/código graph_ui y produce `auditoria/ui.md`; WS05 lee runtime y API pública Scion y produce `auditoria/scion.md`, sin alimentar WS06. WS06 consume solo las auditorías de WS02, WS03 y WS04, contrasta capacidades/deltas con path, símbolo y commit, clasifica ya cubierto/extender ticket/nuevo delta y escribe `reconciliacion.md` con la matriz por repo dueño y la atomización. Cambios previstos: únicamente esos documentos; ninguna implementación, firma ni tarea. Validación integrada: cada auditoría debe distinguir comprobado, ausente y hueco, con dueño; cada fila de la matriz debe tener evidencia, destino y límites, cubrir los deltas sin duplicar código y mantener WS05 separado para E. La completitud no se prueba por hashes/status: exige las salidas de los hijos y la integración descrita.

## FUTURO
El coordinador o humano dispone el gate de comprensión. WS06 deja la matriz para revisión; WS11/WS12 y los receptores P01 producirán contratos y actas por delta; WS05 alimenta el ramal Scion y WS44 aportará el probe. PK01 no acepta producto ni autoriza ejecución.
