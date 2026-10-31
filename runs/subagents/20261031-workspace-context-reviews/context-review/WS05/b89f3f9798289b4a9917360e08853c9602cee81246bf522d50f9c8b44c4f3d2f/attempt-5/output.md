REFORMULACION
- Propósito: inventariar la identidad y la API pública de Scion para separar slug, agente, intento, dispatch, mensaje, conversación y permisos.
- Resultado: `auditoria/scion.md` con esas distinciones, campos internos no expuestos y capacidades que exigen API real; sin usar tablas internas como interfaz.
- Repo dueño: `deskops`; lectura también en `../scion`.
- Límites: solo código y documentación; no endpoints vivos, credenciales, agentes, mensajes, cambios de configuración ni tokens. WS05 no produce `G_SCION`.

AMBIGUEDADES
1. «Leer runtime/templates/RunDoc y API pública de Scion» junto a «no contacta endpoints vivos ni usa credenciales». No se define qué cuenta como «API pública» ni su fuente de verdad: ¿OpenAPI/docs, endpoints exportados o módulos Python? Obliga a inventar el criterio y el nivel de exposición, con riesgo de presentar funciones internas como interfaz.
2. «separar slug/agente/intento/dispatch/mensaje/conversación y permisos». «Permisos» no indica si son roles de usuario, scopes de token, permisos de operación o autorización del Hub. Obliga a inventar la taxonomía y podría omitir la que consuma WS32/WS33.
3. «Sin agentes/mensajes/config ni mostrar tokens». «Config» puede leerse como prohibición de leer configuración o solo de cambiarla; el alcance no lo aclara. Obliga a decidir si puede inspeccionar documentación/configuración existente para inventariar API y Hub.
4. Aceptación: «señalar campos internos no expuestos». No dice “no expuestos” respecto de qué superficie (API HTTP, SDK, documentación) ni cómo determinarlo sin probe. Obliga a inventar el criterio de exposición.

DRY-RUN
- Lecturas previstas: guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo en `dag.yaml`, `task-ws05.md`; código/docs de `deskops` (`runtime`, `templates`, `RunDoc`) y de `../scion`.
- Cambios previstos: crear únicamente `auditoria/scion.md`; ningún cambio de código, configuración ni datos.
- Dependencias: WS01 aporta brief/glosario; WS44 hará el probe real de `G_SCION`; WS07 designa operador y acceso; WS32/WS33 consumirán el inventario.
- Validaciones futuras: revisión de que el inventario separa identidades y no propone tablas internas como interfaz; WS44 comprobará la API real; WS32 no avanzará sin `G_SCION`.

FUTURO
WS44 produce el probe y `G_SCION`; WS07 registra operador y acceso read-only; WS12 fija el contrato de escritura; WS32.1/WS32.2 consumen el inventario; el solicitante resuelve P01/P02 y demás Pxx. No son ambigüedades de WS05.
