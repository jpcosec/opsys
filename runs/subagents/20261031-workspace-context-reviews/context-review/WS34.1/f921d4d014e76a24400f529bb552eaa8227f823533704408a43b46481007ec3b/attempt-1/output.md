REFORMULACION
Propósito: encargar un adaptador público restringido para dispatch Scion con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: código en `runtime/`, `cli/commands/runtime.py` o la API que fije WS12, más pruebas. Repo dueño: `deskops`. Límites: no shell arbitrario, no duplicar transporte, ninguna ejecución durante planificación; el dispatch real queda supeditado a gates, y la confirmación solo vale con respuesta observada del Hub, sin inferir éxito o fallo remoto.

AMBIGUEDADES
1. Umbral de timeout. Citas: «timeout/errores» (scope) y «vencido por timeout» (aceptación). El nodo remite a WS12 solo para «Autoridad del coordinador según contrato WS12», no para el plazo. El ejecutor tendría que inventar el valor o criterio de vencimiento para demostrar ese escenario; WS34.2 sí menciona expresamente «con el umbral del contrato WS12».

DRY-RUN
Lecturas: input suministrado —guía, brief, alcance, decisiones, cobertura y nodo WS34.1 con vecinos citados—. Cambios previstos: ninguno en esta revisión; al ejecutarse el nodo, adaptador y tests en `deskops`. Dependencias: WS33, que aporta correlación con WS32.1/WS32.2; WS12, que fija API, autoridad y contrato; gates G_EXEC, G_SCION y G_WRITE_CONTRACT. Validaciones futuras: gates superados; agente real con dispatch aceptado y otro rechazado o vencido; correlación con id de intento local y registros; ausencia de shell arbitrario y de transporte duplicado; confirmación solo por respuesta observada.

FUTURO
WS12 produce el contrato de operaciones y la autoridad; WS44 produce el probe de G_SCION; un humano resuelve G_EXEC; WS32.1/WS32.2 aportan identidad de intento y registros; la promoción fija archivos, pruebas y textos; WS34.2 cubre la respuesta vinculada.
