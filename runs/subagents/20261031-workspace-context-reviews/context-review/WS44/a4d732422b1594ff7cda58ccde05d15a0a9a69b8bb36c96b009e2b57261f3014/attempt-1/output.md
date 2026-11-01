## REFORMULACION

WS44 es un nodo de validación —no agregado— del repo `deskops`: encarga un probe read-only contra la API pública de Scion para satisfacer `G_SCION`. Propósito: comprobar acceso real, identidad del operador, Hub y capabilities necesarias para intento/mensajes de WS32/WS33. Resultado: `auditoria/scion-probe.md` con respuesta pública real, actor, fecha, Hub y capabilities; si API o acceso faltan, queda bloqueado y `G_SCION` sigue `unverified`. Límites: sin crear agentes, enviar mensajes, cambiar configuración ni exponer secretos; no se ejecuta sin registro en `autorizaciones/scion.md`; las capabilities mínimas se toman de `auditoria/scion.md` (WS05) y se detiene si no están mapeadas por nodo.

## AMBIGUEDADES

1. «Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33; si no las mapea por nodo, WS44 se detiene y registra el hueco antes del probe.»  
   Si el inventario mapea solo algunas capabilities, no queda claro si WS44 debe detenerse por completo o probar el subconjunto mapeado y registrar el resto como hueco. Obligaría a inventar el criterio de parada parcial.

2. «puede repetir el probe si el inventario WS05 terminó sin acceso.»  
   WS05 no contacta endpoints por diseño; «sin acceso» no define una condición observable. Obligaría a inventar cuándo procede repetir.

## DRY-RUN

Un ejecutor futuro: comprobaría `G_PRODUCT` satisfecho y WS05/WS07 cerrados; leería `auditoria/scion.md` para extraer capabilities por nodo y `autorizaciones/scion.md` para confirmar operador y acceso read-only; sin registro, se detendría y registraría el hueco sin probe. Leería configuración sin secretos para que el operador indique el Hub. Ejecutaría solo llamadas read-only y volcaría en `auditoria/scion-probe.md` actor, fecha, Hub, endpoint, capabilities y respuestas públicas, redactando secretos. Si API o acceso no están, dejaría `G_SCION` bloqueado y no avanzaría WS32. Cambios previstos: solo ese informe y el recibo del gate. Errores: falta de registro o mapeo, API inaccesible, credencial inválida, fuga de secreto o mutación accidental; todos paran. Validación: respuesta real, identidad, Hub, fecha, endpoint y capabilities, sin secretos; repetir e invalidar recibo ante cambio.

## FUTURO

WS05 produce `auditoria/scion.md` con el mapeo de capabilities; el solicitante designa operador y registra su acceso read-only en `autorizaciones/scion.md`; el operador indica el Hub. Un cambio de Hub/API/credencial obliga a repetir. WS32/WS33 consumen `G_SCION`. La designación y el registro son decisiones humanas pendientes, no ambigüedad del encargo.
