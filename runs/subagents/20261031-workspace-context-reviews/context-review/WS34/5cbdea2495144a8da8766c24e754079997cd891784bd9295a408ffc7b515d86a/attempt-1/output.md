## REFORMULACION

- **Propósito**: encargo de planificación para un adaptador público restringido que exponga dispatch y reply de Scion con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.
- **Resultado**: nodo `aggregate` no ejecutable; se satisface cuando WS34.1 (dispatch) y WS34.2 (respuesta vinculada al intento) cumplen su aceptación. Sus dependientes dependen de WS34.
- **Repo dueño**: `deskops`, con `output_base: deskops:repository_root/` y salidas en `runtime/`, `cli/commands/runtime.py` o API que fije WS12, y `tests/`.
- **Límites**: no shell arbitrario ni duplicar transporte; no enviar mensajes en planificación; `promotion: not_authorized` exige TaskDoc, pills, átomos y evidencia precisos.

## AMBIGUEDADES

Ninguna. Los puntos que podrían parecerlo están cubiertos por fuentes suministradas: «Autoridad del coordinador según contrato WS12» delega en WS12, que registra hueco y dueño; «Confirmación = respuesta de la API de Scion» define el criterio en WS34.1; «la API que fije el contrato WS12» y los textos exactos corresponden a promoción; G_SCION/G_EXEC/G_WRITE_CONTRACT pendientes son intencionales; rutas exactas y archivos los fija el TaskDoc.

## DRY-RUN

- **Lecturas**: guía de revisión, brief, alcance, decisiones, cobertura y bloques `dag.yaml#node:WS34`, hijos WS34.1/WS34.2 y vecinos (contratos, no revisados).
- **Cambios previstos**: ninguno en ejecución; el agregado no produce artefactos propios y `task-ws34.md` se materializaría en promoción.
- **Dependencias**: WS33, WS12 y los hijos WS34.1/WS34.2; gates G_EXEC (external), G_SCION (WS44) y G_WRITE_CONTRACT (WS12).
- **Validaciones futuras**: probe de API pública de WS44, whitelist/capabilities de WS12, autorización humana en `autorizaciones/scion.md`, pruebas con agente real de dispatch aceptado y rechazado/timeout, respuesta vinculada al intento y timeout reportado sin confirmación.

## FUTURO

No es ambigüedad: WS07 registra P01 y designa operador Scion; el humano autoriza G_EXEC; WS44 produce `auditoria/scion-probe.md`; WS12 cierra la whitelist; WS34.1/WS34.2 implementan; la promoción fija archivos, escenarios y textos; WS36 consume solo el adaptador.
