## REFORMULACION
**Propósito:** implementar en `graph_ui` el alta y baja de relaciones permitidas por el contrato de WS12, usando API real y before-image, sin definir semántica de relaciones en el componente.

**Resultado:** mutaciones de relaciones que persisten y se confirman tras recargar; una relación no permitida o una revisión obsoleta se rechaza con error visible.

**Repo:** `graph_ui`.

**Límites:** alcance en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`; no crear semántica de relaciones; no editar campos workflow-protected; G_HUMAN_READ solo habilita uso de mutaciones en UI, no bloquea desarrollo/pruebas aisladas de API; no duplicar la base ya integrada; promoción no autorizada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas previstas:** nodo WS19.2 y contratos vecinos WS19/WS12; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md` y guía.

**Cambios previstos, sin ejecutar:** código de relaciones y pruebas en `graph_ui`; endpoints solo si WS12 los autoriza; TaskDoc de promoción fijará archivos, pills, escenarios y textos exactos.

**Dependencias:** WS12 produce whitelist/operaciones; WS11 y WS08 llegan transitivamente; G_WRITE_CONTRACT y G_UI_WRITE se evalúan por delta; G_HUMAN_READ para habilitar uso en UI; WS06/reconciliación al promover.

**Validaciones futuras:** alta y baja persisten tras recarga; rechazo visible de relación no permitida y revisión obsoleta; prueba con API real; acta de recepción por delta; no inferir cierre por commit.

## FUTURO
- WS12 debe publicar whitelist, endpoints, errores y requisitos de revisión aplicables a relaciones.
- WS19.1 y el agregado WS19 completan su aceptación.
- El receptor P01 en `graph_ui` produce el acta de G_UI_WRITE para este delta.
- WS16 produce G_HUMAN_READ antes de habilitar mutaciones en UI.
- La promoción fija TaskDoc, archivos y pruebas; WS06 mantiene la matriz sin duplicar implementación.
