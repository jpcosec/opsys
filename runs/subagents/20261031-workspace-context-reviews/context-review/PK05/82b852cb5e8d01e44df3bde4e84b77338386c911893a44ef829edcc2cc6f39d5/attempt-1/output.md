## REFORMULACION
PK05 se revisa como **agrupación de revisión**, no como tarea ejecutable: su propósito es agrupar la revisión de los nodos de autoría y operación manual; su resultado es una agrupación “verdadera” cuando cada hijo directo tiene revisión vigente o bloqueo externo con responsable; el repo dueño se infiere como `deskops` por el comando de aceptación, coherente con que PK no sea entregable operativo. Límites: no evalúo producto, no ejecuto `context_review.py`, no reviso los contratos de los nodos vecinos y no trato gates pendientes ni propuestas Pxx como defectos.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
- **Lecturas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo PK05 y lista de hijos en `dag.yaml`.
- **Cambios previstos:** ninguno; esta revisión no modifica archivos ni estados.
- **Dependencias:** `context_review.py status`; `disposition.md` de cada hijo con hashes vigentes de input y contrato; sesión de coordinación para registrar bloqueos externos con responsable.
- **Validaciones futuras:** ejecutar el comando desde la raíz de `deskops`; comprobar que los nueve hijos directos tengan revisión vigente o bloqueo externo registrado; verificar coincidencia de hashes y existencia de `disposition.md`.

## FUTURO
- **WS07/humano:** resolver P01–P09, incluido `source_mode`, y designar responsables; no es ambigüedad de PK05.
- **WS12:** producir la whitelist/contrato de operaciones que condiciona a varios hijos.
- **Revisiones hijas:** generar sus `disposition.md` y, si aplica, bloqueos con responsable.
- **Coordinación:** ejecutar `context_review.py` y registrar bloqueos externos.
- **WS30:** aportar la validación humana del recorrido manual; PK05 solo revisa su encargo, no su ejecución.
