## REFORMULACION
**Propósito:** que el humano dueño del producto confirme o corrija baseline, host, fuente/edición, escritura/Git/coordinador y cierre, y designe responsables de graph_ui, sldb, spec2viz y operador Scion.
**Resultado:** `decisiones.md` con alternativas, actor humano, fecha y evidencia; `source_mode` sincronizado en `dag.yaml`.
**Repo:** deskops. **Límites:** no implementar, no tocar tareas de otras sesiones, no inventar aprobación, no conceder G_EXEC; WS07 no promociona.

## AMBIGUEDADES
1. **Salida limitada a `decisiones.md` frente a edición del DAG.** El nodo dice “Registrar source_mode=editable o read_only en parámetros del DAG”, pero `output_scope: decisiones.md`. Obliga a inventar si WS07 puede escribir `dag.yaml` o solo declararlo en `decisiones.md` para otro nodo.
2. **Alcance de decisiones frente a G_PRODUCT.** `scope` enumera “baseline, host, fuente/edición, escritura/Git/coordinador y cierre”, mientras G_PRODUCT exige P01/P02/P07/P08/P09 y P04 como `source_mode`. P08 (uso humano y alcance) y P09 (ubicación de entradas reales) no aparecen nombradas en `scope`; obliga a inventar si WS07 debe redactarlas/registrarlas o solo esperar.
3. **“Baseline” sin referente único.** “confirma o corrige baseline” no identifica qué baseline (¿Entrega L/M/E?, ¿P03?). Obliga a inventar el conjunto de afirmaciones que el humano debe aceptar.

## DRY-RUN
**Lecturas previstas:** `decisiones.md`, `dag.yaml#parameters` y nodo WS07, `brief.md`, `alcance.md`, `cobertura.md`, `reconciliacion.md` (WS06) y guía.
**Cambios previstos:** redactar P01–P09 con alternativas/estado pendiente; registrar en P01 designaciones y en P04 `source_mode`; si se autoriza, sincronizar `dag.yaml`.
**Dependencias:** salida de WS06; humano solicitante/designado como actor; gates G_PRODUCT y G_WRITE_POLICY; WS44 espera designación; WS08/09/10 esperan G_PRODUCT.
**Validaciones futuras:** comprobar actor/fecha/resultado por decisión; que P01 nombre responsables y operador Scion; que `source_mode` coincida con P04; que WS11/12 obtengan aceptación; que WS44 haga probe real.

## FUTURO
El humano resuelve P01–P09 y designa identidades; otro nodo verifica gates y reconcilia; WS08/09/10 consumen G_PRODUCT; WS44 ejecuta el probe tras designación; WS11/12 registran aceptación por repo; la promoción requiere autorización separada.
