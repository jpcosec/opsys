## REFORMULACION
Propósito: entregar la Entrega M —autoría manual segura y operación (campos, fuente, intake/trabajo, conocimiento) con revisión y cierre por handoff verificable— sobre SLDB/Deskops y graph_ui. Resultado: contrato WS12 aplicado por delta; edición de campos con conflicto y guardas; guardado fuente reversible; captura sin tarea activa; tareas/Board; diff/evidencia; closeout externo; acta WS30 de UF02–05. Repo dueño: deskops; hijos en graph_ui, sldb y deskops. Límites: agrupación sin ejecución propia; no commits automáticos ni closeout HTTP; mutaciones UI solo con gates; fuera de alcance según alcance.md.

## AMBIGUEDADES
1. «Orden parcial obligatorio de ejecución hipotética… WS12→WS47→WS19.1, WS19.2 y WS26.1» y «WS12→WS46→WS25.2». La guía dice que el dry-run sigue las aristas reales de `dag.yaml` y que expresiones como «en orden» no crean secuencia; en los bloques suministrados WS19 depende de WS12/WS19.1/WS19.2, sin arista desde WS47 ni WS46 hacia esos hijos. Obligaría a inventar si WS46/WS47 bloquean realmente a sus consumidores o son solo narrativa.

## DRY-RUN
Ejecutor hipotético, sin ejecutar: promueve hijos en oleadas según prerrequisitos y sin solapamiento de archivos. WS12 entrega `contratos/operaciones.md`; de ahí WS48 (admisión de escritura), WS46 (captura con origen), WS47 (guarda de contenido no declarado), WS19.1/19.2 (campos/conflicto) y WS20 (raw-source/G_SOURCE), con inventario y pruebas en store temporal. WS45 produce inventario y pruebas de precondición; al satisfacerse G_PAYLOAD_PRECONDITION habilita WS19, WS21 y WS26.1. WS21 integra fuente/render tras WS19+WS48; WS25.2 tras WS46; WS26.1→WS26.2 tras WS22+WS12; WS27.1/27.2 tras WS13+WS12; WS42 tras WS19+WS24+WS12+WS48; WS28 tras WS27+WS12+WS48. WS30 consume salidas de WS17/21/22/23/24/25/26/28/42.

Validación esperada: tests de roundtrip/conflicto/protegidos, rechazo observable de precondición obsoleta, ausencia de tarea activa en captura, read-only/handoff con otro coordinador, no peticiones de escritura en procedimiento; WS30 recorre UF02–05 con entradas WS17 y emite acta. Gates por delta: G_WRITE_CONTRACT/G_UI_WRITE, G_SOURCE, G_PAYLOAD_PRECONDITION, G_HUMAN_READ antes de uso UI, G_CLOSEOUT. Si falta contrato/API/dato, detenerse y registrar hueco con repo dueño, sin sustituto.

## FUTURO
Producen otros nodos: WS12 contrato, WS11 navegación, WS13 lector, WS17 índices, WS22 Board, WS24 grafo, WS40 corpus, WS16 acta G_HUMAN_READ, WS20/WS45 gates. Decide un humano: acta WS30 y recepción P01 por delta.
