## REFORMULACION

**Propósito:** verificar que PK01 está bien formulado como encargo de planificación: agrupación de revisión de sus hijos directos, no tarea ejecutable.

**Resultado:** PK01 será verdadero cuando cada hijo directo (WS01–WS06) tenga revisión vigente sin ambigüedad de encargo, o un bloqueo explícito con responsable y dependencia registrados en su disposición.

**Repo:** PK01 no declara `owner_repo`; es un nodo agregado sin ejecución. Sus hijos declaran `deskops`.

**Límites:** no revisar los bloques `edge` de los vecinos, no ejecutar código, no promover nodos, no resolver propuestas Pxx ni evaluar la calidad del producto. La revisión se limita a la formulación del encargo y a su comprobabilidad.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md` y contrato de PK01 con sus hijos en `dag.yaml`.

**Cambios previstos:** ninguno. Solo se guardaría la disposición de revisión de PK01.

**Dependencias:** estado de `context_review` de WS01–WS06 según `context_review.py status`; disposiciones guardadas; designación de responsable cuando un hijo figure bloqueado.

**Validaciones futuras:** comprobar por cada hijo que la revisión sea vigente con input y contrato actuales; aceptar `blocked` solo con responsable y dependencia explícitos; rechazar como no resuelta cualquier ambigüedad de encargo. No se ejecuta `context_review.py` en este nodo.

## FUTURO

Cada revisor de WS01–WS06 produce su disposición; `context_review.py` reporta el estado; un humano designa al responsable si hay bloqueo. PK01 termina cuando terminan sus hijos, conforme a la guía. Las propuestas Pxx y los gates de producto quedan fuera de esta revisión.
