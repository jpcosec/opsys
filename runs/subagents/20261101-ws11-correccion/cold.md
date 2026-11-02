## REFORMULACION

**Objetivo:** corregir en una pasada `contratos/navegacion.md` (WS11) según puntos A–F y 4 decisiones root, ajustar solo la celda F18a de `vistas.md` y producir `result-summary.md` con resolución por punto y tabla por cada fila C y H, sin ejecutar código.

**Alcance:** escritura solo en tres rutas (contrato, una celda de F18a, `runs/subagents/20261101-ws11-correccion/result-summary.md`). Repo `deskops` en `/home/jp/proyectos/SLDB_1/deskops`; lecturas en `../UIs/graph_ui` y `../sldb`.

**Límites:** no tocar dag.yaml, helper, validadores, fuentes comunes, otros contratos, código, repos hermanos ni auditorías; sin commits, revisiones ni tests; congelar parche con diff/hash a root antes de registrar/revisar; sin WS12/UI/Scion/push; mantener estado borrador.

## AMBIGUEDADES

1. «ajustar solo la celda necesaria de F18a» — `vistas.md` no se adjunta; obligaría a inventar qué celda y su forma exacta.
2. «cotejar todas las filas C y H» — el universo no está definido: H-05b/H-03b son subfilas, H-13 aparece fuera de orden y H-22 figura «resuelto»; obligaría a inventar el criterio de inclusión/exclusión.
3. «revisión fresca no ejecutora del contrato corregido con consumidor» y «el encargo de consumidor pertinente» — no se identifica qué consumidor (WS13.1, WS15.1, WS41) ni qué artefacto de encargo; obligaría a inventar cuál.
4. «WS09 renovada solo si vistas.md cambió» — no se define el procedimiento de renovación (entrada DAG, forma); obligaría a inventar el mecanismo.
5. «clave de sesión de modelado con alias además de Model:name» — sin formato; obligaría a inventar sintaxis (`alias:Model:name` vs otra).
6. «mismo origen» exige «render/fuente de la misma lectura/revisión» — no operacionalizado; obligaría a inventar el criterio verificable.
7. «los 4 dirty ajenos» — no enumerados; obligaría a inventar cuáles preservar.
8. «en una pasada» — no aclara si prohíbe iteraciones de escritura antes de congelar.

## DRY-RUN

Ejecutor futuro: (1) lee completos `review-source.md` y el contrato; (2) abre cada cita de cada fila C y H y las cadenas de llamada nombradas (`parse_links`, `split_anchor`, `doc_status`, `recover_links`, `open_store`, `shell/api.js:5-11`); (3) edita secciones 3, 3.3, 4, 5.4, 6, 7, 8, 10 y filas H-03..H-14, aplica decisiones root y clave de sesión con alias; (4) edita la celda F18a de `vistas.md` con `notation-view.js:356` y `shell/registry.js:16`; (5) redacta `result-summary.md` con resolución A–F, tabla por fila y lo no leído; (6) corre `test -s`, `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`; (7) congela hash/diff para root y entrega a Tester y revisión fresca.

Errores esperados: si `vistas.md` no existe en el tree, la ambigüedad 1 bloquea; si no se identifica consumidor, la 3 bloquea; validadores en rojo impiden congelar. Resultado esperado: contrato corregido, checks verdes, sin cierre ni WS12 hasta aprobación root.
