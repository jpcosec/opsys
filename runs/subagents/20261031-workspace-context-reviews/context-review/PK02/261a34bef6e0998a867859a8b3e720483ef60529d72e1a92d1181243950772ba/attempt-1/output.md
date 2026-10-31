## REFORMULACION

PK02 es un nodo agregado de revisión, no una tarea ejecutable: agrupa WS07–WS12 y su aceptación es una condición de verdad sobre las revisiones de esos hijos. Propósito: comprobar que cada hijo tiene `context_review` vigente, sin ambigüedad de encargo o con bloqueo explícito atribuido. Resultado: ninguna entrega propia; solo habilita o no la agrupación. Repo: deskops (el plan vive allí; el agregado no produce artefacto). Límites: no revisar las aristas vecinas, no ejecutar nada, no resolver Pxx ni sustituir la revisión de cada hijo.

## AMBIGUEDADES

1. «sin ambigüedad de encargo o bloqueo explícito con responsable» frente a «Un hijo con ambigüedad de su propio encargo sin resolver queda pending o blocked por esa causa, y entonces esta aceptación no es verdadera; un bloqueo externo con responsable sí la admite». Un hijo bloqueado por ambigüedad propia cumple literalmente «bloqueo explícito con responsable» —la definición exige responsable y dependencia—, pero la frase siguiente lo excluye. Para decidir hay que inventar un discriminador de causa en `disposition.md` o una precedencia no escrita.

## DRY-RUN

- Lecturas previstas: bloque PK02 y entradas `context_review` de WS07–WS12 en `dag.yaml`; `disposition.md` de los intentos; salida de `context_review.py status`.
- Cambios previstos: ninguno; el nodo es agregado.
- Dependencias: disponibilidad del script en deskops; intentos y disposiciones de los seis hijos; clasificación explícita del motivo de bloqueo.
- Validaciones futuras: ejecutar `status`, comprobar coincidencia de hashes de input y contrato, y verificar que los bloqueos externos tengan responsable y dependencia distinguibles de la ambigüedad propia.

## FUTURO

Las revisiones de WS07–WS12 y sus `disposition.md` las producen esos nodos y la sesión de coordinación; la resolución de Pxx y la designación de responsables corresponde al humano en WS07. La ejecución de `context_review.py status` no es trabajo de este revisor.
