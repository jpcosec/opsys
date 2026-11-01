REFORMULACION
Propósito: inventariar identidad y API pública de Scion para que WS32/WS33 distingan interfaz pública, campos internos y capabilities que exigen API real. Resultado: `auditoria/scion.md` en repo `deskops`, separando slug/agente/intento/dispatch/mensaje/conversación y permisos, y marcando capabilities dependientes de WS32/WS33. Límites: solo lectura de código/documentación en deskops y `../scion` y configuración sin secretos; no endpoints vivos, credenciales, creación de agentes, mensajes ni cambios de configuración; no produce G_SCION, cuya evidencia corresponde al probe de WS44. Dependencia directa: WS01.

AMBIGUEDADES
Ninguna. La frontera público/interno queda acotada por “endpoints/SDK documentados o exportados; no tablas ni funciones internas”. Los huecos deben señalarse como campos internos o capabilities que requieren API real, sin sustituirlos por invención. La falta de contrato o API se resuelve registrando el hueco, conforme a las reglas comunes.

DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, `dag.yaml` y, en deskops/`../scion`, runtime/templates/RunDoc, documentación/exportaciones públicas y configuración sin secretos. Cambios previstos: crear/editar solo `auditoria/scion.md`; ningún código, configuración ni tarea. Dependencias: WS01 como prerrequisito; WS33 como contexto de revisión; salidas consumidas por WS32, WS33 y WS44. Validaciones futuras: comprobar separación de conceptos y permisos, marcas WS32/WS33, ausencia de tablas internas usadas como interfaz, no exposición de tokens y distinción entre inventario y evidencia real de G_SCION.

FUTURO
WS44 ejecutará el probe read-only y producirá la evidencia de G_SCION. WS32/WS33 materializarán las capabilities marcadas. Cualquier acceso, credencial, Hub o autorización de operador corresponde a decisión humana, WS07 o WS44, no a WS05.
