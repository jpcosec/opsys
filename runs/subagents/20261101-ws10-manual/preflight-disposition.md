# Comparación del Supervisor — WS10, aceptada para despacho

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Leí preflight y cold completos. Reproducen objetivo, archivos y límites. Lo que marcan queda fijado aquí; prevalece sobre la TaskDoc donde la precisa.

- Auditorías: WS02 = `auditoria/deskops.md`, WS03 = `auditoria/infraestructura.md`, WS04 = `auditoria/ui.md`, según `output_scope` en `dag.yaml`.
- Los 17 capítulos llevan ficha: Propósito, Entradas, Salidas, Estado, Evidencia. Un capítulo con CLI lleva ficha completa y remite a `docs/operator-manual.md` en Evidencia.
- **Corrección de la TaskDoc.** La precedencia que escribí chocaba con el plan: `manual.md` y WS31 ya fijan «propuesto» para Scion y modelos aunque su dependencia esté identificada. Vale esto: donde `dag.yaml` o el texto existente de `manual.md` fijan una etiqueta, se conserva y se cita, sin importar la precedencia (12 Scion, 15 modelos, la parte avanzada de Changes en 14). En el resto, «bloqueado» si hay dependencia o contrato identificado pendiente y «propuesto» si no. Las definiciones son las de la aceptación.
- Etiqueta por capítulo, referida a las capacidades que describe. Ninguno queda «disponible»: no hay actas.
- Taller: corpus futuro, sin etiqueta. Su ruta y productor los fija el contrato de WS10. **No presentarlos como decisión humana:** P08 solo fija «Taller temporal».
- «Dueño» de un hueco: productor ya citado en el plan (WS31, WS38, WS39, WS29) o nodo del DAG; si no hay, «sin productor en el DAG».
- La palabra «pasos» de la convención existente se conserva: describe el manual futuro. Las fichas no añaden pasos.
- «Revisiones afectadas renovadas» es tarea del Supervisor, no del Executor: PK06, WS10, WS31, WS38.
