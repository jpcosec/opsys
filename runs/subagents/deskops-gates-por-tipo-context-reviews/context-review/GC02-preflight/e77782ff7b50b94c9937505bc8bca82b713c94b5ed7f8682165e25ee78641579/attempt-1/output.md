## REFORMULACION

Propósito: añadir en deskops el modelo ReviewDoc como recibo inmutable de revisiones, anclado a un sujeto (`subject`). Resultado: `deskops/models/review.py` con ReviewDoc (StructuredNLDoc, como RunDoc), registro en MODEL_REFS, creación de `desk/reviews/` en init/desk update, validaciones al escribir (kind, verdict, reason/disposed_by, forma de subject), rechazo de edición del veredicto, tests, fixture de hashes y CHANGELOG; sin comando que escriba ReviewDocs (eso es GC03). Repo: deskops, worktree `deskops-wt-gates`, rama `wt/gates-por-tipo`. Límites: no tocar el repo sldb; nada escrito a mano en `desk/` ni `.sldb/`; fuera de alcance los demás nodos GC y brief.md §Fuera de alcance.

## AMBIGUEDADES

1. «hipótesis: la versión actual de sldb acepta en un campo `__references__` un valor con prefijo doc: o GC02 lo declara solo en `__doc_anchors__` y espera a GO07; el TaskDoc fija cuál» — el TaskDoc no fija nada; obliga a inventar cuál de las dos opciones implementar.
2. «subject_ref (str libre: ruta#node:ID cuando subject está vacío)» — no dice si es obligatorio ni si se valida formato; inventar exclusión mutua.
3. «Un ReviewDoc no se edita con edit review verdict: edit lo rechaza» — no queda clara la superficie CLI exacta ni el mensaje; inventar comando/campo.
4. «id (review-<task>-<kind>-<n>)» frente a «desk/reviews/<task-id>/<kind>-<n>.md» — no se especifica si el id deriva de la ruta o al revés, ni cómo parsear task-id con guiones; inventar derivación.
5. «subject "doc:TaskCodeDoc:task-x" valida» — no dice si el modelo referido debe existir en MODEL_REFS; inventar alcance de validación.
6. «created_at, disposed_at, disposed_by» sin tipos; «run_dir (ruta relativa bajo runs/)» sin raíz (repo, desk, worktree); inventar tipos y base.

## DRY-RUN

Lecturas: archivos listados (review.py, `__init__`, bootstrap, workspace, operations, tests, fixture de hashes, CHANGELOG), RunDoc como patrón, `identity.py`, doc_io y `sldb edges show`. Cambios previstos: modelo con campos y `__doc_anchors__`/`__references__`, validadores, registro MODEL_REFS, creación de `desk/reviews/`, rama de edit que rechaza veredicto, tests y fixture actualizado, CHANGELOG. Dependencias: RunDoc, identity, doc_io, sldb grafo-operable rev 9; sin gates. Validaciones futuras: pytest completo en robocop2, round-trip render/extract, casos negativos, desk temporal con doc_io + edges show, idempotencia de `desk update --apply`. Nada ejecutado.

## FUTURO

GC03 implementa `deskops review dispose` que escribe ReviewDocs; GO07 convierte `__doc_anchors__` en references y decide el sufijo `doc:`; un humano resuelve las ambigüedades 1 y 5; si sldb bloquea, se manda nota con `deskops message send --to sldb`.
