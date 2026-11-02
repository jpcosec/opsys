## REFORMULACION
**Propósito:** precisar el catálogo de vistas/renderizaciones del workspace documental. **Resultado:** `borradores/vistas.md` con una ficha por fila que inventaría origen, contrato —o «sin contrato»—, renderer, acción/dueño, error, estado y clasificación authored/derivado/preferencia local. **Repo dueño:** deskops. **Límites:** es planificación, no implementa UI ni renderers; no inventa actores, APIs ni disponibilidad; ViewDoc es solo grafo, no contrato universal de UI. **Dependencias:** WS07 (decisiones), WS10 (estado del manual), WS08 (UFs); G_PRODUCT ya satisfecho por WS07.

## AMBIGUEDADES
1. «Campo sin evidencia se marca no definido con productor WS11/12 o futura implementación». «Futura implementación» no identifica nodo ni repo dueño; el ejecutor tendría que inventar qué nodo o repositorio produce ese campo.
2. «Inventariar fuente, queries, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas existentes». La enumeración no fija si entran Inbox, Drawer, registry, roles, RunDoc, materializaciones o diff Git; el ejecutor decidiría el conjunto de filas sin criterio cerrado, pese a que la aceptación remite a «cada fila de las tablas de vistas.md».

## DRY-RUN
Lecturas: nodo y aristas WS09 en `dag.yaml`; `decisiones.md`; auditorías `deskops.md`, `infraestructura.md`, `ui.md` (vía WS07); `manual.md` de WS10; `user-flows.md` de WS08; estado actual de `borradores/vistas.md`. Cambios previstos: reescribir las tablas y fichas F01–F20 de `vistas.md`, completando por fila origen, contrato, renderer, acción/dueño, error, estado y clase. Dependencias consumidas: criterio de estado de WS10, mapeo UF de WS08, registro de decisiones de WS07 y evidencia G_PRODUCT. Errores esperados: si falta evidencia, marcar «no definido» con productor WS11/WS12 o futura implementación; si no hay productor identificable, detenerse y registrar el hueco, sin inventar API ni actor. Validación futura: cada fila tiene todos los campos, clasificación y estado; ninguna afirma disponibilidad ni API no auditada; ViewDoc no se trata como contrato universal; no se crean pasos, capturas ni código.
No ejecutable como agregado: es un nodo de planificación atómico; su producto es el documento.

## FUTURO
WS11 consume el catálogo para cerrar el contrato de navegación; WS18 requiere de WS09/WS11 la selección mínima concreta y se detiene si falta; WS22, WS23 y WS24 usan las fichas como fuente de alcance. La recepción de deltas y cualquier corrección del catálogo corresponden a WS11 y al responsable de producto, no a este revisor.
