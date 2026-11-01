REFORMULACION
Propósito: implementar en `deskops` un adaptador público restringido para dispatch Scion autorizado, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: adaptador en `runtime/` y CLI/API fijada por WS12, con pruebas; un dispatch real aceptado y otro rechazado o vencido, correlacionados con el id local de WS32.1 y registros WS32.2; confirmado solo por respuesta observada del Hub. Repo: `deskops`. Límites: sin shell arbitrario ni transporte duplicado; nodo candidato con promoción no autorizada; requiere WS33/WS12 y G_EXEC/G_SCION/G_WRITE_CONTRACT; no se ejecuta en esta revisión.

AMBIGUEDADES
1. Cita: “con confirmación, identidad de intento, timeout/errores” y “vencido por timeout”. No se fija umbral ni clase de timeout —espera del cliente, falta de ack del Hub o expiración remota— ni se declara que WS12 lo defina. Obliga a inventar cuándo el dispatch está vencido y qué se registra.
2. Cita: “un dispatch aceptado y uno rechazado o vencido por timeout”. La “o” no aclara si basta una negativa o deben probarse rechazo y timeout. Obliga a inventar la matriz de aceptación.
3. Cita: `G_WRITE_CONTRACT` en `requires` frente a “G_SCION/G_EXEC pasan” en `acceptance`. No queda dicho si el cierre exige recibo `per_delta` de G_WRITE_CONTRACT ni quién lo emite. Obliga a inventar la condición de cierre.

DRY-RUN
Lecturas previstas: nodo y `dag.yaml`; contrato WS12; salidas WS33; id WS32.1 y registros WS32.2; probe WS44/G_SCION; autorización G_EXEC. Cambios previstos: adaptador de dispatch en `runtime/`; comando CLI o API que fije WS12; tests de aceptado, rechazo/timeout y correlación. Dependencias: WS33 terminado; contrato WS12 y G_WRITE_CONTRACT por delta; G_EXEC/G_SCION; Hub/agente real autorizado; id local previo. Validaciones futuras: gates; dispatch aceptado y negativa/timeout con agente real; confirmación solo con respuesta observada; correlación con id/registros; no inferir resultado remoto no observado; preflight de promoción/TaskDoc.

FUTURO
WS12 produce contrato técnico de API/operación y autoridad del coordinador; WS44 produce el probe G_SCION; un humano resuelve G_EXEC con permiso explícito; WS32.1/32.2 aportan id y registros; WS33 vincula mensajes/resultados; el TaskDoc de promoción fija archivos, pruebas y textos; el receptor verifica el recibo G_WRITE_CONTRACT por delta. Nada de esto autoriza ejecución.
