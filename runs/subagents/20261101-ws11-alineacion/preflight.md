## REFORMULACION

**Objetivo:** aplicar en una pasada las cuatro precisiones de root: (1) `local` se serializa como ausencia del parámetro alias cuando no hay alias configurado, con equivalencia en URL/historia y `local:` como desk del documento origen; (2) WS41 valida unicidad de `(root.resolve(), store.resolve())` sin sinónimos en baseline, sin modelo/nodo; (3) §5.4 nombra quién prepara stores fuera del request; (4) `output_scope` de WS15.1 incorpora `frontends/mindmap/shell/api.js`.

**Alcance:** `contratos/navegacion.md`, `output_scope` de WS15.1 en `dag.yaml`, derivados de `build_plan`/`render_diagram`, punteros de `context_review` medidos stale.

**Repo:** SLDB_1 (`desk`), rutas `desk/drawer/plans/workspace-documental`.

**Límites:** no tocar vistas.md, guía, decisiones, helper, validadores, código, repos hermanos; no cerrar fase/WS12/UI/Scion/push; no suite general; no inventar comandos ni productores automáticos.

## AMBIGUEDADES

1. Cita: "El TaskDoc consumidor identifica operación pública/versión y evidencia de la preparación sin inventar un comando aquí." No se precisa si ese enunciado se incorpora a §5.4 de `navegacion.md` o a otro apartado; obligaría a inventar la ubicación.
2. Cita: "En la revisión fresca WS13.1 el dry-run menciona request() preserva status: hacer inequívoco en la comparación…". No se aclara si la aclaración se edita en el contrato o solo en el artefacto de revisión; obligaría a inventar la superficie.

## DRY-RUN

1. Editar `navegacion.md`: §3.2/8.5 serialización (ausencia de alias si no hay config; equivalencia URL/historia; `local:` como desk origen; alias canónico configurado para el desk del proceso); §5.4 actores; cláusula WS41 de unicidad por `(root.resolve(), store.resolve())`.
2. Editar `dag.yaml`: añadir `frontends/mindmap/shell/api.js` al `output_scope` de WS15.1, sin gates/dependencias ni cambio de aceptación.
3. Ejecutar `build_plan.py` para regenerar, `render_diagram`, y `context_review.py status`; medir stale (no asumir WS13/WS15/WS15.1) y renovar solo lo afectado.
4. Congelar bytes; Tester focal A–F + 4 puntos; revisión fresca WS13.1/WS41.
5. Checks: `test -s`, `build_plan --check`, `validate_plan --check`, `status`.

**Errores esperables:** derivados desincronizados → `--check` rojo; tester FAIL; staleness no medida. **Resultado esperado:** cuatro precisiones exactas, checks verdes, contrato en borrador, solo revisiones medidas renovadas.
