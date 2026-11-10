## REFORMULACION

UI01 es una tarea de código en el repo `deskops`, dentro del workspace `desk`. Debe producir una capa de servicio de solo lectura (`deskops/services/desk_view.py`) que componga cinco vistas —board, task, drawer, inbox y agents— a partir de las operaciones existentes de `DeskopsOperations`, sin duplicar lógica. También debe exponer `deskops view {board,task <id>,drawer,inbox,agents} --root --format json|text` mediante `cli/registry.py` y `cli/commands/view.py`, documentar los contratos en `docs/deskops-ui.md` y cubrirlos con tests sobre desks temporales reales. Las referencias no resueltas deben ir a `errors`, nunca mostrarse como datos. Límite: nada escribe; las fuentes y el mapeo se limitan a `desk/drawer/plans/deskops-ui/alcance.md` y al brief del plan.

## AMBIGUEDADES

1. «columnas por nodo del ciclo de vida en el orden del spec»: el spec no está en el input; obliga a inventar el orden y los nodos.
2. «las últimas N corridas»: no se define `N`; obliga a inventar el límite.
3. «estado de ack»: no se define qué estados existen ni de dónde se leen; obliga a inventar semántica.
4. «revision = sha256 de Board + archivo de tarea como la guarda de graph_ui»: no se especifica serialización ni concatenación exacta; obliga a inventar el cálculo.
5. «--format json|text»: solo se detalla el contrato JSON; obliga a inventar el formato textual.
6. «las operaciones existentes listadas en alcance.md»: el contenido de `alcance.md` no está incluido; obliga a inventar el mapeo exacto.

## DRY-RUN

Nodo ejecutable, no agregado: no tiene hijos. Lecturas previstas: TaskDoc, `alcance.md`, `brief.md`, `DeskopsOperations`, registro CLI, comandos existentes, tests y goldens de help. Cambios previstos: crear `desk_view.py` y `commands/view.py`; registrar el subcomando; añadir tests y fixtures golden; crear `docs/deskops-ui.md`. Dependencias: API real de operaciones, orden del ciclo de vida, contrato de revisión de `graph_ui` y entorno pytest. Validaciones futuras: `pytest -q tests/test_desk_view.py`, `pytest -q tests/test_output_goldens.py`, comprobación de no escritura por hash y suite completa en `robocop2`. Sin ejecución.

## FUTURO

Otro nodo o un humano debe aportar el contenido de `alcance.md`/`brief.md`, el spec del ciclo de vida, el contrato exacto de revisión de `graph_ui`, y decidir `N`, semántica de ack y formato `text`. También corresponde aprobar el contrato documentado y ejecutar la suite en `robocop2`.
