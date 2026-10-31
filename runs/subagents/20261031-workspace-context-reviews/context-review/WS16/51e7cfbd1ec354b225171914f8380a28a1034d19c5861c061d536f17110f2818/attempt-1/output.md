## REFORMULACION

**Propósito:** validar con una persona real el recorrido temprano de lectura y descubrimiento: UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura y UF10 arranque/ausencia de desk.

**Resultado:** acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/acta.md` y resolución del gate `G_HUMAN_READ`; no produce código de producto ni correcciones.

**Repo:** `graph_ui`.

**Límites:** consume el manifiesto y corpus de WS40 sin crear corpus propio; no implementa la tarea de corrección ante fallos; no muta el baseline; UF08 es solo lectura entre desks; los guardados no se prueban hasta WS30. Las representaciones read-only pueden avanzar en paralelo sin implicar aceptación.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas previstas:** `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `validacion-humana.md`, `user-flows.md` y, cuando exista, el manifiesto de WS40.

**Cambios previstos:** únicamente el acta y evidencias bajo `runs/subagents/workspace-documental-acceptance/lectura/`; ningún cambio en producto.

**Dependencias:** WS14, WS15, WS08, WS40 y WS41; `G_HUMAN_READ` es salida de WS16, no prerrequisito de ejecución.

**Validaciones futuras:** recorrido humano sobre el corpus WS40; aperturas y búsquedas medidas; diagnóstico de link roto y backend ausente; lectura del segundo desk; arranque y ausencia de desk; registro de tiempos, ayudas, fallos y soportes; acta versionada en el commit atómico del repo dueño.

## FUTURO

WS40 produce el corpus y su manifiesto; P08 confirma participante y umbrales; P01 identifica responsables; WS17 enriquece índices después, sin bloquear WS16; WS30 prueba edición y guardados; WS43 publica navegación real. Ante fallos, el responsable del repo del nodo afectado abre la tarea de corrección. Nada de esto es ambigüedad del encargo.
