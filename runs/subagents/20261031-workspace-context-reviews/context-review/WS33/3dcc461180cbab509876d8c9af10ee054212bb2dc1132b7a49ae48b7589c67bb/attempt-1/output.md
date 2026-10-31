## REFORMULACION

**Propósito:** planificar la vinculación de mensajes, resultados y decisiones humanas de Scion con su intento, conservando procedencia y evitando duplicados.

**Resultado:** un agregado no ejecutable cuyo cumplimiento deriva de WS33.1 y WS33.2; sus dependientes siguen apuntando a WS33.

**Repo dueño:** `deskops`; salida en `runtime/`, modelos/reportes y tests según hijos.

**Límites:** backend documental, independiente del editor UI; no autoriza promoción ni ejecución; `overlap_with: scion` exige integración como delta o ticket existente, nunca duplicado paralelo; requiere `G_SCION`.

## AMBIGUEDADES

1. **Dependencia WS06 ausente.** Cita: «`integration_mode: delta_or_existing_ticket_only_after_WS06; never_parallel_duplicate`». WS06 no figura en `depends_on`, que solo lista WS32, WS11 y los hijos. Obligaría al ejecutor a inventar si WS06 es prerrequisito real, si basta una comprobación posterior o si la condición es meramente informativa.

2. **Actor de la revisión humana sin fuente definida.** Cita: «Referencias Hub/proyecto/conversación/mensaje/intento y revisión humana explícita». El nodo exige registrar una decisión humana, pero no nombra quién la emite, cómo se identifica ni qué evidencia la respalda. Obligaría a inventar identidad, autenticación y formato de registro, o a decidir que basta un campo libre.

## DRY-RUN

**Lecturas previstas:** `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, nodo WS33 en `dag.yaml` y, en promoción, `task-ws33.md`.

**Cambios previstos:** ninguno; esta revisión no modifica archivos ni `dag.yaml`.

**Dependencias:** WS32 y WS11 como prerrequisitos; WS33.1 y WS33.2 como hijos; `G_SCION` producido por WS44 con operador designado en WS07; WS06 referido solo en `integration_mode`.

**Validaciones futuras:** aceptación agregada de ambos hijos; evidencia real de `G_SCION`; ausencia de duplicación de tablas o pipeline Scion; confirmación de que no hay promoción ni ejecución autorizadas; preflight de archivos exactos, pills y átomos antes de promover.

## FUTURO

- WS07 designa al operador Scion.
- WS44 ejecuta el probe y produce `G_SCION`.
- WS06 define la vía de integración delta/ticket existente.
- WS12 aporta el contrato de escritura y efectos.
- Un humano autoriza la promoción; otro nodo ejecuta el preflight y la promoción.
