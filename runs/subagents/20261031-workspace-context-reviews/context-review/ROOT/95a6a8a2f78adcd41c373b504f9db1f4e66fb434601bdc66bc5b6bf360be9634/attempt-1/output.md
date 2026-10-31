REFORMULACION
- **Propósito:** revisar ROOT como encargo de planificación del workspace documental, no como producto ni ejecución.
- **Resultado:** agrupación de revisión verdadera cuando PK01–PK08 tengan revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable; además `execution_authorized=false` y `validate_plan.py --check` en PASS.
- **Repo:** deskops, según la ruta del input y el comando indicado «desde la raíz de deskops».
- **Límites:** no implementa UI, no resuelve decisiones humanas, no ejecuta hijos ni sustituye sus revisiones. Las aristas no se revisan aquí.

AMBIGUEDADES
Ninguna. La aceptación es comprobable mediante `context_review.py status` y `validate_plan.py --check`; define revisión vigente, disposición guardada y bloqueo explícito. Las decisiones Pxx pendientes no cuentan según la guía y ROOT no exige resolverlas.

DRY-RUN
- **Lecturas previstas:** `dag.yaml` completo para confirmar `execution_authorized=false`; salida de `context_review.py status`; `disposition.md` de cada PK; resultado de `validate_plan.py --check`.
- **Cambios previstos:** ninguno. ROOT es agregado y no se ejecuta.
- **Dependencias:** revisión vigente de PK01–PK08, con coincidencia de hashes de input y contrato, y `disposition.md` en su intento. Un bloqueo solo admite responsable y dependencia registrados.
- **Validaciones futuras:** `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops y `python desk/drawer/plans/workspace-documental/validate_plan.py --check` en PASS.

FUTURO
La sesión de coordinación ejecutará las comprobaciones y registrará `context_review.status=blocked` si procede; otros nodos producirán las revisiones de PK01–PK08 y sus disposiciones. Las decisiones P01–P09 y los gates G_PRODUCT/G_WRITE_POLICY quedan para decisión humana y WS07, fuera de esta revisión.
