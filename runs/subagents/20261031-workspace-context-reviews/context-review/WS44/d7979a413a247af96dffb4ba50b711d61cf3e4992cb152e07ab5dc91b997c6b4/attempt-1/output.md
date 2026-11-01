REFORMULACION
Propósito: comprobar o revalidar acceso público real a Scion y satisfacer G_SCION mediante un probe read-only, registrando identidad del operador, Hub, fecha y capabilities requeridas por WS32/WS33. Resultado: `auditoria/scion-probe.md` como recibo verificable o registro de bloqueo/hueco. Repo dueño: deskops. Límites: no crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos; G_PRODUCT no autoriza Scion; si falta acceso, API o mapeo de capabilities, no se cierra como verificado ni se habilita WS32.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería la evidencia de G_PRODUCT vía WS07, `auditoria/scion.md` de WS05, `autorizaciones/scion.md` y la configuración existente sin secretos. Comprobaría que el solicitante designó operador y acceso read-only; si no, se detiene. Extraería de WS05 las capabilities requeridas por WS32/WS33; si no están mapeadas por nodo, registraría el hueco en `auditoria/scion-probe.md` y no probaría. Si están, identificaría el Hub indicado y ejecutaría un probe read-only a la API pública: identidad del actor, Hub, fecha, endpoint y capabilities, sin mutaciones. Escribiría el recibo en `auditoria/scion-probe.md`, sin secretos. Validaría G_SCION solo con respuesta pública real y datos registrados; si API o acceso fallan, dejaría WS44 bloqueada y no avanzaría WS32. Ante cambio de Hub/API/credencial, repetiría e invalidaría el recibo anterior. Errores esperados: falta de registro, Hub no resoluble, capability no mapeada, API inaccesible o respuesta no pública; todos se registran como bloqueo, no como éxito. No ejecuto nada.

FUTURO
El solicitante designa operador y registra el acceso read-only; WS05 entrega el inventario; WS32/WS33 consumen las capabilities y quedan bloqueados hasta el recibo; el receptor humano valida el acta/recibo. No es ambigüedad de este nodo.
