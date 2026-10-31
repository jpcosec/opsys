## REFORMULACION
**Propósito:** revisar WS26 como encargo de planificación: agregado que integra autoría desde candidato y contexto de tareas, compuesto por WS26.1 y WS26.2.
**Resultado:** nodo `aggregate` no ejecutable; su aceptación es la de sus hijos. La salida es el agregado de las salidas de WS26.1 y WS26.2.
**Repo:** `graph_ui`, con `output_base: graph_ui:repository_root/`.
**Límites:** no ejecutar; promoción `not_authorized`; no confundir enrutar en Board con ejecución; promoción solo por canal autorizado que respete commits previos y estado real. Depende de WS12, WS22 y sus hijos; requiere G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

## AMBIGUEDADES
Ninguna.

El encargo es legible como agregado: el resultado está definido por sus hijos («Agregado: salidas de WS26.1, WS26.2»), la aceptación remite a ellos («se cumple cuando todos sus hijos cumplen su aceptación»), el repo está presente (`owner_repo: graph_ui`) y los límites excluyen ejecución y promoción no autorizada. Que `depends_on` incluya WS26.1/WS26.2 es coherente con un agregado que termina cuando terminan sus hijos; no obliga a inventar nada. Los gates pendientes son intencionales según la guía.

## DRY-RUN
**Lecturas previstas:** nodo WS26, aristas WS12/W22/WS26.1/WS26.2/WS30 y bloque de gates en `dag.yaml`; guía, brief, alcance, decisiones y cobertura.
**Cambios previstos:** ninguno; esta revisión no modifica archivos ni promueve el nodo.
**Dependencias:** contrato de operaciones de WS12; representación de Board de WS22; aceptación de WS26.1 y WS26.2; gates G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.
**Validaciones futuras:** WS30 sobre UF02/03/04/05; verificación de G_UI_WRITE/G_WRITE_CONTRACT por WS12; G_HUMAN_READ vía WS16; G_CLOSEOUT por resolutor externo.

## FUTURO
WS12 debe producir el contrato de operaciones y la aceptación de deltas en `graph_ui`. WS16 produce G_HUMAN_READ. El resolutor externo de G_CLOSEOUT aporta evidencia de cierre. WS07 y el solicitante humano resuelven P01/P03–P06/P08–P09 y autorizan o no promoción/ejecución. Los hijos WS26.1 y WS26.2 se ejecutan y validan por separado; WS30 integra la aceptación manual. Ningún nodo debe inferir aprobación de gates pendientes.
