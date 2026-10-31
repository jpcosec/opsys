## REFORMULACION
Propósito: planificar en `graph_ui` un delta de la tarea Changes existente que muestre impacto comprobable de una mutación del store: documento afectado, relaciones alcanzadas y errores, apoyándose en `sldb stores check`, `deskops doctor` y `deskops drift check`. Resultado: integración/vista en `frontends/mindmap/views/workspace/changes/` con tests sobre store temporal real, sin reparación automática. Repo dueño: `graph_ui`. Límites: no CST ni árbol Kimun; no duplica Changes; no bloquea lector/manual básico; requiere `G_UI_READ`; promoción no autorizada.

## AMBIGUEDADES
1. «relaciones alcanzadas» (aceptación) y «relaciones comprobadas» (scope): no se define desde qué nodo, con qué profundidad ni dirección se consideran alcanzadas; obligaría a inventar el criterio de impacto.
2. «documento afectado, relaciones alcanzadas y errores»: «errores» no se acota —¿de lectura, `check`, `doctor` o `drift`?— ni su forma de mostrarse; obligaría a inventar taxonomía y origen.
3. «la vista enlaza al comando documentado»: no identifica cuál de los tres comandos enlaza ni dónde está documentado; obligaría a inventar el destino del enlace y la correspondencia error→reparación.
4. «Delta sobre tarea Changes actual»: no nombra la tarea/ticket receptor concreto; obligaría a decidir si es delta o ticket nuevo, aunque `integration_mode` y la matriz WS06 pretendan resolverlo transitivamente.

## DRY-RUN
Lecturas: `dag.yaml` (WS29, gates), brief, alcance, decisiones, cobertura, reconciliación y guía. Cambios previstos: `frontends/mindmap/views/workspace/changes/` y `tests/`; rutas de integridad según contrato WS11. Dependencias: WS15 (errores de lectura/modo degradado), WS24 (grafo/relaciones), `G_UI_READ` (WS11) y matriz WS06 vía WS11/WS12. Validaciones futuras: crear store temporal real, provocar mutación, comprobar documento/relaciones/errores, verificar enlace a comando documentado y ausencia de reparación automática; confirmar que no bloquea lector/manual.

## FUTURO
WS11 produce el contrato de rutas de integridad y el acta `G_UI_READ`; WS07 designa actor; WS06/WS04 confirman la tarea Changes receptora y el no solapamiento; el TaskDoc de promoción fija archivos, escenarios y textos; un humano decide la promoción y, si aplica, la política de mutación de WS12.
