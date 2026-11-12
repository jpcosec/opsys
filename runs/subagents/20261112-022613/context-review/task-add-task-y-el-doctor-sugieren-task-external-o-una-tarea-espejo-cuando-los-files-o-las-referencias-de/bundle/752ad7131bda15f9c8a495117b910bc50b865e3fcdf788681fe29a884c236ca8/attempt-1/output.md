## REFORMULACION

Encargo ejecutable (`task.code`) en el repo deskops: al crear una tarea con `add task`, si sus `files` apuntan a otro repo registrado, imprimir una línea no bloqueante que nombre ese repo y sugiera `task.external` o una tarea espejo en el desk de ese repo; y hacer que `deskops doctor` liste como alerta —sin alterar su código de salida— las tareas existentes con esa forma que no son `task.external`. Incluye detección en las formas (i)-(iii), tests con dos repos en `tmp_path`, operator-manual, CHANGELOG y conservación de goldens. Fuera: closeout, cambiar el tipo de una tarea sola y cualquier cambio en sldb. Resultado: a1-a5 hechos, tests y suite en verde, docs/CHANGELOG actualizados y el ítem de drawer de origen dado de baja por CLI.

## AMBIGUEDADES

1. "cuando los files o las referencias de una tarea apuntan a otro repo" (título) frente a "una entrada de files es de otro repo" (a1) y "tiene files de otro repo" (a3): ¿las `references` también disparan aviso/alerta? Obligaría a inventar el alcance real.
2. "empieza por la carpeta padre y resuelve bajo la raíz registrada de otro repo" (a1-iii): no dice cuál es la base de una ruta relativa (raíz del desk, ecosistema, cwd). Obligaría a inventar la resolución.
3. "cada tarea abierta" (a3): no enumera estados (¿`draft`, `active`, `ready_for_testing`?, ¿candidatas del drawer?). Obligaría a inventar el filtro.
4. "a stdout, por ejemplo: la tarea declara files del repo <identidad>..." (a2): el texto es ejemplo y no fija qué ocurre con `--format json`. Obligaría a decidir mensaje exacto y canal en formatos máquina.

## DRY-RUN

Lecturas: `deskops/operations.py` (ruta `add task`), `deskops/identity.py` (registro y raíces), `deskops/cli/commands/operations.py`, `doctor.py`/`doctor_findings.py` (`Findings.alerts`), tests, manual y CHANGELOG.

Cambios previstos (hipotéticos): helper que clasifique un file como local/otro repo reutilizando el registro, llamada en `add task` que imprima el aviso solo si aplica, comprobación en doctor que añada alertas sin tocar errores, tests nuevos para (i)-(iii), locales y `task.external`, y actualización de docs/CHANGELOG.

Dependencias: referencias calificadas de `resolved-by` en deskops main; dos repos registrados en `tmp_path`. Validaciones futuras: tests nuevos, goldens de ayuda/salida sin cambio, suite completa de a un archivo desde `/dev/shm` y los 4 pasos de CI en clon limpio.

## FUTURO

El coordinador ejecuta los 4 pasos de CI en clon limpio y valida la suite. El worker confirma con ejemplos reales de los desks que (i)-(iii) cubren el caso de AntonIA y muestra el diff de cualquier golden antes de actualizarlo. La baja del ítem de drawer por CLI se ejecuta al cerrar, fuera de este nodo.
