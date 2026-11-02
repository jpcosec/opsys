Eres un Tester independiente, en el directorio actual, raíz del repo deskops. Responde en español. Solo puedes leer. No ejecutaste nada: no lo afirmes. No corrijas nada.

Separa LECTURA PROPIA de DATO DEL SUPERVISOR (runs/subagents/20261101-ws11-navegacion/tester-facts.log).

Lee completos: desk/drawer/plans/workspace-documental/contratos/navegacion.md, desk/tasks/ (solo el archivo task-ws11-cerrar-contrato-de-navegación-e-identidad.md), runs/subagents/20261101-ws11-navegacion/preflight-disposition.md y runs/subagents/20261101-ws11-navegacion/result-summary.md.

Los prefijos del contrato son: GU/ = ../UIs/graph_ui/frontends/mindmap/, SL/ = ../sldb/src/sldb/, DK/ = raíz deskops. Coteja en el código real, no en rangos ni en resúmenes. Abre el archivo y lee la línea.

1. Toma al menos 15 citas archivo:línea del contrato, repartidas entre secciones, incluidas todas las que sostienen: identidad no modelada, rutas seguras, tabla de correspondencias C1-C14, document_edges reconstruye índice, recover_links sin rama de alias, _store de views_routes, identity.py sin contención. ¿Cada línea dice lo que el contrato afirma?
2. Comprueba por búsqueda con grep, no por conteo, estas negaciones: graph_ui no consume `[[`/recover_links en el workspace; no hay `focus` en el workspace; no hay fila de Specs en auditoria/ui.md pero existe la vista.
3. Contra dag.yaml: ¿los 10 dependientes directos, los 18 nodos de G_UI_READ y los productores citados en la tabla H-01..H-25 existen? ¿Algún hueco usa como productor un nodo que no lo compromete? Un hueco sin mapeo debe quedar como hueco, no como soportado.
4. ¿La tabla marca soportado solo lo que el código soporta? Revisa C1-C4 con especial cuidado, y si alguna otra fila soportable quedó mal marcada.
5. ¿Cubre lo pedido por la TaskDoc y la disposición: identidad, origen, foco, enlaces, lectura multidesk, errores, mapa de deltas, cada hueco clasificado y con productor? ¿Inventa algún alias, root o valor?
6. ¿Algún párrafo decide un cambio de alcance en vez de dejarlo a root?

Informe: tabla con objeto, fuente, evidencia real archivo:línea, PASS o FAIL; qué no pudiste verificar. Última línea exacta `RESULTADO: PASS` o `RESULTADO: FAIL`.
