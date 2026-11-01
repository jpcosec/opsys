REFORMULACION
Objetivo: corregir los cuatro defectos señalados por la revisión root —cláusula incondicional de WS12, interfaz de timeout sin productor, dry-run faltante de WS19.1 y atribución falsa de comparación— sin implementar código. Alcance: `desk/drawer/plans/workspace-documental/dag.yaml` y proyecciones, evidencia en `runs/subagents/20261031-correccion-revision9/` y atestaciones en `runs/subagents/20261031-workspace-context-reviews/context-review/`; `review-source.md` es contrato obligatorio. Repo: `deskops`, cwd `/home/jp/proyectos/SLDB_1/deskops`; no se fija raíz git para el diff. Límites: no código, validadores salvo fallo real con tarea específica, P01-P09, auditorías, `reconciliacion.md` salvo exigencia, WS07, WS08-12, UI, Scion, push; no elegir duración de timeout.

AMBIGUEDADES
1. “ramal E” y “sección de contrato por delta”: no definen ubicación ni formato. Obligaría a inventar esquema y alcance.
2. “sin bloquear el cierre del contrato núcleo”: no identifica qué contrato es núcleo. Obligaría a inventar su frontera.
3. “política aplicable y probada”: no define prueba ni evidencia. Obligaría a inventar el criterio de “probada”.
4. “supersesión fechada” / “atestación posterior”: no fija formato, nombre ni archivo exacto. Obligaría a inventar plantilla.
5. El comando `git diff … deskops/…` desde cwd `deskops`: no fija raíz git. Obligaría a inventar si se ejecuta desde el padre o desde el repo.
6. “Tester independiente”: no define independencia. Obligaría a inventar separación de rol.
No son lagunas: editar WS12/WS34, nuevo dry-run WS19.1, ledger, nota WS42, `promotion-notes.md` y Tester son tareas futuras asignadas.

DRY-RUN
Fuentes: task, `review-source.md`, `dag.yaml`, `handoff.md`, ritual `context-review.md`, pills y ledger objetivo. Cambios: en `dag.yaml`, sustituir la cláusula WS12 por “G_PAYLOAD_PRECONDITION y, solo en variante editable, G_SOURCE”; añadir en aceptación WS12 la producción de política/umbral timeout dispatch/reply y clasificación observable para ramal E; condicionar WS34.1/2 a contrato aplicable probado; nueva instrucción/proceso WS19.1 que describa el delta sin ejecutar, conservando el intento anterior sin crédito; escribir `comparison-ledger.md` con supersesión y, por nodo, rol/actor real, sha de input/output/disposición, alcance, resultado y fecha; corregir nota WS42 y `promotion-notes.md`; regenerar proyecciones y revisiones por hashes.
Comandos: `python desk/drawer/plans/workspace-documental/build_plan.py --check`; `…/validate_plan.py --check`; `…/context_review.py status`; `test -s runs/subagents/20261031-correccion-revision9/comparison-ledger.md`; `git diff --name-only 5f05281c..HEAD -- deskops/ tests/ docs/ …` vacío; Tester read-only. Resultado esperado: checks verdes, status sin stale, diff vacío y `tester-result-summary.md` con PASS. No ejecutado aquí.
