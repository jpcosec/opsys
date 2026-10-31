REFORMULACION
Propósito: inventariar la identidad y la API pública de Scion para separar slug, agente, intento, dispatch, mensaje, conversación y permisos, sin acceso vivo. Resultado: `auditoria/scion.md`. Repo dueño: deskops; lectura adicional en `../scion`. Límites: solo lectura de código, documentación y configuración sin secretos; no contacta endpoints ni usa credenciales; no crea agentes, envía mensajes, cambia configuración ni muestra tokens; no produce G_SCION.

AMBIGUEDADES
1. «marca qué capabilities requieren WS32 y WS33». WS33 no aparece definido en el input suministrado. Para clasificar sus capabilities el ejecutor tendría que inventar el alcance o las necesidades de WS33.
2. «API pública de Scion (endpoints/SDK documentados o exportados; no tablas ni funciones internas)». No se fija qué prevalece si documentación y exports discrepan, ni el límite exacto entre símbolo exportado y función interna. Obligaría a inventar un criterio de “público” para decidir qué campos son interfaz.

DRY-RUN
Lecturas previstas: `dag.yaml` (WS05, WS01, WS32, WS44, gates), `brief.md`, `alcance.md`, `decisiones.md`; `runtime/templates/RunDoc` en deskops; documentación y exports públicos en `../scion`; configuración sin secretos. Cambios previstos: crear únicamente `auditoria/scion.md`; ningún cambio de código o configuración. Dependencias: WS01 como prerrequisito; WS44 para el probe real; WS32/WS33 como consumidores. Validaciones futuras: revisión de aceptación, mapeo de capabilities y probe read-only de WS44.

FUTURO
WS44 ejecuta el probe y produce G_SCION. WS07 designa al operador Scion y registra su acceso read-only. WS32 y WS33 consumen el inventario. WS07 resuelve las propuestas Pxx. Nada de esto es ambigüedad del nodo.
