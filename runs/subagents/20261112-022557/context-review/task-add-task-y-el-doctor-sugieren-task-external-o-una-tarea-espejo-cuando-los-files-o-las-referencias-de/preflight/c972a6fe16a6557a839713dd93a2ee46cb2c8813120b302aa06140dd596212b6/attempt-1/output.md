## REFORMULACION

Encargo ejecutable (no agregado): en el repo **deskops**, implementar la opción a de la nota a79fe2d6. Propósito: evitar que se cree una `task.code` en el desk equivocado cuando su código vive en otro repo. Resultado: (a1) definir “file de otro repo” en tres formas; (a2) aviso no bloqueante en `add task` tras crear la tarea, sin cambiar tipo ni imprimir para `task.external`; (a3) alerta del doctor para tareas abiertas no `task.external` con files de otro repo, sin cambiar códigos de salida; (a4) tests de las tres formas, negativos y goldens; (a5) docs y CHANGELOG. Límites: fuera closeout, cambio de tipo y cualquier cambio en sldb. Superficie declarada: `deskops/operations.py`, `identity.py`, CLI de operations/doctor, `doctor_findings.py`, tests, manual y CHANGELOG. Done When añade dar de baja por CLI el ítem de drawer de origen.

## AMBIGUEDADES

1. “files o las referencias de una tarea apuntan a otro repo” (título) frente a Goal/a1, que solo hablan de `files`: obligaría a inventar si `references` también dispara aviso/alerta.
2. “las referencias calificadas por repo de resolved-by (tarea xrepo) están en deskops main”: no define cómo verificar esa precondición; obligaría a inventar criterio de comprobación.
3. “empieza por la carpeta padre y resuelve bajo la raíz registrada”: “carpeta padre” no está definida; obligaría a inventar normalización, symlinks y `..`.
4. “cada tarea abierta”: no enumera estados abiertos; obligaría a inventar qué `status` cuentan.
5. “task.external”: no define cómo se identifica (tipo, campo, metadato); obligaría a inventar la detección.
6. “una línea tras crear la tarea, a stdout, por ejemplo”: el texto final no es normativo; obligaría a inventar redacción exacta y su efecto en goldens.
7. “el doctor lista como alerta”: no fija formato ni severidad; obligaría a inventar salida.
8. “el ítem de drawer de origen se da de baja por CLI”: no nombra comando; obligaría a inventar la invocación.
9. “el worker confirma en el informe, con ejemplos reales de los desks”: no define “informe” ni acceso a esos desks; obligaría a inventar evidencia.

## DRY-RUN

Lecturas hipotéticas: TaskDoc, registro de repos, `operations.py`, `identity.py`, CLI de operations/doctor, `doctor_findings.py`, tests y goldens, manual, CHANGELOG. Cambios previstos: helper de clasificación de files (i–iii), aviso en `add task`, alerta en doctor, tests nuevos y actualización documental. Dependencias: tarea xrepo integrada en main y registro consultable. Validaciones futuras: tests nuevos, goldens sin cambios, suite por archivo desde `/dev/shm` y cuatro pasos de CI en clon limpio.

## FUTURO

El coordinador ejecuta los cuatro pasos de CI. Un humano revisa cualquier diff de golden antes de aceptarlo y valida la evidencia con desks reales. La baja del ítem de drawer queda para el cierre por CLI.
