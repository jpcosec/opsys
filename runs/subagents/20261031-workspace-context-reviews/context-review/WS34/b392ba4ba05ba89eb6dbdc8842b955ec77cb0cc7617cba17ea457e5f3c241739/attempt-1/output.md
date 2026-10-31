## REFORMULACION
**Propósito:** revisar WS34 como encargo de planificación: nodo agregado que expone un adaptador público restringido de dispatch/reply Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.
**Resultado:** un veredicto de revisión, no código ni ejecución. WS34 se satisface cuando WS34.1 y WS34.2 cumplen su aceptación.
**Repo dueño:** `deskops` (`owner_repo: deskops`; `output_base: deskops:repository_root/`).
**Límites:** depende de WS33, WS12, WS34.1 y WS34.2; requiere `G_EXEC`, `G_SCION`, `G_WRITE_CONTRACT`; sin shell arbitrario ni duplicar transporte; sin mandar mensajes en planificación.

## AMBIGUEDADES
Ninguna. Los elementos que podrían parecer huecos están cubiertos por fuentes suministradas:
- La autoridad del coordinador se delega explícitamente: «Autoridad del coordinador según contrato WS12».
- El contrato de operaciones tiene productor: WS12 (`G_WRITE_CONTRACT`, `produced_by: WS12`).
- La accesibilidad de Scion tiene productor: «resolver: WS44 por operador Scion designado en WS07».
- La aceptación del agregado es comprobable por composición: «se cumple cuando todos sus hijos cumplen su aceptación».
- Archivos, rutas finas y pruebas concretas quedan para promoción/TaskDoc, excluido por guía.

## DRY-RUN
**Lecturas (sin ejecutar):** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`; nodos WS34, WS33, WS12, WS34.1, WS34.2, WS36 y gates `G_EXEC`, `G_SCION`, `G_WRITE_CONTRACT`.
**Cambios previstos:** ninguno en repo, DAG ni tareas; solo el informe de revisión.
**Dependencias:** WS12 debe cerrar contrato y `G_WRITE_CONTRACT`; WS33 debe vincular mensajes/resultados/decisiones; WS34.1 y WS34.2 deben cumplir aceptación; gates pendientes son intencionales.
**Validaciones futuras:** aceptación de WS34.1 (dispatch aceptado y rechazado/timeout con agente real) y WS34.2 (reply vinculado al intento y timeout reportado como fallo); ambas condicionadas por `G_EXEC`/`G_SCION`.

## FUTURO
- WS44 produce el probe real de Scion (`auditoria/scion-probe.md`) que satisface `G_SCION`.
- WS12 produce whitelist/canal/efectos y `G_WRITE_CONTRACT`.
- WS07 designa operador Scion y responsables de repo.
- Un humano resuelve `G_EXEC` mediante autorización explícita.
- La promoción fijará archivos, tests y textos exactos dentro de la aceptación.
- WS36 consumirá únicamente el adaptador WS34.
