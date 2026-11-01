## REFORMULACION
WS09 (planning, deskops) debe precisar en `borradores/vistas.md` el catálogo de renderizaciones: por cada fila, origen, contrato o «sin contrato», renderer, acción/dueño, error y estado, distinguiendo authored/derivado/preferencia local y completando la ficha. Resultado: catálogo contrastado con auditorías WS02–04, decisiones y UFs WS08. Límites: no implementa UI/API ni inventa actores/APIs; ViewDoc es grafo, no contrato universal de UI.

## AMBIGUEDADES
1. «Estado = disponible/propuesto/bloqueado según WS10; disponibilidad actual viene de auditoria/ui.md (WS04)». WS10 exige acta humana para «disponible»; no aclara si un renderer ya implementado sin acta es disponible o propuesto. Obliga a inventar el criterio de estado.
2. «Campo sin evidencia se marca no definido con productor WS11/12 o futura implementación, incluido renderer/actor/campos/relaciones». No asigna productor por tipo: para renderer o acción de lectura, WS11/12 no son dueños y «futura implementación» no identifica nodo. Obliga a inventar productor.
3. «separar fila solo si el delta tiene evidencia/estado independiente». No define qué cuenta como delta independiente para dividir o mantener filas compuestas. Obliga a inventar el criterio de granularidad.

## DRY-RUN
Leería `dag.yaml`, auditorías WS02–04, `decisiones.md`, `borradores/user-flows.md` de WS08, `borradores/manual.md` de WS10 y `borradores/vistas.md`. Cambiaría solo `vistas.md`: completaría filas y una ficha por fila con los campos exigidos, listas en filas compuestas y «no definido» con productor. Consumiría G_PRODUCT (satisfecho por WS07) y las dependencias WS07/WS08/WS10; WS04 llega transitivamente. No tocaría código ni otros repos. Si falta auditoría, UF, definición de estado o evidencia, se detendría y registraría el hueco con repo dueño, sin sustituto. Validaría: campos completos, estados trazables a WS10/ui.md, ausencia de actores/APIs inventados y filas compuestas justificadas.

## FUTURO
WS11 cerrará navegación/identidad; WS12 operaciones y actores; WS18 ViewDoc/NotationDoc; WS13/22/23/24 implementaciones; WS16/30 actas humanas; WS10 definiciones de estado. La aceptación de producto es humana. No son ambigüedades de WS09.
