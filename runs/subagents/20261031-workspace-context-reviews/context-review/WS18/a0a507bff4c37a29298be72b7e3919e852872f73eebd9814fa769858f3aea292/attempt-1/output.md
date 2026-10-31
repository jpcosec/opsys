## REFORMULACION
**Propósito:** declarar en spec2viz proyecciones de grafo reutilizables mediante ViewDoc y su NotationDoc, para selecciones y notación ya soportadas.
**Resultado:** una vista portable que renderiza sobre un store real la selección declarada, coincide con ella, y un ViewDoc que documenta qué selecciona.
**Repo dueño:** spec2viz; rutas concretas las confirma su dueño al promover.
**Límites:** no crear páginas UI declarativas ficticias, no modificar el repo desde este plan, promoción no autorizada y gate receptor G_SPEC_VIEW obligatorio.

## AMBIGUEDADES
1. **«Vista portable renderiza sobre un store real»**: no hay definición de “portable” en brief, alcance ni glosario. Obliga a inventar el criterio de portabilidad —entre stores, hosts o formatos— y, por tanto, cuándo la aceptación se cumple.
2. **«para selecciones y notación ya soportadas»**: no se indica dónde queda fijado qué selecciones y notaciones están soportadas. WS09 inventaría renderizaciones y advierte que «ViewDoc es grafo, no contrato universal de UI»; WS11 cierra navegación e identidad, no un catálogo de notación. Obliga a inventar el conjunto exacto y el alcance de lo declarable.

## DRY-RUN
**Lecturas previstas:** nodo WS18, guía de revisión, brief, alcance, decisiones, cobertura, dag.yaml (WS09, WS11, gates) y task-ws18.md al promover.
**Cambios previstos:** ninguno en este revisor; no se ejecuta ni modifica repo.
**Dependencias:** WS09 y WS11 como prerrequisitos; G_SPEC_VIEW pendiente, resuelto por WS11; promoción por dueño de spec2viz.
**Validaciones futuras:** comprobar acta G_SPEC_VIEW con delta y responsable; confirmar rutas y no solapamiento en spec2viz; promover tarea receptora; ejecutar prueba sobre store real y verificar coincidencia y documentación del ViewDoc.

## FUTURO
WS07 debe designar al responsable de spec2viz; WS11 debe producir el acta G_SPEC_VIEW; el dueño del repo promueve la tarea receptora; un nodo posterior de ejecución implementa y valida; WS24 consume la proyección. Nada de esto se resuelve aquí.
