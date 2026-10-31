## REFORMULACION
**Propósito:** inventariar la identidad y la API pública de Scion, separando slug/agente/intento/dispatch/mensaje/conversación y permisos, sin contacto vivo. **Resultado:** `auditoria/scion.md`. **Repo dueño:** deskops, leyendo también `../scion`. **Límites:** solo lectura de código, documentación, SDK/endpoints y configuración sin secretos; no crear agentes, enviar mensajes, modificar configuración ni mostrar tokens; no usar tablas internas como interfaz; WS05 no produce `G_SCION`. Depende de WS01.

## AMBIGUEDADES
1. «marca qué capabilities requieren WS32 y WS33». El input no incluye alcance ni aceptación de WS33; el ejecutor tendría que inventar qué necesidades tiene WS33 y qué capabilities marcar.
2. «señalar los campos internos que no figuren en la API pública definida en el scope». El scope dice «API pública de Scion (endpoints/SDK documentados o exportados...)», pero no fija versión ni prevalencia entre documentación y SDK exportado; si discrepan o están incompletos, el ejecutor debe inventar el criterio de qué es interfaz pública.
3. «separar slug/agente/intento/dispatch/mensaje/conversación». El glosario suministrado define “intento”, pero no define slug, dispatch ni conversación; si la API no los etiqueta, el ejecutor tendría que inventar sus equivalencias.

## DRY-RUN
- **Lecturas:** WS01 (`brief.md`, glosario); `runtime/templates/RunDoc` en deskops; documentación/SDK/endpoints públicos de `../scion`; configuración sin secretos.
- **Cambios previstos:** producir/actualizar únicamente `auditoria/scion.md`.
- **Dependencias:** WS01 como prerrequisito; WS44 consume el inventario para el probe y `G_SCION`; WS32/WS33 consumen las marcas de capabilities.
- **Validaciones futuras:** comprobar separación de conceptos y permisos; ausencia de tablas internas como interfaz; campos internos fuera de API pública; capabilities requeridas; no secretos; no cierre de `G_SCION`.

## FUTURO
WS44 ejecuta el probe read-only y satisface `G_SCION`; WS07 designa al operador Scion; WS32/WS33 implementan según el inventario; el TaskDoc de promoción fija archivos, pills y evidencia; el humano resuelve las propuestas Pxx. Nada de eso se decide en esta revisión.
