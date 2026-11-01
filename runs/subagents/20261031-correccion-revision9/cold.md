# REFORMULACION

**Objetivo.** Corregir cuatro defectos señalados por la revisión root en la revisión 9 del plan `workspace-documental`, con evidencia verificable y sin implementar producto: (1) condicionar `G_SOURCE` a variante editable en la aceptación de WS12; (2) hacer que WS12 produzca explícitamente la política/umbral de timeout y clasificación observable del ramal E, con WS34.1/WS34.2 dependiendo de ella sin bloquear el contrato núcleo; (3) dar a WS19.1 un dry-run real mediante proceso barato nuevo; (4) sustituir la atribución falsa de revisión por comparación efectiva nodo a nodo y ledger firmado. Además: corregir con nota fechada la afirmación falsa sobre WS42 en `result-summary.md`, justificar la exclusión de WS42 por guardas/contrato propio y WS19 transitivo, y actualizar `promotion-notes.md`.

**Alcance.** Solo documentación en `deskops`: `desk/drawer/plans/workspace-documental/dag.yaml` y proyecciones generadas; evidencia en `runs/subagents/20261031-correccion-revision9/`; disposiciones/atestaciones en `runs/subagents/20261031-workspace-context-reviews/context-review/`. Fuera: código, validadores (salvo fallo real con tarea propia), P01–P09, auditorías, WS07, WS08–12, UI, Scion, push.

**Repo/ruta.** `/home/jp/proyectos/SLDB_1/deskops`. Rituales: `execution.md`, `context-review.md`. Pills 001, 005, 007 y ready-phases.

**Límites.** El Supervisor edita contratos, compara, firma ledger y cierra; un agente puede preparar borradores; Tester independiente read-only verifica los cuatro puntos. `review-source.md` es contrato obligatorio.

# AMBIGUEDADES

1. **Directorio de evidencia en conflicto.** Scope dice "disposiciones nuevas o atestaciones en `runs/subagents/20261031-workspace-context-reviews/context-review/`", pero `context-review.md` paso 2 fija `runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/`. Obligaría a inventar cuál ruta es canónica o si se duplica.
2. **"todos los nodos finales" / "todos los nodos".** "comparación real de TODOS los outputs+disposiciones finales por nodo" no define si "finales" = última revisión por nodo o nodos hoja del DAG, ni si cubre los 73. Obligaría a inventar el conjunto exacto a comparar y los shas de input/output/disposition cuando no existan registrados.
3. **"no se usa el runner cuando devolvería answered".** "Si solo cambia la instrucción... no se usa el runner cuando devolvería answered del mismo input". No se especifica cómo detectar esa condición sin ejecutar; obligaría a inventar un criterio de decisión.
4. **Ubicación del cambio de WS42.** "WS42 sale de la justificación" no nombra archivo ni sección ("la justificación" podría ser `result-summary.md`, `promotion-notes.md` u otro). Obligaría a inventar el destino del cambio.
5. **"política... probada en el contrato de su delta".** "WS34.1 y WS34.2 declaran que solo avanzan con esa política aplicable y probada" no define quién/cómo se "prueba" sin ejecutar código. Obligaría a inventar el mecanismo de prueba documental.
6. **"congelar TODAS las correcciones fuente".** No se define el procedimiento de congelación (hash, commit, marca en dag.yaml). Obligaría a inventar el mecanismo.

Ninguna bloquearía el dry-run; sí requieren corrección textual antes de dispatch.

# DRY-RUN

**Fuentes a leer:** `review-source.md` (contrato), `dag.yaml`, `handoff.md` de `20261031-ajuste-canonico-ws06`, `result-summary.md`, `promotion-notes.md`, disposiciones existentes en ambos directorios de `context-review`, pills y rituales citados.

**Cambios concretos:**
1. WS12 acceptance (≈768–771): sustituir cláusula por "G_PAYLOAD_PRECONDITION y, solo en variante editable, G_SOURCE"; añadir sección de contrato por delta para política/umbral dispatch/reply y clasificación observable del ramal E.
2. WS34.1/WS34.2: declarar dependencia de esa política; sin tocar gates.
3. WS19.1: lanzar nuevo `attempt-n` barato con brief que pida ejecución hipotética (campos, precondición, campos protegidos, buffer/conflicto, validación), registrar bytes/argv, conservar intento previo sin crédito.
4. Escribir `comparison-ledger.md` con supersesión fechada y por nodo: rol/actor real, sha input/output/disposición, alcance, resultado, fecha; corregir atribuciones falsas con atestación posterior, sin retrofechar.
5. Nota fechada en `result-summary.md` corrigiendo WS42; actualizar `promotion-notes.md`.

**Comandos previstos:**
- `python desk/drawer/plans/workspace-documental/build_plan.py --check`
- `python desk/drawer/plans/workspace-documental/validate_plan.py --check`
- `python desk/drawer/plans/workspace-documental/context_review.py status`
- `test -s .../comparison-ledger.md`
- `git diff --name-only 5f05281c..HEAD -- ...` (vacío)

**Resultado esperado:** tres checks en verde, ledger existente y firmado, sin cambios en validadores/código/auditorías/decisiones, Tester read-only deja `tester-result-summary.md` con PASS sobre los cuatro puntos y el cambio de `G_SOURCE`.
