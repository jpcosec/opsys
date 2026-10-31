## REFORMULACION

**Propósito:** comprobar mediante un probe read-only real que la API pública de Scion y el acceso del operador designado permiten las capabilities que WS32/WS33 requieren, y registrar evidencia para G_SCION.

**Resultado:** `auditoria/scion-probe.md` bajo `deskops:desk/drawer/plans/workspace-documental/`, con fecha, Hub, identidad, capabilities y actor, sin secretos.

**Repo dueño:** deskops (artefacto); Scion es el sistema sondeado.

**Límites:** no crear agentes, enviar mensajes, cambiar configuración ni mostrar secretos. Sin registro en WS07 de operador y acceso read-only no se ejecuta. Si `auditoria/scion.md` no mapea capabilities por nodo, se detiene y registra el hueco antes del probe. No cierra `unverified` ni habilita WS32.

## AMBIGUEDADES

1. «verifica capacidades/identidad necesarias para intento y mensajes. Sin crear agentes, enviar mensajes, cambiar config» y «capabilities… registrados»: no se define cómo se comprueba una capability de escritura (dispatch/mensaje) sin ejecutarla —¿endpoint de introspección, catálogo documentado o llamada real?—. Obligaría a inventar el método y podría chocar con el límite de no enviar mensajes.

2. «El operador indica el Hub desde la configuración existente»: no se indica ubicación, formato ni qué hacer si existen varios Hubs. Obligaría a inventar la fuente autoritativa del Hub.

## DRY-RUN

**Lecturas previstas:** `auditoria/scion.md` (WS05), registro de WS07 sobre operador/acceso y `parameters.source_mode`/decisiones, configuración Scion existente sin secretos y API pública documentada o expuesta.

**Cambios previstos:** crear o actualizar `auditoria/scion-probe.md`; ningún cambio en configuración, agentes ni estado Scion.

**Dependencias:** WS05 y WS07; G_PRODUCT; capabilities requeridas por WS32/WS33; acceso read-only registrado por el solicitante.

**Validaciones futuras:** repetir el probe e invalidar el recibo previo tras cambio de Hub/API/credencial; G_SCION solo con respuesta pública real, identidad, Hub, fecha, capabilities y actor; si falta API o acceso, permanecer bloqueada y registrar el hueco.

## FUTURO

- WS07: designa operador Scion, registra su acceso read-only y resuelve P01/G_PRODUCT.
- WS05: entrega `auditoria/scion.md` con capabilities requeridas por WS32/WS33.
- Humano: autoriza la promoción del nodo; WS32 consume G_SCION.
- Eventos externos de Hub/API/credenciales obligan a revalidar.
