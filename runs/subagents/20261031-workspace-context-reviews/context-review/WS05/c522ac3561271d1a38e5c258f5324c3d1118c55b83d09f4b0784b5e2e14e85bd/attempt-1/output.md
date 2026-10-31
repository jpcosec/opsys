## REFORMULACION

**Propósito:** inventariar la identidad y la API pública de Scion para separar slug, agente, intento, dispatch, mensaje, conversación y permisos, distinguiendo lo público de lo interno.

**Resultado:** `auditoria/scion.md`.

**Repo:** `deskops`; lectura permitida en `../scion`.

**Límites:** solo lectura de código, documentación y configuración sin secretos; sin endpoints vivos, credenciales, creación de agentes, mensajes ni cambios de configuración. No produce `G_SCION`; el probe corresponde a WS44.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS05 en `dag.yaml`; guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`; contratos vecinos WS01, WS32, WS32.1, WS32.2, WS44, WS33 y gate `G_SCION`.

**Cambios previstos:** únicamente crear `auditoria/scion.md`. No se modifica código ni configuración.

**Dependencias:** WS01 como prerrequisito directo; disponibilidad del repo `../scion` para lectura. WS12, WS32, WS33 y WS44 aparecen como consumidores o contratos futuros, no como dependencias de ejecución de WS05.

**Validaciones futuras:** comprobar que el inventario no usa tablas internas como interfaz; que señala campos internos ausentes de la API pública y capacidades que exigen API real; que separa las seis identidades y los permisos; y que marca qué capacidades requieren WS32 y WS33. El TaskDoc de promoción fijará archivos, escenarios y textos dentro de esa aceptación.

## FUTURO

WS44 ejecutará el probe real y producirá `G_SCION`; WS32/WS33 consumirán el inventario para identidad, dispatch, manifiesto, mensajes y cierre; WS12 aportará el contrato del registro por intento; el solicitante designará operador Scion al abordar el ramal E. La promoción de WS05 requiere TaskDoc y preflight, hoy no autorizados.
