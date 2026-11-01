REFORMULACION
WS30 es un nodo de validación humana en graph_ui: una persona recorre en el ejemplo Taller UF01 con entradas WS17 materializadas por WS40, UF02, UF03 edición, UF04 y UF05, incluidos errores, conflicto en dos ventanas y teclado. Resultado: acta humana en runs/subagents/workspace-documental-acceptance/manual/ que enumera plantillas/entradas WS17 validadas, paths/hashes y recorridos, y satisface G_HUMAN_MANUAL. Límites: no implementa, no corrige otros repos, no declara ready por tests, no ejecuta cierre ni publicación; un fallo bloquea el gate; promoción no autorizada.

AMBIGUEDADES
1. «los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md». WS08 no está en depends_on ni se indica qué hacer si falta su guion; el ejecutor tendría que encontrarlo fuera del DAG o inventar escenarios de teclado/error.
2. «Acta enumera plantillas/entradas WS17 validadas, paths/hashes y recorridos, para que WS43 pueda trazar publicación real». No se precisa si los paths/hashes corresponden a las plantillas versionadas en deskops:ejemplo/nav/ o a los destinos temporales materializados por WS40; elegir uno obliga a inventar la correspondencia que WS43 necesitará.

DRY-RUN
Un ejecutor futuro leería task-ws30.md, validacion-humana.md, el guion de WS08, plantillas WS17, manifiesto/corpus WS40 y contratos WS12. Prepararía Taller, recorrería el guion con la persona, provocaría conflicto en dos ventanas y comprobaría UF01/02/03/04/05, teclado y errores. Consumiría WS17+WS40, WS21, WS22, WS23, WS24, WS25, WS26, WS28 y WS42. Cambio previsto: crear y commitear el acta en graph_ui bajo output_scope; no tocar código ni otros repos. Validaría que el acta enumera paths/hashes y recorridos, que un fallo bloquea G_HUMAN_MANUAL y que una observación solo se registra; si falta un contrato/API/dato de una dependencia, se detendría y registraría el hueco. Si la causa no se aísla, registraría incidente sin atribuir nodo.

FUTURO
La persona participante decide y firma el acta; G_HUMAN_MANUAL queda resuelto por WS30. WS43 contrastará el acta para trazar la publicación real y WS31 la usará para el manual. El responsable del repo causante o el supervisor autorizará tareas de corrección; WS30 no las ejecuta.
