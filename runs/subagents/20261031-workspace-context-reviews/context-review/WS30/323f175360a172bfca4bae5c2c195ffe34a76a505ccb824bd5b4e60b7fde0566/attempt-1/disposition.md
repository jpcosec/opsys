# Disposición WS30, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Acta humana de autoría/revisión (UF01 con entradas WS17, UF02/03/04/05) en graph_ui, un fallo bloquea el gate, incidente si la causa no está aislada, depende de WS17, WS21–WS26, WS28, WS42: coincide.

**Ambigüedades.**

1. «escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08» (WS08 no está en depends_on). Clase: `futuro asignado`. productor WS08 (guion/user-flows); WS08 es ancestro transitivo de WS30 (WS08→WS11→WS12→WS19→…) y validacion-humana.md cita «conflicto en dos ventanas». Observación: «navegación por teclado» no aparece en validacion-humana.md; WS08 debe incluirla (ver promotion-notes.md).
2. «supervisor receptor autorice diagnóstico». Clase: `futuro asignado`. actor nombrado: el supervisor del repo receptor; la autorización es previa a atribuir nodo, no es trabajo del ejecutor.
3. «paths/hashes» (¿plantillas WS17 o materialización WS40?). Clase: `detalle de promoción`. la aceptación dice «plantillas/entradas WS17 validadas, paths/hashes»: son los de las entradas WS17; si se añade el del corpus materializado lo fija el TaskDoc.
