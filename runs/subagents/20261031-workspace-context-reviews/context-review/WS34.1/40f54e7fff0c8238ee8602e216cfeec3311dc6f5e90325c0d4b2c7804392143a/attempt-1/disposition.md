# Disposición WS34.1, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Adaptador de dispatch restringido con confirmación solo por respuesta observada del Hub, correlación con WS32.1/WS32.2, sin shell arbitrario, repo deskops, depende de WS33 y WS12: coincide.

**Ambigüedades.**

1. umbral de timeout. Clase: `futuro asignado`. productor WS12 (WS34.2 lo cita: «con el umbral del contrato WS12»; WS34.1 depende de WS12 y su autoridad es «según contrato WS12»). Observación: la aceptación de WS12 no lista el umbral entre sus contenidos; si no lo publica, rige la regla común (detenerse y registrar el hueco). Ver promotion-notes.md.
2. «rechazado o vencido por timeout» (¿ambos?). Clase: `no es ambigüedad`. la frase dice «un dispatch aceptado y uno rechazado o vencido»: basta uno de los dos casos negativos.
