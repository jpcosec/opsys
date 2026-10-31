## REFORMULACION

**Propósito:** revisar WS34 como encargo de planificación: nodo agregado que reúne la exposición de un adaptador público restringido para dispatch/reply Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.

**Resultado:** WS34 no se ejecuta; queda cumplido cuando WS34.1 y WS34.2 cumplen su aceptación. Su `output_scope` es agregado de las salidas de ambos hijos.

**Repo dueño:** `deskops`, con `output_base: deskops:repository_root/`.

**Límites:** no shell arbitrario, no duplicar transporte, no enviar mensajes en planificación; requiere `G_EXEC`, `G_SCION` y `G_WRITE_CONTRACT`; promoción no autorizada. No se revisan los bloques edge vecinos.

## AMBIGUEDADES

Ninguna. El nodo es agregado no ejecutable, identifica hijos, dependencias, repo y aceptación comprobable por cierre de hijos. La autoridad del coordinador se remite al contrato WS12 y la confirmación a la respuesta observada de la API Scion; no obliga a inventar resultados ni actores.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (WS34, hijos WS34.1/WS34.2, dependencias WS33/WS12, gates), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y guía de revisión. Ninguna ejecución.

**Cambios previstos:** ninguno sobre el plan en esta revisión. Al cerrar el agregado, registro de que ambos hijos cumplen su aceptación; no se crean sustitutos ni actas.

**Dependencias:** WS33, WS12, WS34.1 y WS34.2; gates `G_EXEC`, `G_SCION`, `G_WRITE_CONTRACT`.

**Validaciones futuras:** aceptación de WS34.1 (dispatch aceptado y rechazado/timeout correlacionados al intento) y WS34.2 (respuesta vinculada al intento correcto y timeout como fallo sin confirmación); contrato WS12 por delta; sonda Scion de WS44.

## FUTURO

WS34.1 y WS34.2 producirán implementación en `runtime/`, CLI/API y pruebas. WS12 fijará el contrato técnico aplicable; WS44 aportará la comprobación pública de Scion. WS36 consumirá solo el adaptador WS34. La autorización de ejecución (`G_EXEC`) y la promoción con TaskDoc corresponden a un humano; no son ambigüedades de este nodo.
