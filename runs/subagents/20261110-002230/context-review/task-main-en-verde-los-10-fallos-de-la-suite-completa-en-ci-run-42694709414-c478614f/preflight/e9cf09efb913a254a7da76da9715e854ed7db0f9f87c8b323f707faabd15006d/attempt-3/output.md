## REFORMULACION

Propósito: devolver main de deskops a verde arreglando los 10 fallos del run 42694709414 (c478614f), con causa raíz escrita antes de cada arreglo. Resultado: `python -m pytest tests -q` sin fallos y workflow tests en success en 3.12 y 3.13, con URL en references. Repo: deskops, en copia/worktree bajo /dev/shm (TMPDIR=/dev/shm). Límites: sin skip/xfail ni relajar aserciones sin causa; el worker no corre la suite completa; push a wt/main-en-verde; incluye p4 (desk update --apply sobre el desk real), p5 (dejar activables las tareas abiertas reescribiendo recibos por CLI) y p7.

## AMBIGUEDADES

1. «una copia del worktree en /dev/shm» (p1) frente a «git worktree add --detach /dev/shm/deskops-mv HEAD» (p6): dos mecanismos y bases distintas (origin/main 45198785 vs HEAD); obliga a inventar cuál usar.
2. «el worker para y avisa» (p2): no dice si detiene toda la tarea o solo ese fallo; obliga a inventar el alcance del paro.
3. «recibos accepted pero lost o changed» (p5): no define lost ni changed; obliga a inventar el criterio.
4. «Hoy las tareas abiertas son CC30, CC36 y CC38» (p5): instantánea fechada; obliga a inventar si se revalida al ejecutar.
5. «Las opciones a evaluar y proponer con su costo» (p3): no dice si el worker elige o espera; obliga a inventar el punto de decisión.
6. «se commitean exactamente los archivos que escribió el CLI» (p4): sin granularidad ni mensajes de commit; obliga a inventar.
7. «el commit de cierre» (Done When) frente a «el coordinador de proyecto integra» (p7): no identifica commit ni quién cierra; obliga a inventar.

## DRY-RUN

Lecturas: TaskDoc, log del run, git log/blame, tests citados, `deskops show task <id>`, estado de recibos, .gitignore/.pi. Cambios previstos: causa raíz por fallo en el informe; arreglo en test o código (10); 7 rule-activation y .sldb escritos por CLI; recibos reescritos por CLI (CC30, CC36, CC38, CC37, CC33a, esta); commits y push a wt/main-en-verde. Dependencias: modelo para `deskops review` (una a la vez, pgrep), gh, evidencia de goldens existente. Validaciones futuras: archivo solo antes/después desde /dev/shm, diff sin skip/xfail, segunda corrida de update sin cambios, tabla de recibos; suite completa y workflow los corre el coordinador. No se ejecuta nada.

## FUTURO

El coordinador integra, corre la suite completa y espera el workflow en 3.12 y 3.13; la URL va a references. Deciden humanos: p2 (gramática del CLI, review record con evidencia de operador), si .pi/skills es parte del repo o el test asume archivo local, y qué hacer si falta la evidencia de goldens.
