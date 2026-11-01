REFORMULACION
Propósito: encargar la implementación de un adaptador público restringido para dispatch en `deskops`. Resultado: dispatch con confirmación, identidad de intento, timeout/errores y autoridad del coordinador, con pruebas. Repo dueño: `deskops`; salidas en `runtime/`, CLI/API fijada por WS12 y `tests/`. Límites: no shell arbitrario, no duplicar transporte; promotion no autorizada; nodo candidato, sin ejecución autorizada. Aceptación: agente real demuestra dispatch aceptado y rechazo/timeout, correlacionado con id de intento WS32.1 y registros WS32.2; `confirmed` solo con respuesta Hub observada.

AMBIGUEDADES
1. «timeout/errores» y «vencido por timeout»: el nodo no fija umbral ni criterio de clasificación, y solo WS34.2 remite «con el umbral del contrato WS12». Obligaría a inventar duración, condición de vencimiento y forma de reportar el error.
2. «un dispatch aceptado y uno rechazado o vencido por timeout»: la conjunción «o» no aclara si basta rechazo o timeout, o si deben probarse ambos. Obligaría a inventar la matriz de aceptación.

DRY-RUN
Lecturas: nodo WS34.1, guía, brief, alcance, decisiones, cobertura y gates; no vecinos. Cambios previstos: adaptador runtime, comando/API y tests. Dependencias: WS33, WS12; gates G_EXEC, G_SCION, G_WRITE_CONTRACT. Validaciones futuras: agente real con aceptación y rechazo/timeout; correlación WS32.1/WS32.2; ausencia de shell arbitrario y transporte duplicado; confirmación solo por respuesta Hub. Sin ejecutar nada.

FUTURO
WS12 produce contrato de operaciones, adapter y autoridad del coordinador. WS44/G_SCION produce probe público de Scion. Un humano resuelve G_EXEC. WS32.1/WS32.2 aportan identidad de intento y registros; WS33 vincula mensajes/resultados. La promoción fijará archivos, pruebas y textos; la recepción técnica por delta se registra en el repo dueño.
