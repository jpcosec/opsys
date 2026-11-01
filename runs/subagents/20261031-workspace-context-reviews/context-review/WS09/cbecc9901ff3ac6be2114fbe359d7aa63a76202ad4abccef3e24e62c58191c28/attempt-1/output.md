## REFORMULACION

**Propósito:** WS09 debe precisar el catálogo de renderizaciones del workspace documental, contrastando fuentes, consultas, Board, rituales, conocimiento/crossroads, issues, FAQ, Code y vistas existentes con la evidencia disponible.

**Resultado:** `borradores/vistas.md` actualizado: cada fila con origen, contrato o «sin contrato», renderer, acción/dueño, error y estado; fichas completas; distinción authored/derivado/preferencia local.

**Repo:** `deskops`.

**Límites:** nodo de planificación, no implementación. No crea contratos, APIs ni actores; no inventa disponibilidad; ViewDoc es grafo, no contrato universal de UI. `promotion: not_authorized`; el nodo sigue siendo candidato.

## AMBIGUEDADES

Ninguna. La aceptación ya prevé el tratamiento de huecos: «Campo sin evidencia se marca no definido con productor WS11/12 o futura implementación» y «nunca inventar actor/API disponible». Las fuentes y dependencias están nombradas; las ausencias se resuelven con la regla común de ejecución, no inventando.

## DRY-RUN

Un ejecutor futuro, si se autoriza la promoción, leería: nodo WS09 en `dag.yaml`, `vistas.md`, `decisiones.md`, auditorías WS02–04, `borradores/user-flows.md` (WS08) y `borradores/manual.md` (WS10), y comprobaría `G_PRODUCT` ya satisfecho.

Cambios previstos: editar solo `borradores/vistas.md`. Por cada fila de sus tablas, rellenaría origen, contrato, renderer, acción/dueño, error y estado; completaría la ficha; usaría listas en filas compuestas; marcaría campos sin evidencia como «no definido» con productor; distinguiría authored/derivado/local; no asignaría actores/API no evidenciados.

Dependencias: auditorías, UFs, decisiones y definiciones de estado de WS10. Gates: `G_PRODUCT` satisfecho; no hay gate adicional ni autorización de promoción. Errores esperados: si falta un contrato/API/dato de una dependencia, detenerse y registrar el hueco con repo dueño, sin sustituto. Validación posterior: comprobar que todas las filas tienen los campos exigidos, estados solo `disponible/propuesto/bloqueado`, errores condicionados o «no definido», y que ViewDoc no se trata como contrato universal.

## FUTURO

WS11/WS12 producirán contratos, actores y operaciones faltantes; WS04/WS08/WS10 aportan evidencia y criterios; WS18 consumirá la selección mínima del catálogo; WS22–24 implementarán vistas. La autorización de promoción y cualquier recepción posterior corresponden al humano o al repo dueño, no a WS09.
