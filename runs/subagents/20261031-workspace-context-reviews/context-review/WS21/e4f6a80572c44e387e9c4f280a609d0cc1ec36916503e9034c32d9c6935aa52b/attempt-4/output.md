## REFORMULACION
Propósito: revisar WS21 como encargo de planificación, no como producto ni ejecución. Resultado: dictamen sobre si propósito, resultado, repo dueño, límites, dependencias y aceptación son comprensibles y comprobables. Repo dueño: `graph_ui`, con alcance en `frontends/mindmap/views/workspace/; tests/`. Límites: no revisar bloques edge vecinos, no ejecutar, no convertir propuestas Pxx en decisiones, no juzgar calidad del producto.

## AMBIGUEDADES
1. Contradicción de gates. Cita: «No requiere G_SOURCE si el humano eligió fuente read_only». El nodo base lista `G_SOURCE` en `requires` y la regla de variantes dice que «Una variante añade dependencias y gates a los del nodo base; nunca los quita»; la variante read_only usa `requires: []`. Obligaría a inventar si `G_SOURCE` sigue siendo prerrequisito en read_only.
2. Confirmación de descarte del buffer. Cita: «nunca se descarta sin confirmación». No se define actor, canal ni condición de esa confirmación; obligaría a inventar quién confirma y qué ocurre si no hay confirmación disponible.
3. Estado `pending` dentro de la aceptación. Cita: «Cumplir la aceptación específica de la variante P04», mientras solo existen variantes `editable` y `read_only`. El `scope` dice que con pending no se prepara ni promueve, pero la aceptación no declara resultado verificable para ese valor; obligaría a inventar si el nodo queda no ejecutable o bloqueado.

## DRY-RUN
Lecturas: guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, `dag.yaml` (parameters, nodo WS21, gates, edge WS19/WS20/WS30, solo como contratos). Cambios previstos: ninguno sobre el plan; únicamente el dictamen de revisión. Dependencias observadas: WS19 (agregado), WS12/WS16 transitivas, WS20 solo en editable, gates G_UI_WRITE, G_WRITE_CONTRACT y G_SOURCE. Validaciones futuras: contraste de aceptación con variante elegida, coherencia con `variant_rule`, preflight de promoción limitado a tarea, y verificación de que el manual/WS30 no declaren edición fuente en read_only.

## FUTURO
P04 lo resuelve el solicitante humano o quien designe WS07; WS12 produce contrato y aceptación de mutación; WS20 produce `G_SOURCE` en editable; WS06 aporta la matriz de forma transitiva; el TaskDoc de promoción fija archivos, pills y escenarios; WS30 ejecuta la validación manual; un humano autoriza o rechaza la promoción de WS21.
