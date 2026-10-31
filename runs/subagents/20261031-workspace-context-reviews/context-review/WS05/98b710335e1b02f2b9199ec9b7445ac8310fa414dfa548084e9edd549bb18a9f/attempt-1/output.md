REFORMULACION

Propósito: inventariar la identidad y la API pública de Scion para separar slug, agente, intento, dispatch, mensaje, conversación y permisos, sin usar tablas ni funciones internas como interfaz.

Resultado: `auditoria/scion.md` en el repo `deskops`, con campos internos señalados y capabilities marcadas según WS32/WS33.

Límites: solo lectura de código/documentación en `deskops` y `../scion`; no contacta endpoints vivos, no usa credenciales, no crea agentes, no envía mensajes, no modifica configuración ni muestra secretos. No produce G_SCION; eso corresponde a WS44.

Dependencia declarada: WS01.

AMBIGUEDADES

1. «marca qué capabilities requieren WS32 y WS33». WS33 no aparece definido en el input suministrado: no consta su alcance ni qué capabilities necesita. Para cumplir la aceptación, el ejecutor tendría que inventar los requisitos de WS33 o asumir que basta con nombrarlo. Cita textual: «marca qué capabilities requieren WS32 y WS33».

DRY-RUN

Lecturas previstas: `brief.md`, `alcance.md`, `decisiones.md`, `dag.yaml` (WS05, WS01), documentación/código de `deskops` (`runtime/templates/RunDoc`) y del repo `../scion`; configuración sin secretos. No se ejecutan probes.

Cambios previstos: crear/editar únicamente `auditoria/scion.md`; sin cambios de código, configuración ni mensajes.

Dependencias: WS01 debe estar disponible; WS32/WS33 consumirían el inventario. WS44 produce la evidencia real de G_SCION.

Validaciones futuras: revisión de aceptación del nodo; comprobar que el inventario separa las seis identidades y permisos, señala campos internos y no presenta tablas internas como interfaz. G_SCION seguirá `unverified` hasta el probe de WS44.

FUTURO

WS44 ejecuta el probe read-only y registra actor, Hub, fecha y capabilities. El solicitante designa operador/acceso de Scion. WS32/WS33 consumen el inventario; WS07 reutiliza decisiones registradas. La aceptación de deltas y cualquier habilitación de dispatch/mensajes quedan fuera de este nodo y requieren actores humanos o contratos posteriores.
