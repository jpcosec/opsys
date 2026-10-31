## REFORMULACION
**Propósito:** dejar `brief.md` autosuficiente: acuerdos del solicitante citados textualmente y glosario que distinga documento, nodo, vista, renderer/representación, consulta y foco.
**Resultado:** edición en sitio de `brief.md`, sin requisitos que dependan de un chat invisible.
**Repo dueño:** deskops. **Límites:** solo `brief.md`; no implementar UI ni modificar tareas de otras sesiones; las propuestas remiten a `decisiones.md`, no las resuelve este nodo.

## AMBIGUEDADES
1. «distinciones documento/nodo/vista/renderer/consulta/foco». El brief define «Renderización/representación» y «Vista de trabajo», pero no usa el término «renderer». Obliga a inventar si debe añadirse una entrada nueva «renderer», renombrar la existente o interpretarla como sinónimo.
2. «Cada acuerdo cita al solicitante y cada propuesta remite a decisiones.md.» No se delimita qué afirmaciones del brief son «acuerdo» ni qué es «propuesta» (frente a vocabulario, criterio de éxito o límites). Obliga a inventar el inventario de acuerdos/propuestas y su correspondencia con Pxx.

## DRY-RUN
**Lecturas previstas:** `brief.md`, `decisiones.md`, `alcance.md`, `dag.yaml` y la guía; contraste con `cobertura.md` y `borradores/vision.md` solo como fuentes suministradas.
**Cambios previstos:** editar únicamente `deskops:desk/drawer/plans/workspace-documental/brief.md`, preservando citas textuales y referencias a `decisiones.md`.
**Dependencias:** ninguna (`depends_on: []`); no requiere contratos, API ni permisos.
**Validaciones futuras:** review barato sin historial que reformule el producto usando solo `brief.md`; comprobar cita del solicitante por acuerdo y remisión a `decisiones.md` por propuesta. Sin ejecución.

## FUTURO
El TaskDoc de promoción fijará archivos exactos, pills y evidencia. WS07 resolverá las propuestas Pxx; un humano aprobará el brief. WS02–WS05 consumen este brief como fuente. La promoción sigue `not_authorized`.
