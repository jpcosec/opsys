## REFORMULACION
**Propósito:** comprobar acceso público real y read-only a Scion para el ramal E. **Resultado:** `auditoria/scion-probe.md` con respuesta pública, actor del probe, Hub, fecha y capabilities. **Repo:** `deskops`. **Límites:** no crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos; sin registro en `autorizaciones/scion.md` no se ejecuta; si faltan capabilities mapeadas, se detiene y registra el hueco.

## AMBIGUEDADES
1. «Responsable de instalación Scion, designado por solicitante al abordar ramal E»: no se identifica al operador ni quién consta como actor. Aunque `promotion` exige designarlo, ejecutar obligaría a inferir la identidad y el acceso autorizado.
2. «El operador indica el Hub desde la configuración existente»: no define qué hacer si hay varios Hubs o ninguno. Elegir uno obligaría a inventar el criterio de selección.
3. «Puede repetir el probe si el inventario WS05 terminó sin acceso»: no aclara si esa repetición requiere un cambio previo de Hub/API/credencial, en tensión con «Tras cambio de Hub/API/credencial, repetir». Obligaría a inventar la condición de repetición.

## DRY-RUN
**Lecturas previstas:** `dag.yaml` (WS44, WS05, WS07, gates), `auditoria/scion.md` de WS05, `autorizaciones/scion.md` y configuración Scion sin secretos. **Cambios previstos:** solo `auditoria/scion-probe.md`; si falta algo, registrar el hueco sin crear sustituto. **Dependencias:** WS05, G_PRODUCT satisfecho, designación de operador y registro de acceso, Hub y capabilities requeridas por WS32/WS33. **Validaciones futuras:** respuesta pública real read-only; actor, Hub, fecha y capabilities registrados; ausencia de secretos; repetición e invalidación tras cambio; bloqueo si falta API, acceso o mapeo.

## FUTURO
El solicitante designa operador y registra su acceso read-only; WS05 entrega el inventario; WS32/WS33 declaran las capabilities; un humano valida el recibo de G_SCION. Cambios de Hub/API/credencial disparan revalidación. El TaskDoc de promoción fijará archivos y escenarios dentro de esta aceptación.
