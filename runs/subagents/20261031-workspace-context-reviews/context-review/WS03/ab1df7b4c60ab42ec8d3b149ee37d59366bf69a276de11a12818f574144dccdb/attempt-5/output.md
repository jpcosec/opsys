## REFORMULACION
**Propósito:** revisar WS03 como encargo de planificación: auditoría de solo lectura sobre persistencia, consultas y notaciones en `sldb/pron/spec2viz`, con Kimun solo como referencia.
**Resultado:** un documento en `deskops:desk/drawer/plans/workspace-documental/auditoria/infraestructura.md`, sin cambios interrepo, que distinga API comprobada, ausencia y hueco.
**Repo dueño:** `deskops`.
**Límites:** no ejecutar, no promover ni modificar otros repos; WS03 depende de WS01 y no sustituye decisiones pendientes.

## AMBIGUEDADES
1. «conflictos y límites de locks»: no identifica qué mecanismo de bloqueo debe auditarse —transacción/DB, archivo, coordinador/CLI u otro— ni qué cuenta como conflicto o límite. Obligaría al ejecutor a inventar el objeto de la auditoría y el criterio para declararlo comprobado, ausente o hueco.

## DRY-RUN
- **Lecturas previstas:** guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS03 y contratos de WS01/WS06; para la ejecución futura, código y documentación de `sldb/pron/spec2viz`, y Kimun solo como referencia.
- **Cambios previstos:** ninguno por este revisor. WS03 produciría únicamente `auditoria/infraestructura.md`; no crearían cambios en repos auditados.
- **Dependencias:** WS01 debe fijar brief y glosario; se requiere acceso de lectura a los tres repos auditados; WS06 consumiría el inventario. Las decisiones P02/P03/P04 no se resuelven aquí.
- **Validaciones futuras:** comprobar que existe una sola salida documental, que no hay cambios interrepo y que el documento separa API comprobada, ausencia y hueco. La promoción sigue no autorizada.

## FUTURO
WS01 produce el brief/glosario; WS06 usa esta auditoría para su matriz; WS07/WS11/WS12 designan responsables y aceptación por repo receptor. Un humano decide P02/P03/P04 y el acceso o revisión concreta de los repos. Nada de ello debe resolverse en esta revisión.
