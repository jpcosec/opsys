REFORMULACION
Propósito: cerrar el contrato técnico de operaciones y escritura (whitelist por campo/modelo, canal público, permisos, CAS/locks, Git, fallos y closeout externo). Resultado: `contratos/operaciones.md` con capabilities exactas y lagunas registradas. Repo dueño: deskops. Límites: no diseña un adapter inexistente, no implementa WS20, no asume que el lock de UI protege escritores CLI; toda operación sin contrato queda no disponible; autoría/cierre no se etiquetan disponibles sin G_CLOSEOUT.

AMBIGUEDADES
1. «Aceptar deltas de escritura por graph_ui antes de cerrar; aceptar delta en sldb solo si source_mode=editable.» No define la unidad de aceptación: ¿un acta global o una por operación/campo? Tampoco aclara si «delta» abarca todas las operaciones de los `scope_nodes` de G_UI_WRITE o solo las incluidas en la whitelist final. G_UI_WRITE fija la evidencia mínima del acta, no su granularidad. Obligaría a inventar el criterio de cierre y qué actas son exigibles.

DRY-RUN
Lecturas: nodo WS12, guía, brief, alcance, decisiones, cobertura y gates; los bloques edge solo como dependencias, sin revisarlos. Cambios previstos: ninguno; esta revisión no modifica artefactos. Dependencias: WS11 (identidad/navegación), WS08 (UF→operaciones), WS07 (G_WRITE_POLICY, `source_mode` de P04 y responsables de P01), G_CLOSEOUT externo, G_SLDB_WRITE/G_SOURCE vía WS20 y actas de graph_ui/sldb. Validaciones futuras: G_WRITE_POLICY resuelto por humano; whitelist por campo/operación con canal, actor y efectos; coherencia con `source_mode`; clasificación existente/comprobada/faltante; no anunciar capacidades gated; recepción de deltas antes de cerrar.

FUTURO
El humano resuelve P01–P09; WS07 registra `source_mode` y designa responsables; graph_ui y sldb emiten actas; WS20 produce G_SOURCE/G_SLDB_WRITE; G_CLOSEOUT se estabiliza fuera de este nodo; la promoción fija TaskDoc, archivos y pills.
