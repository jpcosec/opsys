## REFORMULACION
**Propósito:** agrupar la entrega M (autoría y operación manual) para revisar su coherencia como encargo de planificación, no ejecutarla.
**Resultado sustantivo:** un paquete verificable de autoría manual segura: contrato de operaciones por delta, edición de campos con conflicto, guardado fuente reversible, alternancia fuente/render, captura/triage, autoría y contexto de tareas, diff/evidencia, handoff de cierre y operaciones de conocimiento, integrados y validados humanamente en WS30 (UF02–05 y navegación).
**Repo dueño:** deskops (agrupación); hijos en graph_ui y sldb.
**Límites:** sin ejecución propia ni aristas nuevas; no autoriza tareas; gate solo de comprensión, no completitud sustantiva; uso de mutaciones en UI espera G_HUMAN_READ; guardar no hace commit ni cierre HTTP.

## AMBIGUEDADES
1. «Acta WS30 cubre UF02–05 y navegación» frente a la fuente suministrada del hijo WS30: «Incluye explícitamente UF01». Obliga a inventar si el acta de aceptación debe cubrir UF01 con entradas WS17 o solo UF02–05 más navegación.

## DRY-RUN (hipotético, sin ejecutar)
- **Entradas/orden:** WS12 (contrato/whitelist) alimenta WS19, WS20, WS25, WS27, WS28, WS42. WS19+WS20/G_SOURCE habilitan WS21 editable. WS22+WS12 habilitan WS26. WS13+WS12 habilitan WS27. WS27+WS12 habilitan WS28. WS19+WS24+WS12 habilitan WS42. WS17 y salidas de WS21/22/23/24/25/26/28/42 alimentan WS30.
- **Cambios previstos:** WS19 editores de campos y relaciones con before-image; WS20 API pública de guardado raw-source y tests de roundtrip/conflicto/recuperación/campos protegidos (G_SOURCE/G_SLDB_WRITE); WS21 alternancia fuente/render con buffer; WS25 captura/ack; WS26 autoría y Board; WS27 diff/evidencia; WS28 verificación y handoff de closeout; WS42 split/merge/typing; WS30 acta humana.
- **Dependencias:** G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT, G_SOURCE, G_CLOSEOUT, G_SLDB_WRITE, según hijo y delta.
- **Validaciones futuras:** CAS/conflicto/buffer/protegidos; guardar sin commit; read-only/handoff con coordinador escritor; evidencia declarada/encontrada/verificada distinta; cierre confirmado por `deskops show task` y commit; acta WS30 sobre corpus/entradas WS17.

## FUTURO
Producen otros nodos: WS12 contrato; WS20 G_SOURCE; WS16 G_HUMAN_READ; WS17 entradas; WS22/WS24 prerrequisitos; WS43 publicación real. Decide el humano/receptor P01: actas por delta, G_WRITE_CONTRACT/G_SLDB_WRITE y aceptación de WS30.
