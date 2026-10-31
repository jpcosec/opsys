## REFORMULACION

**Propósito:** revisar ROOT como encargo de planificación, no como producto ni como ejecución. Se evalúa si su propósito, resultado, repo dueño, límites y aceptación comprobable están definidos sin obligar a inventar.

**Resultado:** una disposición de revisión sobre ROOT; no se implementa nada ni se modifican nodos.

**Repo:** `deskops`, con el plan en `desk/drawer/plans/workspace-documental/`; los comandos de aceptación se ejecutan desde la raíz de `deskops`.

**Límites:** ROOT es agrupación de revisión, no dependencia operativa. No resuelve decisiones humanas, no autoriza ejecución (`execution_authorized=false`) y no revisa los bloques `edge`, que son contratos de vecinos.

## AMBIGUEDADES

Ninguna.

La aceptación identifica el resultado —revisión vigente de cada hijo directo—, el actor que registra bloqueos —la sesión de coordinación—, la evidencia —`disposition.md` asociada a hashes— y las validaciones —`context_review.py status` y `validate_plan.py --check`. El repo y el límite de no implementar también están explícitos. Las referencias a `publicación básica` o al ramal Scion quedan acotadas por PK06 y PK08, sin forzar al ejecutor de ROOT a definir su contenido.

## DRY-RUN

- **Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/vision.md`, bloque ROOT y bloques PK01–PK08 de `dag.yaml`.
- **Cambios previstos:** ninguno sobre el plan; solo la disposición de revisión que produzca este nodo.
- **Dependencias:** disposiciones vigentes de PK01–PK08, hashes de input y contrato coincidentes, y herramienta de revisión disponible.
- **Validaciones futuras, sin ejecutar:** `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de `deskops`; `python desk/drawer/plans/workspace-documental/validate_plan.py --check` en PASS; comprobar `execution_authorized=false`.

## FUTURO

La sesión de coordinación ejecuta las validaciones y registra bloqueos externos con responsable. Los hijos PK/WS producen sus propias disposiciones. Las personas resuelven P01/P02/P07/P08/P09 y los principios P03–P06; WS07 formaliza ese registro. WS11/WS12 completan contratos y permisos. Nada de eso se decide en esta revisión.
