## REFORMULACION
Propósito: integrar en `graph_ui` la verificación de closeout, el diagnóstico de faltantes y un handoff explícito con evidencia. Resultado: superficie en `frontends/mindmap/views/workspace/review/`, endpoints y pruebas para ejecutar/consumir `deskops closeout verify` por el canal de WS12, mostrar faltantes y derivar a `deskops closeout commit` por CLI o al coordinador activo. Repo dueño: `graph_ui`. Límites: no commit/close por HTTP, no terminal embebido genérico; el handoff no equivale a cierre. Depende de WS27 y WS12; gates: `G_CLOSEOUT` satisfecho, `G_HUMAN_READ` pendiente y `G_UI_WRITE`/`G_WRITE_CONTRACT` por delta.

## AMBIGUEDADES
Ninguna. El resultado, el repo, los límites y la aceptación quedan acotados; el contrato de operaciones lo produce WS12 y el cierre externo se verifica con `deskops show task` y el commit de closeout. La condición de “coordinador activo” y el canal público quedan dentro de la política de WS12, no de una invención de este nodo. Los textos exactos, archivos y escenarios de prueba corresponden a la promoción/TaskDoc.

## DRY-RUN
Lecturas previstas: `dag.yaml#node:WS28`, guía, brief, alcance, decisiones, cobertura y gates; sin ejecutar comandos. Cambios previstos: UI de revisión, endpoints de consulta/diagnóstico y tests; ningún cambio de contrato ni cierre HTTP. Dependencias: WS27 como agregado de diff/evidencia; WS12 como contrato de canal, actores, errores y efectos; `G_CLOSEOUT` ya satisfecho. Validaciones futuras: acta `G_HUMAN_READ`, recibos por delta de `G_UI_WRITE` y `G_WRITE_CONTRACT`, pruebas aisladas de API y verificación externa de `deskops closeout verify`/`show task`/commit.

## FUTURO
El cierre externo lo ejecuta la CLI en modo manual o el coordinador conforme P03/P05/P06; WS28 solo verifica, diagnostica y entrega el handoff. WS12 debe publicar el canal y la política aplicable; WS27 debe completar sus hijos. La persona designada en P01 produce los recibos por delta. La validación humana de lectura corresponde a WS16 y la aceptación manual completa a WS30.
