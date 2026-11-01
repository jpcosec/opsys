## REFORMULACION
**Propósito:** revisar WS32 como encargo de planificación: si se entiende su alcance, resultado, repo dueño y aceptación.
**Resultado:** veredicto de claridad para WS32, nodo agregado no ejecutable.
**Repo:** `deskops`.
**Límites:** no ejecutar nada, no revisar los bloques edge vecinos, no evaluar calidad del producto ni aprobar implementación/API/Scion.

## AMBIGUEDADES
1. **Naturaleza del artefacto a refinar.** El scope dice: «Refinar el ticket de external_references.scion, sin segundo pipeline». Pero `reconciliacion.md` (C-64) afirma: «El destino es un candidato diferido del drawer, no un ticket ni un draft del Board». Eso obligaría al ejecutor a inventar si debe tratar el candidato del drawer como ticket, crear un ticket/Board nuevo o limitarse a refinar el candidato existente; también afecta qué significa su aceptación y promoción.

## DRY-RUN
- **Lecturas previstas:** guía de revisión, `dag.yaml` (WS32, hijos WS32.1/WS32.2, gates), referencia externa `scion`, `reconciliacion.md`, `decisiones.md`, `alcance.md`.
- **Cambios previstos:** ninguno; solo revisión documental.
- **Dependencias observadas:** WS05, WS12, WS32.1, WS32.2; gates `G_CLOSEOUT` satisfecho, `G_SCION` no verificado, `G_WRITE_CONTRACT` pendiente por delta.
- **Validaciones futuras:** comprobar aceptación de ambos hijos; verificar que el agregado termina solo cuando ellos cumplen; confirmar que no se duplica pipeline; revisar `G_SCION` antes de cualquier avance que lo requiera.

## FUTURO
- WS05 produce el inventario de identidad/API Scion.
- WS12 fija el contrato de registro por intento, operaciones y precondiciones.
- WS44 produce la evidencia real de `G_SCION`; WS34/WS37 prueban Hub real bajo `G_EXEC`.
- El receptor P01 emite actas por delta en el repo dueño; un humano designa al operador Scion y autoriza promoción/ejecución.
