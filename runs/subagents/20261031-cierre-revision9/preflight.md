## REFORMULACION

**Objetivo:** cerrar la revisión 9 del plan workspace: crédito operativo a cinco nodos (WS13, WS15, WS33, WS12, WS37), reclasificación de WS35 por supersesión fechada, corrección del conteo por adenda y build/validate/status verdes con Tester PASS.

**Alcance:** planificación en deskops (workspace desk). Archivos: `review-source.md`, `comparison-ledger.md` (adenda), `dag.yaml` (solo `context_review` y proyecciones), `promotion-notes.md` de ws06, disposiciones e intentos bajo `runs/subagents/20261031-workspace-context-reviews/context-review/`, `tester-result-summary.md`. Fuera: código de producto, Scion, WS07/WS08-12, los otros 68 outputs, push y reabrir correcciones aceptadas. Se preservan cuatro rutas sucias ajenas. Supervisor ejecuta; Tester solo lectura.

## AMBIGUEDADES

1. «los cinco nodos pendientes» no se enumeran en Goal; solo se infieren de Punto 1/3. Obliga a consultar `review-source.md` o inventar cuáles son.
2. «--reason <razón>»: el texto no está dado; obliga a inventar la razón.
3. «context_review.py run WS13 WS15 WS33 WS12 WS37» frente a Punto 3 («WS12 y WS37 reciben intentos frescos por el canal reparado»): no queda claro si es una invocación única o separada.
4. «El dry-run de un agregado debe recorrer por sus hijos el trabajo, las transferencias y la validación»: no define qué nodo es agregado, qué salida constituye dry-run ni dónde se registra.
5. «Si aparece ambigüedad real»: sin umbral ni juez; obliga a inventar el criterio.
6. WS35: «decisión de presentación pendiente al promover» no indica campo de `dag.yaml` ni cómo se codifica la supersesión fechada; «sin cambiar contrato» tensiona con reclasificar.
7. «firma lo que leyó»: formato y artefacto de la firma no se especifican.
8. Contradicción: «ningún intento registrado tenga recibo incompleto» frente a WS12/WS37 «con recibo incompleto; no se rellenan». Exigiría inventar la excepción.
9. «comprobar los 73»: no se declara la unidad (¿intentos, outputs?).
10. «cuatro rutas sucias ajenas»: no se nombran.
11. «commit» aparece en pasos 1 y 6 sin fijar número ni mensajes.

## DRY-RUN

Leer `review-source.md`, ledger, `dag.yaml`, pills y `promotion-notes.md`. Ejecutar `python desk/drawer/plans/workspace-documental/context_review.py run WS13 WS15 WS33 WS12 WS37 --new-attempt --reason "<razón>"`; verificar intentos y recibos; ejecutar el dry-run del agregado; añadir adenda fechada corrigiendo 39/34→40/33 y declarando versión de instrucción por intento; registrar supersesión WS35 y disposiciones. Después: `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`, `pytest -q tests/test_context_review_helper.py`; commit; Tester escribe `tester-result-summary.md`.

**Errores esperables:** flags o razón inválidos, status rojo, recibos incompletos, contradicción del punto 8, supersesión no codificable, rutas sucias, tests fallando.

**Esperado:** cinco intentos frescos con recibo completo, dry-run sustantivo, WS35 reclasificado, conteo corregido, tres checks y pytest verdes, PASS.
