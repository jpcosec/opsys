REFORMULACION
Propósito: sustituir los dos scripts de revisión en frío (`desk/drawer/plans/workspace-documental/context_review.py` y `tests/test_context_review_helper.py`) por un comando `deskops review` con subcomandos `node`, `preflight`, `bundle`, `status` y `dispose`. Resultado: cada corrida escribe bajo `runs/subagents/<run>/context-review/<clave>/<sha256>/attempt-N/` (input.md, manifest.json, output.md, stderr.log, receipt.json), más un ReviewDoc GC02 con `verdict: pending`; perfil por defecto `desk/runtimes/runtime-pi-deepseek-flash.md` escrito por init; topes D9; fallo de transporte → `technical_ok: false` y `verdict: incomplete` con reason "technical"; borrado de los scripts; nota a sldb; produce G_RECEIPTS. Repo deskops, worktree `deskops-wt-gates`, rama `wt/gates-por-tipo`. Límites: depende de GC02, sin gates; no tocar sldb; no push a main; no `git add -A`; nada escrito a mano en `desk/` ni `.sldb/`; fuera de alcance otros nodos GC y cambios en sldb.

AMBIGUEDADES
1. "claves KEEP del script gobernado": no se enumeran; obliga a inventar cuáles son.
2. "los cuatro archivos base del plan si existen": no se fija su ruta respecto al `dag.yaml`; obliga a inventar ubicación.
3. "rituales enrutados por el Board": no se define el Board ni su API de enrutamiento; obliga a inventar el mecanismo.
4. "pills ligadas + átomos ligados": no se define el criterio de ligazón; obliga a inventar la resolución.
5. "menores de 60 KB": no se dice qué hacer si un archivo excede; obliga a inventar (¿omitir, truncar, fallar?).
6. "el system prompt SYSTEM del script gobernado": no se transcribe su contenido; obliga a inventar el texto del perfil.
7. "una por hash de contrato de la tarea": no se define qué campos componen el contrato ni el algoritmo; obliga a inventar.
8. "status [<task> | <plan-dir>]" sin argumento: no se especifica comportamiento; obliga a inventar.
9. "un tercer intento... falla sin --force" frente a "--max-attempts 2": la interacción entre ambos topes no se ordena; obliga a inventar precedencia.

DRY-RUN
Lecturas: TaskDoc GC03, dag.yaml gates-por-tipo, esquema ReviewDoc de GC02, script gobernado (SYSTEM y claves KEEP), ritual context-review pasos 3 y 5, Board de rituales, perfiles de runtime, `workspace.py`, `registry.py`, fixtures de tests.
Cambios previstos: `deskops/cli/registry.py`, `deskops/cli/commands/review.py`, `deskops/services/review.py`, `deskops/workspace.py`, `desk/runtimes/`, borrado de los dos scripts, `tests/`, `tests/fixtures/golden/help/`, `docs/operator-manual.md`, `CHANGELOG.md`.
Dependencias: GC02, Board, contrato sldb grafo-operable rev 9, perfil pi deepseek-flash, ejecutable pi falso de fixture.
Validaciones futuras: pytest completo en robocop2 sin rojos ni saltados; preflight/status/bundle/node/dispose; exit 1 → `technical_ok:false`; grep vacío de `context_review.py`; CHANGELOG y manual.

FUTURO
GC02 entrega el ReviewDoc y su esquema. sldb decide el contrato grafo-operable rev 9 y pinnea el hash del subject (GO07). El Board decide el enrutamiento de rituales. Un humano decide `--engine`, `--force`/`--reason` y los veredictos de `dispose`. Init materializa el perfil de runtime. La nota a sldb queda como acción externa.
