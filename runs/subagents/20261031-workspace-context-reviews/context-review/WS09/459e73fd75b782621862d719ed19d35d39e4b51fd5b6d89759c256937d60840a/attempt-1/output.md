## REFORMULACION
**Propósito**: convertir el borrador `vistas.md` en un catálogo de renderizaciones preciso, no en una lista de pantallas. **Resultado**: `borradores/vistas.md` con cada fila provista de origen, contrato, renderer, acción/dueño, error y estado, distinguiendo authored/derivado/preferencia local. **Repo dueño**: deskops. **Límites**: no diseñar UI, no ejecutar, no promover (`promotion: not_authorized`); ViewDoc es grafo, no contrato universal de UI; depende de WS07 y del gate G_PRODUCT.

## AMBIGUEDADES
1. **Alcance de "cada fila"**. Cita: «Cada fila tiene origen, contrato, renderer, acción/dueño, error y estado» frente a «Ficha de cada vista (pendiente de completar)». `vistas.md` tiene tres tablas (catálogo, «Filas que faltaban», ficha) y filas-categoría («Cualquier documento del desk») que no son vistas. Obliga a inventar si la aceptación se aplica a todas las tablas, solo al catálogo, y si la granularidad es fila o vista.
2. **Taxonomía de "error" y "estado"**. Cita: «error y estado». No se define qué valores son válidos (¿error de resolución de origen, de renderer, de contrato?; ¿disponible/planificado/inexistente?). Obliga a inventar el vocabulario con el que se comprueba la aceptación.
3. **Fuente del inventario de "vistas existentes"**. Cita: «Inventariar ... y vistas existentes» y «disponibilidad actual» en la ficha. El nodo no nombra quién aporta el inventario de renderizadores de graph_ui/spec2viz ni qué hacer si no hay acceso; con `owner_repo: deskops` obliga a inventar el "estado" de disponibilidad o a leer código no designado.

## DRY-RUN
**Lecturas**: `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/vistas.md`, nodo WS09 y gate G_PRODUCT en `dag.yaml`.
**Cambios previstos**: solo `desk/drawer/plans/workspace-documental/borradores/vistas.md`.
**Dependencias**: WS07 debe registrar G_PRODUCT/decisiones con actor y fecha antes de cerrar WS09.
**Validaciones futuras**: WS11 consume huecos clasificados; WS18, WS22 y WS23 consumen filas de ViewDoc/Board/ritual; verificación de aceptación fila a fila antes de promoción.

## FUTURO
G_PRODUCT lo resuelve un humano vía WS07 (no este nodo). WS11 cierra el contrato de navegación e identidad y clasifica huecos; WS18 declara proyecciones en spec2viz con G_SPEC_VIEW. La promoción de WS09 y cualquier cambio de `dag.yaml` los decide el humano, no esta revisión.
