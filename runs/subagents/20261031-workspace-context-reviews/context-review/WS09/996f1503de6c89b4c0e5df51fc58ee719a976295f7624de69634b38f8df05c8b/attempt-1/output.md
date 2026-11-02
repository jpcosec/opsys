## REFORMULACION

WS09 es un nodo de planificación en `deskops` cuyo propósito es precisar el catálogo de renderizaciones del workspace documental. Debe producir `borradores/vistas.md` con cada fila y ficha inventariando origen, contrato o «sin contrato», renderer, acción/dueño, error y estado, usando auditorías WS02–04, decisiones WS07 y user-flows WS08. Los campos sin evidencia se marcan «no definido» con productor WS11/12 o implementación futura; se distingue authored/derivado/preferencia local y ViewDoc se trata como grafo, no como contrato universal de UI. Límites: no implementa UI/API, no ejecuta, no inventa actores, APIs ni errores actuales, y su promoción no está autorizada.

## AMBIGUEDADES

Ninguna. La aceptación fija fuentes, campos, estados y regla para lo no definido; las dependencias WS07/WS08/WS10 cubren decisiones, user-flows y estados, y las auditorías llegan transitivamente. No hay contradicción con el alcance ni límite que permita excederlo.

## DRY-RUN

Lecturas: `dag.yaml` (WS09 y vecinos), `decisiones.md`, `borradores/manual.md` (WS10), `borradores/user-flows.md` (WS08), auditorías `deskops.md`/`infraestructura.md`/`ui.md` y `borradores/vistas.md` actual. Cambio previsto: solo `deskops:desk/drawer/plans/workspace-documental/borradores/vistas.md`; completar cada fila y ficha con los seis campos, productor explícito para lo no definido, estado según WS10, error condicionado o «no definido», clasificación authored/derivado/local y citas. Dependencias: G_PRODUCT ya satisfecho por WS07; WS08/WS10 entregados; auditorías disponibles. Validación esperada: ninguna fila sin contrato/renderer/actor/error/estado; ningún actor/API/error actual inventado; ViewDoc no presentado como contrato universal; estados coherentes con WS10; filas separadas solo con evidencia/estado independiente.

## FUTURO

WS11 consume el catálogo para fijar identidad y navegación; WS18 toma de WS09/WS11 la selección mínima de ViewDoc. Los nodos de implementación y receptores por delta (WS13, WS22–25, WS27, WS29, WS39, WS41, WS42, entre otros) consumen filas concretas; la promoción y el TaskDoc quedan a cargo del supervisor, y la aceptación humana corresponde al solicitante. Nada de esto autoriza Scion ni escritura interrepo.
