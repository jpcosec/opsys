## REFORMULACION

**Propósito:** comprobar que PK08 se entiende como encargo de revisión: agrupa el ramal Scion sin ejecutar sus hijos. **Resultado:** una agrupación de revisión, no un entregable operativo; será verdadera cuando cada hijo directo tenga revisión vigente sin ambigüedad propia o bloqueo externo con responsable. **Repo:** PK08 no declara `owner_repo`; es agrupación de revisión y sus artefactos viven en `desk/drawer/plans/workspace-documental/`. **Límites:** no ejecutar, no revisar los contratos de los nodos vecinos, no aprobar Pxx, no evaluar el producto Scion.

## AMBIGUEDADES

1. «cuyo hash de input y de contrato coinciden con los actuales». El input no define qué artefacto constituye el «contrato» del hijo ni cómo se calcula o conserva su hash. Obligaría a inventar el objeto hasheado y el procedimiento de comparación, salvo que se presuma que `context_review.py status` lo define por completo; el input no lo afirma.

## DRY-RUN

- **Lecturas previstas:** nodo PK08 y aristas de sus hijos directos WS32–WS38 y WS44; guía, brief, alcance, decisiones y cobertura.
- **Cambios previstos:** ninguno por este revisor; una `disposition.md` correspondería a la sesión de coordinación.
- **Dependencias:** revisiones vigentes de cada hijo, disposiciones guardadas, hashes de input/contrato y el script `context_review.py`.
- **Validaciones futuras:** ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops; comprobar que todo hijo directo está vigente sin ambigüedad propia o bloqueado externamente con responsable.

## FUTURO

La sesión de coordinación ejecuta el comando de estado y registra bloqueos con responsable en la `disposition.md`. Otros nodos producen las revisiones de los hijos. WS07 designa operador Scion y su acceso read-only. WS44 realiza el probe y produce G_SCION; WS32–WS38 producen sus salidas. Las decisiones Pxx siguen pendientes de acto humano y no se resuelven aquí.
