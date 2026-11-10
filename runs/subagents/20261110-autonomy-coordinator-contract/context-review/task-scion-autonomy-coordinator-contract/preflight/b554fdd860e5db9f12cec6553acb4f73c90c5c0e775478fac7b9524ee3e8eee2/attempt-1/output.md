REFORMULACION
El nodo es una tarea ejecutable (`task.code`), no un agregado. Propósito: eliminar contradicciones entre el contrato fuente RoleDoc, los modos/prompts generados y las instrucciones operativas de Scion. Resultado: contrato coherente para que el coordinador recupere estado configurado, seleccione trabajo autorizado listo, despache ejecutor y tester independiente, valide evidencia y concilie cierre antes de continuar. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops-wt-scion-autonomy`, superficie listada en `files`. Límites: sin motor de ciclo de vida sustituto, decisiones automáticas de política, pi-subagents ni tareas CC no relacionadas.

AMBIGUEDADES
1. “progress routine authorized work”: no define qué es rutinario frente a decisión del owner; obligaría a inventar la frontera de escalado.
2. “select reviewed ready unowned tasks”: no fija qué estados/campos concretos expresan “reviewed” y “ready”; obligaría a inventar valores o prioridades.
3. “correct RoleDoc via SLDB”: no identifica el RoleDoc exacto ni los campos autoritativos a corregir; obligaría a inventar destino y contenido del contrato.
4. “real unattended coordinator -> executor -> independent tester -> closeout/continue integration”: no especifica escenario, fixture ni criterio de éxito; obligaría a inventar el experimento y su evidencia.

DRY-RUN
Lecturas: TaskDoc, referencias, dependencia `task-scion-autonomy-review-status`, átomo, aceptación live, tests, goldens, manual y CHANGELOG. Cambios previstos: RoleDoc vía SLDB; `runtime/scion.py` para contexto, nombres/labels y helper de ejemplos; CLI/registro para `--context-file` y modo tester; tests y goldens; documentación generada. Dependencias: helpers existentes de hash/contrato, semántica nativa de Scion para duplicados/notificaciones, Board/RunDoc y la tarea runtime declarada. Validaciones futuras: pytest focalizado, goldens de ayuda/salida, ejemplos de comandos y prueba integrada no atendida. Nada se ejecuta ahora.

FUTURO
`task-scion-autonomy-review-status` aporta estado de revisión/aceptación. La tarea runtime declarada aporta hooks/bootstrap y permite la integración no atendida final. Otro nodo o el operador produce la evidencia de aceptación live. El humano resuelve decisiones de owner, conflictos reales de ownership y credenciales/permisos.
