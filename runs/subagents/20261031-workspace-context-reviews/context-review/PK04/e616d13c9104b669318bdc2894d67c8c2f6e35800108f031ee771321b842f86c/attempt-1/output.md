## REFORMULACION

- **Propósito:** revisar si PK04, tal como está escrito, se entiende como encargo de planificación verificable.
- **Resultado:** un veredicto/disposition sobre la agrupación; no se implementa ni se corrige el DAG.
- **Repo:** PK04 no declara `owner_repo` porque es agrupación de revisión (ROOT/PK no son entregables); el artefacto de revisión vive en deskops.
- **Límites:** no ejecutar el script ni comandos; no revisar los bloques edge vecinos; no aprobar Pxx; no evaluar calidad del producto; no promover nodos.

## AMBIGUEDADES

1. Cita: «`context_review` del hijo en dag.yaml cuyo hash de input y de contrato coinciden con los actuales». No se define qué campo constituye el «contrato» del hijo ni de dónde se obtiene su hash actual. Obligaría a inventar la fuente y el algoritmo; el script `status` puede resolverlo, pero el encargo no lo declara como definición.
2. Cita: «Un hijo con ambigüedad de su propio encargo sin resolver queda pending o blocked por esa causa... un bloqueo externo con responsable sí la admite». Ambos casos pueden acabar en `status=blocked` con «responsable y dependencia»; no hay campo ni criterio que distinga la causa. El revisor tendría que inventar cómo clasificar el bloqueo.
3. Cita: «con responsable y dependencia en esa disposition.md». No se define qué identifica a un «responsable» (nombre, rol, designación WS07) ni el formato mínimo. Obligaría a inventar el criterio de aceptación del bloqueo.

## DRY-RUN

- **Lecturas previstas:** guía de context review, brief, alcance, decisiones, cobertura, nodo PK04 y aristas de WS17/18/22/23/24 en dag.yaml.
- **Cambios previstos:** ninguno de código; solo disposition/veredicto de PK04.
- **Dependencias:** `context_review.py`, disposition.md guardadas en los intentos de cada hijo, hashes input/contrato, designaciones de WS07.
- **Validaciones futuras:** ejecutar `status`, comprobar coincidencia de hashes, existencia de disposition en el intento, y clasificar bloqueos por causa.

## FUTURO

La sesión de coordinación ejecuta `context_review.py` y registra bloqueos; los dueños de cada hijo emiten sus revisiones; WS07 designa responsables; el humano resuelve las Pxx pendientes.
