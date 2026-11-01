# Disposición WS32.1, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. IDs de intento locales distintos antes de dispatch, registro intent/no confirmado por operaciones reales del store temporal, sin red ni Hub simulado, repo deskops, depende de WS05 y WS12: coincide.

**Ambigüedades.**

1. «WS34 y WS37 demostrarán dispatch real… contrato de integración explícito». Clase: `futuro asignado`. trabajo de nodos dependientes: lo demuestran WS34/WS37; el contrato/ubicación del registro por intento lo produce WS12 («WS12 especifica contrato/ubicación del registro por intento»).
2. representación de `confirmed` cuando no hay observación. Clase: `futuro asignado`. productor WS12 (registro por intento); la regla de fondo está dada: «Confirmed = respuesta de la API pública de Scion» y «Registro local intent/no confirmado no afirma fallo/éxito de Hub».
