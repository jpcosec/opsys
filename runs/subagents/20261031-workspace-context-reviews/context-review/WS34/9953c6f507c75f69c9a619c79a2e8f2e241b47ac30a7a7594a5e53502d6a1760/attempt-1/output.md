## REFORMULACION

Propósito: dejar escrito un encargo de planificación para un adaptador público restringido de dispatch/reply Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: WS34 es un agregado no ejecutable; su cumplimiento es la suma de WS34.1 (dispatch) y WS34.2 (reply), con salidas en `runtime/`, CLI/API y tests. Repo dueño: `deskops`. Límites: no habilita ejecución ni mensajes reales; exige G_EXEC, G_SCION y G_WRITE_CONTRACT; no duplica transporte ni admite shell arbitrario; `promotion: not_authorized`.

## AMBIGUEDADES

Ninguna.

El alcance del agregado queda cerrado por su aceptación («se cumple cuando todos sus hijos cumplen su aceptación») y por la guía: un `aggregate` no se ejecuta. La confirmación («respuesta de la API de Scion») y la autoridad («según contrato WS12») están delegadas a hijos o a dependencias con productor nombrado. Los gates pendientes son intencionales y no defectos.

## DRY-RUN

Lecturas previstas: guía de revisión, brief, alcance, decisiones, cobertura, nodo WS34 y contratos vecinos (WS33, WS12, WS34.1, WS34.2, WS36, gates). Cambios previstos: ninguno; es nodo agregado y no se ejecuta. Dependencias: WS33 y WS12 como prerrequisitos; WS34.1 y WS34.2 como hijos que materializan el resultado; gates G_EXEC, G_SCION y G_WRITE_CONTRACT. Validaciones futuras: aceptación de ambos hijos, contrato WS12 por delta, evidencia de dispatch aceptado/rechazado o timeout y reply vinculado al intento. Nada de esto se ejecuta aquí.

## FUTURO

WS34.1 y WS34.2 producirán el adaptador y sus pruebas; WS12 fijará el contrato de operaciones; WS44 aportará el probe de G_SCION; el humano resolverá G_EXEC. WS36 consumirá únicamente este adaptador. La promoción y el TaskDoc fijarán archivos, escenarios y textos dentro de la aceptación, sin autorizar ejecución.
