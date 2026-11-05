REFORMULACION
GC08 es un nodo de entrega documental (`kind: docs`, no agregado) del plan `gates-por-tipo`, repo dueño deskops. Propósito: alinear rituales y documentación con tipos de tarea, `ReviewDoc` y `deskops review`. Resultado: editar `desk/rituals/execution.md`, `context-review.md` y `phase.md`; `docs/workflow-policy-reference.md`, `operator-manual.md` y `quickstart.md`; y `CHANGELOG.md`. Límites: solo el `output_scope` listado; no toca código ni sldb; depende de GC03, GC05 y GC06; las ediciones de rituales se hacen con `deskops edit ritual`, no a mano.

AMBIGUEDADES
1. “paso 8 nombra los dos kinds”. No dice cuáles dos. Obliga a inventar si son `preflight`/`bundle` o pares como `reproduction`/`goldens`, cuando GC03 define cinco kinds.
2. “se retira la ruta runs/subagents/<run-dir>/preflight.md como lugar único” frente a “grep de "preflight.md" en desk/rituals y docs no devuelve nada”. Contradicción: “como lugar único” admite conservarla como una ubicación; el grep exige eliminarla por completo. Obliga a decidir si se borra toda mención o se deja una.
3. “deskops doctor sin alertas nuevas”. No fija el estado base. Obliga a inventar contra qué ejecución o snapshot se comparan las “nuevas”.

DRY-RUN
Un ejecutor futuro leería los tres rituales, los tres documentos, `brief.md` §Tipos, `CHANGELOG.md` y las salidas ya cerradas de GC01, GC03, GC05 y GC06. Editaría los rituales con `deskops edit ritual`; reemplazaría la ruta `preflight.md` por la evidencia de `runs/` que escribe `deskops review`; añadiría el tope D9; actualizaría la tabla de tipos, reglas por tipo, campos del contrato y campos no editables; y escribiría el flujo `add task --task-type → review preflight → review bundle → review dispose → advance`. Dependencias: GC03 aporta comando, `ReviewDoc` y `runs/`; GC05, reglas por tipo; GC06, campos rechazados; GC01, tabla de tipos. Validaría con extracción ida y vuelta por `RitualDoc`, `deskops doctor`, los dos greps, comparación de tabla con `brief.md`, `test_cli_help_examples.py` y entrada de CHANGELOG. Sin ejecutar.

FUTURO
GC03 produce `deskops review` y `ReviewDoc`; GC05, las reglas por tipo y `G_CONSUMER`; GC06, el rechazo de campos; GC01, la tabla de tipos. Quien opera el desk ejecutará doctor, greps y tests, y escribirá la disposición de revisión; el dueño decide los pendientes de `decisiones.md` que no bloquean este nodo.
