REFORMULACION
Propósito: comprobar, mediante probe read-only, que existe acceso público real a Scion y verificar identidad, Hub y capabilities necesarias para intento/mensajes. Resultado: `auditoria/scion-probe.md`, base de G_SCION. Repo dueño: deskops. Límites: no crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos; no cerrar G_SCION como `unverified` ni habilitar WS32 sin probe real. Requiere operador designado y acceso read-only registrado.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: WS44 y gates; `auditoria/scion.md` de WS05 para capabilities requeridas por WS32/WS33; registro de decisiones/G_PRODUCT de WS07; `autorizaciones/scion.md`; configuración existente para obtener el Hub sin secretos.

Cambios previstos: crear o actualizar `deskops:desk/drawer/plans/workspace-documental/auditoria/scion-probe.md` con fecha, identidad del operador, Hub, endpoint si la evidencia del gate lo exige, capabilities comprobadas y referencia a respuesta pública real, sin credenciales ni secretos.

Dependencias y gates: consumiría WS05 y el registro G_PRODUCT de WS07. Si falta la designación/registro de acceso read-only, no ejecutaría el probe. Si `auditoria/scion.md` no mapea capabilities por nodo, se detendría y registraría el hueco antes del probe. G_SCION seguiría `unverified` si no hay respuesta real.

Errores y validación esperada: acceso ausente, API inalcanzable, Hub no identificable, capability no comprobada o falta de registro impedirían satisfacer G_SCION; no se avanzaría WS32. La validación exigiría evidencia pública real, actor del probe, Hub, fecha y capabilities; un cambio posterior de Hub/API/credencial invalidaría el recibo previo.

FUTURO
El solicitante humano designa operador y registra su acceso read-only en `autorizaciones/scion.md`; WS05 produce `auditoria/scion.md` con el mapeo de capabilities; el operador aporta el Hub desde configuración. La promoción sigue `not_authorized` hasta designación y confirmación. WS32/WS33 consumirían G_SCION. La detección de cambios de Hub/API/credencial corresponde a operación humana o a otro nodo, no a una invención de WS44.
