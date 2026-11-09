## REFORMULACION
Propósito: habilitar en deskops los recibos que exigen las reglas de activación de CC32 (reproduction, goldens, owner) sin llamar al modelo. Resultado: subcomando `deskops review record <task> --kind reproduction|goldens|owner --evidence <ruta>... --reason "<texto>" --root <r>` que escribe un ReviewDoc pending vía un método nuevo `record_receipt` en `services/review.py` reusando `_write_review`; despacho en `cli/commands/review.py` y `cli/registry.py`; `tests/test_review_record.py`; goldens de ayuda `deskops_review.txt` y `deskops_review_record.txt`; doc y CHANGELOG. Repo: deskops, base CC35a squash 8d0e23fe. Límites: no toca `_task_path`/`_resolve_review_path` ni la resolución de documentos (CC35b), ni reglas CC32, ni los kinds preflight/bundle/node; no se modifica el modelo ReviewDoc.

## AMBIGUEDADES
1. «input_sha256 el sha256 de la concatenación ordenada de los archivos de evidencia (ruta + contenido)» — no fija criterio de orden (¿argv o alfabético?) ni separadores/formato; obligaría a inventar el algoritmo del hash.
2. «summary «<kind> receipt recorded by <actor>; evidence: <rutas>»» — no define de dónde sale `<actor>`; obligaría a inventar su origen (env, config, usuario).
3. «la sección de review de docs/workflow-policy-reference.md o la referencia del CLI donde se documenta review» — el «o» no fija archivo destino; obligaría a elegir.
4. «un campo existente del modelo si alguno la admite (references o evidence)» — si ambos existieran, no dice cuál; obligaría a elegir.

## DRY-RUN
Hipotético, sin ejecutar. Lecturas: `services/review.py` (`_write_review` :562, `dispose` :616), `models/review.py:33`, `cli/commands/review.py`, `cli/registry.py:744-850`, goldens de help, doc y CHANGELOG. Cambios previstos: método `record_receipt`, subcomando y su registro, `test_review_record.py`, `deskops_review.txt` y `deskops_review_record.txt`, doc y CHANGELOG. Dependencias: CC35a (escritura por `sldb.api.transaction`, ancla pinneada). Validaciones futuras: pytest de `test_review_record`, `test_review_command`, `test_review_doc`, `test_cli` desde copia en `/dev/shm`, `test_output_goldens` y `test_cli_help_examples`; diff de goldens; `wc -l` antes/después.

## FUTURO
El dueño revisa y ratifica r1–r8 (marcadas revisables). El coordinador resuelve el rebase con CC35b (r6). La integración con CC32 y la prueba de que su regla cuenta el recibo ocurren en otro nodo (r7). El veredicto lo ejerce el operador con `review dispose`.
