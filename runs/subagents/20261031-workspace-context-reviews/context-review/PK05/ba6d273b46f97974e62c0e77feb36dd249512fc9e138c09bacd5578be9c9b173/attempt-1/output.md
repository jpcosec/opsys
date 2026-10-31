REFORMULACION
Propósito: fijar PK05 como encargo de planificación de autoría manual segura, intake/trabajo y revisión/cierre por handoff verificable, no como producto ni ejecución.
Resultado sustantivo: paquete integrado por el contrato WS12 por delta y las salidas de WS19/20/21/25/26/27/28/42, validado por WS30 con acta humana; debe probar CAS/conflicto/buffer/protegidos, guardar sin commit, read-only/handoff con coordinador escritor, distinción evidencia declarada/encontrada/verificada y cierre confirmado por commit/Deskops. La UI de mutaciones espera G_HUMAN_READ; la API aislada no.
Repo dueño: deskops (plan); implementación en graph_ui/sldb según hijos.
Límites: agrupación no ejecutable, no autoriza tareas ni añade aristas; no ejecutar; no sustituir contratos faltantes; revisión de comprensión ≠ completitud sustantiva.

AMBIGUEDADES
Ninguna. «WS30 integra pruebas humanas con entradas WS17» y «Acta WS30 cubre UF02–05 y navegación» tienen productor/consumidor identificados; lo no fijado (archivos, TaskDoc, textos) queda delegado a promoción y no obliga a inventar en PK05.

DRY-RUN
Lecturas hipotéticas: dag.yaml, contratos WS12/WS11 y salidas de hijos; sin ejecutar.
Orden previsto: WS12 entrega whitelist/matriz por delta. En paralelo, WS19 campos/conflicto, WS20 API fuente/G_SOURCE, WS25 captura, WS26 tareas, WS27 diff/evidencia y WS42 conocimiento; WS21 fuente/render tras WS19 y, en editable, G_SOURCE de WS20. WS28 handoff tras WS27/WS12. WS30 integra con entradas WS17 y salidas de WS21/25/26/28/42, más prerrequisitos WS22/23/24.
Artefactos: contrato→UI; API/tests→WS21; deltas UI→WS30; evidencia→WS28; acta→WS30.
Validaciones futuras: roundtrip/conflicto/protegidos, dos ventanas, buffer conservado, no commit al guardar, read-only/handoff, closeout verify frente a commit y acta UF02–05/navegación.

FUTURO
WS12 produce contrato; WS20/G_SOURCE y WS30/acta; WS17 entradas; WS16/G_HUMAN_READ; humanos aceptan deltas y el TaskDoc fija archivos/pruebas/textos. No son ambigüedad de PK05.
