## REFORMULACION
Propósito: dictaminar si PK05, como agrupación de revisión, está bien planteado como encargo de planificación: propósito, resultado, repo dueño, límites, dependencias y aceptación comprobable. Resultado: una `disposition.md` de context review para PK05, sin ejecutar nada. Repo: PK05 no declara `owner_repo`; por ser agrupación, no aplica. Límites: no revisar los bloques edge de vecinos, no ejecutar `context_review.py`, no aprobar Pxx ni sustituir gates humanos.

## AMBIGUEDADES
1. «hash de input y de contrato coinciden con los actuales»: el input no define qué artefacto es el «contrato» ni cómo se calcula su hash. Obligaría a inventar el objeto y el algoritmo que la sesión coordinadora debe comparar.
2. «disposition.md guardada en su intento»: un hijo puede tener varios intentos; no se indica cuál cuenta (¿el último, cualquiera?). Obligaría a inventar la regla de vigencia entre intentos.
3. «read_only excluye WS20 de la entrega» (decisiones.md) frente a «cada hijo directo tiene revisión vigente»: con P04 en read_only, WS20 sigue listado como hijo, pero se excluye de la entrega. Obligaría a decidir si su revisión sigue siendo exigible para que PK05 sea verdadera.

## DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo PK05 y aristas de sus hijos. Cambios previstos: redactar la disposición de PK05 en este intento; ningún cambio de código ni de `dag.yaml`. Dependencias: `context_review.py`, los inputs y contratos hasheados de WS19/20/21/25/26/27/28/30/42, la decisión P04 para WS20/21 y el contrato de WS12. Validaciones futuras: ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops; comprobar hashes vigentes y disposiciones guardadas; registrar bloqueos con responsable.

## FUTURO
El humano resuelve P04 (`source_mode`) y las Pxx pendientes; la sesión de coordinación ejecuta `context_review.py` y registra `blocked` con responsable; cada hijo obtiene su propia revisión; WS12 cierra la whitelist; WS30 produce el registro humano de validación.
