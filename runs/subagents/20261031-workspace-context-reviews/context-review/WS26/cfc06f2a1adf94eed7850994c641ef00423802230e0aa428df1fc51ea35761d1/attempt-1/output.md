REFORMULACION
WS26 es un nodo `aggregate` no ejecutable, con repo dueño `graph_ui`. Su propósito es integrar autoría explícita desde candidato, evidencia, dependencias, contexto/pills, enrutamiento en Board y representación de capa lista, sin confundir ruta de Board con ejecución. El resultado es el agregado de WS26.1 y WS26.2: «Agregado: salidas de WS26.1, WS26.2». Límites: no define contrato ni canal propios; la promoción solo procede cuando el contrato resuelve commits previos por canal autorizado, y depende de WS12, WS22 y sus hijos, además de los gates declarados.

AMBIGUEDADES
Ninguna. La aceptación del agregado es comprobable por composición: «se cumple cuando todos sus hijos cumplen su aceptación». El alcance remite el contrato de promoción a WS12 y el estado de commits a `G_CLOSEOUT`; no obliga a inventar resultados, actores ni límites para este nodo.

DRY-RUN
Lecturas: guía de revisión, brief, alcance, decisiones, cobertura y fragmentos de `dag.yaml` de WS26 y sus dependencias. Cambios previstos: ninguno; esta revisión no modifica el plan ni ejecuta código. Dependencias: WS12 aporta contrato de operaciones/escritura; WS22 aporta representación de Board; WS26.1 y WS26.2 producen las salidas agregadas. Gates: `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`. Validaciones futuras: aceptación de ambos hijos, satisfacción de gates y validación humana de WS30; no se ejecutan aquí.

FUTURO
WS12 debe producir el contrato/whitelist y el canal autorizado; WS26.1 y WS26.2 deben implementar y evidenciar sus aceptaciones; WS22 debe entregar la representación de Board; WS30 valida el recorrido humano. WS07 y el actor humano resuelven Pxx y gates; `G_CLOSEOUT` depende del cierre externo. Nada de eso se presume aprobado en esta revisión.
