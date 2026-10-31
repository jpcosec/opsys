## REFORMULACION
**Propósito:** comprobar mediante un probe read-only que la API pública de Scion es accesible con el acceso ya autorizado y verificar capacidades e identidad necesarias para intento y mensajes. **Resultado:** `auditoria/scion-probe.md` con respuesta pública real, operador, Hub, fecha y capabilities. **Repo:** `deskops`. **Límites:** sin crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos; sin registro de acceso read-only en WS07 no se ejecuta; si faltan capabilities mapeadas, se detiene y registra el hueco.

## AMBIGUEDADES
1. «verifica capacidades/identidad necesarias para intento y mensajes. Sin crear agentes, enviar mensajes, cambiar config» — no se define cómo comprobar de forma read-only la capacidad de mensajes si enviar mensajes está prohibido. Obligaría a inventar si basta con consultar un endpoint de capacidades, documentación o un listado, y qué respuesta cuenta como prueba.
2. «El operador indica el Hub desde la configuración existente» — no se identifica qué configuración ni quién la localiza/registra. Obligaría a inventar la ruta/fuente del Hub y si WS05 debe dejarlo inventariado o si el operador lo aporta por conocimiento propio.
3. «Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33; si no las mapea por nodo, WS44 se detiene» — no queda claro si un mapeo parcial también detiene el probe o si basta con las capabilities que sí aparezcan. Obligaría a decidir entre bloquear todo o probar un subconjunto.

## DRY-RUN
**Lecturas previstas:** `auditoria/scion.md` de WS05, registro P01/acceso read-only de WS07, `dag.yaml`/gates y configuración Scion sin secretos. **Cambios previstos:** crear `auditoria/scion-probe.md`; registrar recibo de G_SCION si hay respuesta real. **Dependencias:** WS05, WS07 y G_PRODUCT; capabilities marcadas por WS32/WS33 en el inventario. **Validaciones futuras:** respuesta pública real, identidad del operador, Hub, fecha, capabilities y ausencia de secretos; si falta API/acceso, dejar WS44 bloqueada y no avanzar WS32. No se ejecuta nada.

## FUTURO
WS07 debe designar operador Scion y registrar su acceso read-only; WS05 debe mapear capabilities por nodo; el solicitante confirma P01 y el acceso. WS32/WS33 consumirán G_SCION. La repetición tras cambio de Hub/API/credencial y la invalidación del recibo corresponden a operación humana/WS07, no a este revisor.
