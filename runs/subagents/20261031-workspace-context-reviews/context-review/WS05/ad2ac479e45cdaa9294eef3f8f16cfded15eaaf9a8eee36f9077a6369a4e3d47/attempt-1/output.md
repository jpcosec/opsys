## REFORMULACION
- **Propósito:** inventariar la identidad y la API pública de Scion leyendo `runtime/templates/RunDoc` y la API pública.
- **Resultado:** `auditoria/scion.md`, separando slug/agente/intento/dispatch/mensaje/conversación y permisos, y señalando campos internos no expuestos y capacidades que exigen API real.
- **Repo:** `deskops`; salida bajo `desk/drawer/plans/workspace-documental/auditoria/scion.md`.
- **Límites:** sin crear agentes, enviar mensajes ni cambiar config; sin mostrar tokens; sin usar tablas internas como interfaz; no produce G_SCION ni sustituye el probe de WS44.

## AMBIGUEDADES
1. «Puede registrar observaciones de API ya disponibles sin crear un segundo recibo». No define si «ya disponibles» significa documentación/código o un endpoint vivo consultable, ni si WS05 puede usar credenciales existentes para lecturas. Obliga a inventar si se contacta la API o solo se lee fuente, y qué observación es admisible sin convertirse en probe.
2. «Leer runtime/templates/RunDoc y API pública de Scion». No identifica el repo que contiene esos artefactos ni si están en `deskops`; el operador Scion se designa en WS07. Obliga a inventar la ubicación de lectura y si se requiere autorización de acceso.

## DRY-RUN
- **Lecturas previstas:** `brief.md`, `alcance.md`, `decisiones.md`, `dag.yaml` (WS01, WS32, WS44, G_SCION), `runtime/templates/RunDoc` y documentación/API pública de Scion.
- **Cambios previstos:** crear únicamente `auditoria/scion.md`; sin tocar código ni configuración.
- **Dependencias:** entrada de WS01 (brief/glosario); contexto P01/P02 y designación de operador en WS07, que no bloquean el inventario según `decisiones.md`; salida consumida por WS32/WS32.1 y WS44.
- **Validaciones futuras:** comprobar que separa las seis identidades y permisos, no prescribe tablas internas, marca campos internos/capacidades con API real, no expone tokens y no reclama G_SCION. G_SCION solo se satisface con `auditoria/scion-probe.md` de WS44.

## FUTURO
- WS44 ejecuta el probe read-only y produce la evidencia de G_SCION con actor, fecha, Hub y capabilities.
- WS07 designa al operador Scion; un humano resuelve Pxx.
- WS32/WS32.1 usan este inventario para separar intento/dispatch y hacer idempotente el cierre.
