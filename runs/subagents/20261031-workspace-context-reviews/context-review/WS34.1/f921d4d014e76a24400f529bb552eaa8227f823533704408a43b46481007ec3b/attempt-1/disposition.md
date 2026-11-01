# Disposición WS34.1, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Adaptador de dispatch restringido con confirmación solo por respuesta observada del Hub, correlación con el id de intento WS32.1 y registros WS32.2, sin shell arbitrario, repo deskops, depende de WS33 y WS12: coincide.

**Ambigüedades.**

1. umbral de timeout («vencido por timeout»). Clase: `futuro asignado`. productor WS12 (WS34.2 lo cita: «con el umbral del contrato WS12»; WS34.1 depende de WS12); además la aceptación admite «un dispatch aceptado y uno rechazado o vencido», así que no exige demostrar el timeout. Hueco de coordinación: la aceptación de WS12 no menciona el umbral (ver promotion-notes.md).
