REFORMULACION
Propósito: encargo de implementación en `graph_ui` para enrutar una tarea en el BoardDoc mediante operación pública y mostrar una capa lista separada por dependencias y solapamiento de archivos. Resultado: vista de routing y pruebas en `frontends/mindmap/views/workspace/routing/`, con Board actualizado y capa lista distinguida de ejecución, dependencias pendientes y solapamientos. Repo dueño: `graph_ui`. Límites: no implementar promoción nueva; invocar solo operación completa admitida por WS12 o dejar handoff/pendiente; no usar heurística optimista; no editar status; no ejecutar commits.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura y nodo WS26.2 con sus vecinos como contratos, sin revisarlos ni ejecutar nada. Cambios previstos: integrar la operación pública de enrutamiento en BoardDoc, representar la capa lista y separar estados; añadir pruebas de routing, dependencias pendientes, igualdad/contención de rutas, glob/no resolución y handoff cuando falte promoción. Dependencias: WS12 aporta contrato de operaciones, canal público, normalización/expansión y promoción admitida; WS22 aporta Board y lifecycle; WS26.1 aporta tarea autorada y contexto. Gates: G_CLOSEOUT ya satisfecho; G_HUMAN_READ pendiente por WS16, intencional, solo habilita uso de mutaciones en UI; G_UI_WRITE y G_WRITE_CONTRACT se evalúan por delta. Validaciones futuras: `deskops show board` tras enrutar, distinción visual/estado en UI, capa lista separada, solapamiento por igualdad o contención de directorio, no comprobado ante glob/no resolución con revisión de supervisor, y handoff pendiente si falta promoción completa.

FUTURO
WS12 produce el contrato de operaciones, canal de promoción y reglas de normalización/expansión; WS26.1 produce la tarea autorada; WS22 produce la representación del Board; WS16 produce el acta humana de lectura para G_HUMAN_READ; el receptor P01 decide y registra G_UI_WRITE por delta; WS12 verifica G_WRITE_CONTRACT por delta. El TaskDoc de promoción fija archivos, escenarios y textos; el supervisor decide los casos no resueltos antes de marcar capa lista.
