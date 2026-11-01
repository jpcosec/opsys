# Disposición WS27.2, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Evidencia declarada/encontrada/verificada con definiciones explícitas, abrir soporte Markdown en el lector, ausencias distintas, reporte ausente = no verificable, repo graph_ui, depende de WS13 y WS12: coincide.

**Ambigüedades.**

1. «declarada/encontrada/gates/summary se muestran según reporte real» (qué son). Clase: `futuro asignado`. productor WS12: «WS12 fija… salida pública de closeout verify»; gates y summary son campos de ese reporte; reporte ausente = no verificable con error.
2. «artefactos resolubles en las references/files» (base de resolución). Clase: `futuro asignado`. productor WS11: output_scope «rutas de lectura definidas por el contrato WS11»; repo/rutas por registry/aliases como en WS27.1.
3. «evidencia ausente» frente a «declarada sin artefacto». Clase: `no es ambigüedad`. definiciones del input: declarada = closeout_evidence, encontrada = artefactos resolubles; ausente es declarada no encontrada, y se distingue de artefacto no declarado y de verificación fallida.
