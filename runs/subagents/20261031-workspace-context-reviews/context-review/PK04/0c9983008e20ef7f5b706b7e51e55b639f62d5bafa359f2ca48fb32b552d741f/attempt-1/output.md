## REFORMULACION
- **Propósito**: revisar PK04, nodo de agrupación de revisión (no ejecutable) que cubre entradas authored y representaciones de Board, procedimientos, conocimiento y grafo.
- **Resultado**: agrupación verdadera solo si cada hijo directo (WS17, WS18, WS22, WS23, WS24) tiene revisión vigente sin ambigüedad de su propio encargo, o bloqueo externo con responsable y dependencia registrados en su `disposition.md`.
- **Repo**: deskops (plan y herramienta `context_review.py`).
- **Límites**: no se revisan los bloques edge de los hijos ni se ejecuta nada; PK04 no es dependencia operativa.

## AMBIGUEDADES
ninguna

El encargo queda comprobable: nombra el comando de verificación, define revisión vigente por coincidencia de hash de input y contrato, exige `disposition.md` en el intento correspondiente y distingue bloqueo externo (admisible con responsable) de ambigüedad propia del hijo (no admisible). Los hijos listados coinciden con el alcance declarado y ninguno es `aggregate`.

## DRY-RUN
- **Lecturas previstas**: `dag.yaml` (nodo PK04, entradas de los cinco hijos y sus `context_review`), guía, brief, alcance, decisiones y cobertura; salida de `context_review.py status`.
- **Cambios previstos**: ninguno en este nodo; no se promueve ni edita dag.yaml.
- **Dependencias**: disposiciones guardadas de WS17/WS18/WS22/WS23/WS24 con hashes alineados a los contratos actuales; para bloqueos, actor o repo responsable y dependencia anotada.
- **Validaciones futuras**: ejecutar `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops y comprobar que cada hijo aparece vigente o bloqueado con responsable y dependencia.

## FUTURO
- La sesión de coordinación ejecuta `context_review.py` y registra los bloqueos con su responsable.
- Los revisores de cada hijo guardan su `disposition.md` en el intento correspondiente a los hashes vigentes.
- La aceptación de PK04 la resuelve esa herramienta; si cambia un contrato de hijo, sus hashes invalidan la revisión hasta regenerarla.
