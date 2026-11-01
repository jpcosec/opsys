# Disposición WS27.2, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Evidencia declarada/encontrada/verificada con definiciones, apertura de soporte Markdown en el lector, `deskops closeout verify` como fuente de «verificada», repo graph_ui, depende de WS13 y WS12: coincide.

**Ambigüedades.**

1. «gates/summary se muestran según reporte real». Clase: `futuro asignado`. productor WS12: «WS12 fija correspondencia… y salida pública de closeout verify»; gates y summary son campos de ese reporte.
2. granularidad de «verificada» (por TaskDoc, tipo o evidencia). Clase: `detalle de promoción`. el scope dice «resultado del gate de la TaskDoc/tipo»; cómo se reparte una salida única entre filas lo fija el TaskDoc.
3. «evidencia ausente» frente a «declarada sin artefacto». Clase: `futuro asignado`. productor WS12: la correspondencia por tipo de evidencia declarada define qué evidencia se espera; ausente es la esperada sin declarar, distinta de declarada sin artefacto.
4. «no verificable» frente a «verificación fallida». Clase: `no es ambigüedad`. el scope los separa: «Reporte ausente/fallo de comando es no verificable con error, nunca verificado»; fallida es un resultado del gate.
