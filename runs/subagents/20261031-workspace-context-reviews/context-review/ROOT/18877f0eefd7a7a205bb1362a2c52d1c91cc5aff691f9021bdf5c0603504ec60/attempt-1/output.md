## REFORMULACION

- **Propósito:** revisar ROOT como encargo de planificación agregado: si su alcance, resultado, repo, límites y aceptación son comprensibles y comprobables. No se evalúa el producto ni se ejecuta el plan.
- **Resultado:** disposición de `context_review` para ROOT, sin ambigüedad o con bloqueo/ambigüedad explícitos, para que coordinación determine si la revisión está vigente.
- **Repo dueño:** `deskops`, según rutas `desk/drawer/plans/workspace-documental/...` y comandos desde su raíz.
- **Límites:** ROOT es agrupación de revisión y no se ejecuta; no implementa ni autoriza producto. No reviso los contratos de PK01–PK08. No ejecuto scripts, no promuevo tareas, no pido decisiones ya registradas ni permisos Scion.

## AMBIGUEDADES

ninguna.

## DRY-RUN

- **Lecturas previstas:** `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/vision.md`, el fragmento ROOT de `dag.yaml`; los bloques `edge:PK*` solo como contratos vecinos, sin revisarlos.
- **Cambios previstos:** ninguno ejecutado; como revisor, dejar constancia de la disposición de ROOT. No escribiría archivos ni modificaría `dag.yaml`.
- **Dependencias:** revisiones vigentes de los hijos directos PK01–PK08 y, por su aceptación, de sus WS; `disposition.md` guardada para los hashes actuales de input y contrato; `execution_authorized=false`.
- **Validaciones futuras, sin ejecutar:** `python desk/drawer/plans/workspace-documental/context_review.py status` y `python desk/drawer/plans/workspace-documental/validate_plan.py --check` en PASS desde la raíz de `deskops`; comprobar coincidencia de hashes y revisión de cada hijo.

## FUTURO

Los nodos PK y sus hijos producirán sus propias revisiones y disposiciones. La sesión de coordinación ejecutará `context_review.py status` y `validate_plan.py --check`, registrará bloqueos externos con responsable si aparecen y verificará los hashes. El responsable humano ya consta en `decisiones.md`; no corresponde nueva firma en este nodo. Cualquier contrato, API, acta o permiso pendiente tiene productor definido y no se sustituye aquí.
