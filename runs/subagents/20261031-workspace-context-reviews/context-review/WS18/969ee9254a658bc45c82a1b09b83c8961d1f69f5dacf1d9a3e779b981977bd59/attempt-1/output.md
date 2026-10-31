## REFORMULACION
- **Propósito:** declarar proyecciones de grafo reutilizables mediante ViewDoc y su NotationDoc, limitadas a selecciones y notación ya soportadas por spec2viz, sin inventar UI declarativa.
- **Resultado:** una vista portable (mismo ViewDoc, sin código de host) que renderiza sobre un store real la selección declarada, coincide con ella y documenta qué selecciona.
- **Repo:** `spec2viz` (`owner_repo`); salida en `sldb/views/` (rutas a confirmar por su dueño al promover) y `tests/`.
- **Límites:** no crear UI pages ficticias; no modificar su repo desde este plan; promoción no autorizada; gate `G_SPEC_VIEW` obligatorio, evaluado por delta; este revisor no ejecuta nada.

## AMBIGUEDADES
1. **«no modificar su repo desde este plan»** — No queda claro el antecedente de «su» ni cómo conciliarlo con `owner_repo: spec2viz` y una entrega de tipo `implementation`. Obliga a inventar si el ejecutor escribe ViewDoc/tests en spec2viz o solo produce un artefacto/tarea en deskops para que el dueño lo promueva, y quién materializa el resultado.
2. **«para selecciones y notación ya soportadas por spec2viz»** / **«la selección declarada»** — No se enumera qué selección o notación concreta constituye el entregable; la aceptación remite circularmente a lo que declare el propio ViewDoc. WS09 cataloga renderizaciones, no necesariamente selecciones ViewDoc. Obliga a inventar el conjunto mínimo o el caso concreto que debe declararse y probarse. No se considera ambigüedad el store: las reglas comunes ya fijan store temporal real o corpus WS40.

## DRY-RUN
- **Lecturas previstas:** nodo WS18 y gate `G_SPEC_VIEW`; bloques vecinos WS09/WS11 como contratos; brief, alcance, decisiones y guía; documentación real de spec2viz al promover.
- **Cambios previstos:** ViewDoc + NotationDoc en `sldb/views/`, pruebas en `tests/`, y promoción de tarea receptora en spec2viz por su dueño.
- **Dependencias:** catálogo WS09, contrato de navegación WS11 y recibo per-delta `G_SPEC_VIEW`; confirmación de rutas por el dueño de spec2viz; store real de prueba.
- **Validaciones futuras:** render portable coincide con la selección declarada; ViewDoc documenta la selección; pruebas pasan; recibo con actor, IDs, efecto y commit/blob en repo receptor.

## FUTURO
WS11 produce el recibo `G_SPEC_VIEW`; el dueño de spec2viz confirma rutas y promueve tareas receptoras; la promoción fijará archivos, escenarios y evidencias; la aceptación humana y la recepción técnica ocurren fuera de este nodo. Este ViewDoc es opcional y no bloquea WS24 ni el manual.
