## REFORMULACION

**Propósito.** Revisar si WS32 se entiende como encargo de planificación: unificar identidad de intento y cierre Scion refinando el ticket existente, sin segundo pipeline.

**Resultado.** Nodo `aggregate` (no ejecutable) cuyo cumplimiento depende de WS32.1 y WS32.2; sus dependientes siguen apuntando a WS32.

**Repo dueño.** `deskops` (`output_base: deskops:repository_root/`), con `overlap_with: scion`.

**Límites.** No duplicar implementación ni recrear pipeline; `integration_mode: delta_or_existing_ticket`; `promotion: not_authorized`; matriz WS06 llega transitivamente por WS11/WS12.

## AMBIGUEDADES

1. **Ticket destino sin ubicación verificable.** Cita: «Refinar el ticket de external_references.scion, sin segundo pipeline». El nodo no nombra repo, ruta ni identificador del ticket, y `external_references` no se suministra en el input. Obligaría a inventar qué artefacto se refina y dónde queda la evidencia de ese refinamiento (¿comentario, sección, nueva tarea?).

2. **Dependencia de gate sin arista de prerrequisito.** Cita: «requires: - G_SCION» junto a `depends_on: [WS05, WS12, WS32.1, WS32.2]`. El bloque de gates declara `produced_by: WS44`, que no figura como dependencia directa ni transitiva declarada del nodo. Obligaría a inventar si WS32 puede promoverse antes del probe o si debe esperar a WS44.

3. **Modo de integración alternativo sin criterio.** Cita: «integration_mode: delta_or_existing_ticket». Aunque se delega en la matriz WS06, el nodo no fija qué condición elige una rama u otra para este delta. Obligaría a inventar el criterio de elección al preparar la promoción. *(No es ambigüedad: aceptación agregada, gates pendientes y `promotion: not_authorized`.)*

## DRY-RUN

- **Lecturas previstas:** dag.yaml (WS32, WS32.1/2, gates), brief.md, alcance.md, decisiones.md, cobertura.md, reconciliacion.md y `desk/drawer/tasks/workspace-documental/task-ws32.md` (no suministrado en el input).
- **Cambios previstos:** ninguno en esta revisión; WS32 no ejecuta. En promoción se enlazaría el ticket `external_references.scion` ya existente.
- **Dependencias:** WS05 (inventario), WS12 (contrato/registro por intento), WS32.1 y WS32.2.
- **Validaciones futuras:** aceptación conjunta de hijos; G_CLOSEOUT ya satisfecho; G_WRITE_CONTRACT `per_delta`; G_SCION vía WS44.

## FUTURO

- WS05 produce inventario; WS12 contrato; WS32.1/2 implementan y prueban.
- WS06 integra el delta en el ticket receptor vigente.
- WS44 ejecuta el probe de Scion (G_SCION).
- El receptor P01 emite acta por delta con commit/blob en repo dueño.
- Un humano autoriza la promoción.
