## REFORMULACION

**Propósito:** agrupar los contratos de producto, navegación y operaciones que habilitan la preparación de cada delta del workspace documental, sin ejecutar producto.

**Resultado:** paquete integrado por `decisiones.md`, `reconciliacion.md`, `borradores/user-flows.md`, `borradores/vistas.md`, `borradores/manual.md`, `contratos/navegacion.md` y `contratos/operaciones.md`, con decisiones Pxx trazadas, UFs cubiertas, vistas con origen/soporte, APIs y huecos con productor.

**Repo dueño:** `deskops`.

**Límites:** no implementa UI/API, no aprueba deltas, no crea actas interrepo, no autoriza Scion ni mutaciones, no inventa actores/contratos y no sustituye gates humanos pendientes.

## AMBIGUEDADES

1. «Completitud sustantiva del paquete requiere salidas de sus hijos e **integración indicada**» y «cómo se probaría resultado integrado». No se define artefacto, ubicación ni evidencia de esa integración; el ejecutor tendría que inventar dónde se registra y qué cuenta como prueba integrada.

## DRY-RUN

Orden hipotético según aristas: WS06 → WS07 → WS10 → WS08 → WS09 → WS11 → WS12.

- **WS06** lee auditorías WS02–04; produce `reconciliacion.md` con matriz por repo dueño.
- **WS07** consume WS06 y `owner-decisions.json`; consolida P01–P09 en `decisiones.md` y `baseline_proposal`.
- **WS10** consume auditorías, WS07 y P08; fija índice/convención en `manual.md`.
- **WS08** consume WS07 y operaciones auditadas; produce `user-flows.md` con UF01–UF10, operaciones, errores, nodos y gates.
- **WS09** consume UFs WS08, convención WS10 y decisiones; produce `vistas.md` con origen, contrato, renderer, acción, error y estado.
- **WS11** consume vistas y UFs; produce `navegacion.md` con identidad, foco, enlaces, multidesk y huecos clasificados.
- **WS12** consume navegación y UFs; produce `operaciones.md` con whitelist, canales, actores, precondición y efectos.

**Validación futura:** contrastar que cada Pxx tenga tipo/actor/fuente/nodos; cada UF tenga entrada/salida/operación/error/nodo/gate; cada vista tenga soporte/origen/estado; cada hueco tenga productor; `G_SOURCE`, `G_PAYLOAD_PRECONDITION` y `G_WRITE_CONTRACT` se evalúen por delta; y que no se infieran permisos ni APIs. Nada se ejecuta ahora.

## FUTURO

P01/repos receptores producen actas por delta; WS20 produce `G_SOURCE`; WS45 produce `G_PAYLOAD_PRECONDITION`; WS16/30/37/39 ejecutan pruebas humanas; WS40 genera el corpus.
