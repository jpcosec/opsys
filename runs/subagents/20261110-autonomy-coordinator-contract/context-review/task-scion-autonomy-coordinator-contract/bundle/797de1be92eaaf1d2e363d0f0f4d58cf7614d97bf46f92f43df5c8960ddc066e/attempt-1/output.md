REFORMULACION  
El nodo debe producir un contrato fuente coherente para que el coordinador Scion, en el repo `deskops` (`/mnt/ssd/proyectos/SLDB_1/deskops-wt-scion-autonomy`), recupere el estado configurado, seleccione una hoja ready revisada y no poseída, despache ejecutor y tester independiente con identidad determinista, registre intención RunDoc y reconcilie closeout antes de continuar. Resultado: RoleDoc/supervisor, plantillas Scion y ejemplos de comandos corregidos; `--context-file` estricto; `--mode tester`; helpers de identidad/argv; átomo y documentación. Límites: no motor de lifecycle, no decisiones automáticas de política, no pi-subagents ni tareas CC ajenas; el supervisor muta workflow por CLIs pero no implementa.

AMBIGUEDADES  
1. “final unattended acceptance/phase integration requires the declared setup runtime task” pero `depends_on` solo lista `task-scion-autonomy-review-status`. Obligaría a inventar qué tarea es ese setup runtime y si bloquea el cierre.  
2. “real unattended coordinator -> executor -> independent tester -> closeout/continue integration” y la referencia `live-integration-acceptance.md` no está incluida. Obligaría a inventar escenario, repo/tarea, modelo/credenciales y criterio de éxito.  
3. “Capture source atom before operator docs, generate from source” no dice qué se genera ni con qué comando. Obligaría a inventar el artefacto y el generador.

DRY-RUN  
Lecturas: TaskDoc, Board/rituales/pills/átomos enrutados, `deskops/runtime/scion.py`, `deskops/cli/commands/runtime.py`, `desk/roles/deskops-supervisor.md`, tests, golden de ayuda, manual y changelog. Cambios previstos: validación estricta del contexto; env/volumen y ejemplos con rutas; modo tester y autodetección; identidad/nombres/labels/attempt; RunDoc de intención; prompts de coordinador, tester y ejecutor; documentación y changelog. Dependencias: `task-scion-autonomy-review-status`, la tarea de setup runtime y un proyecto/credenciales Scion reales. Validaciones futuras: `pytest tests/test_scion_runtime.py`, goldens de ayuda/salida, pruebas de digest canónico, nombres/labels, contexto inválido antes de escribir, alcance tester y ejemplos de comandos; integración no atendida. No se ejecuta nada.

FUTURO  
La tarea de setup runtime aporta hooks/bootstrap y ejecuta la aceptación no atendida; un humano decide política no resuelta, conflictos reales de ownership y credenciales/permisos; el commit de salida de la dependencia se registra en ese nodo.
