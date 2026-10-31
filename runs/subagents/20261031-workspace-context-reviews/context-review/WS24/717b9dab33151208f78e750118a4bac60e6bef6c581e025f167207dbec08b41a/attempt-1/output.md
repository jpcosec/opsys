## REFORMULACION
**Propósito:** integrar en graph_ui la navegación entre conocimiento y grafo local, reutilizando el grafo existente y una vista documental genérica. **Resultado:** navegación ida/vuelta con backlinks, clasificación, vecindad y Markdown sin modelo visible con su ruta de origen. **Repo:** graph_ui (`frontends/mindmap/views/workspace/graph/; Context; tests/`). **Límites:** delta sobre el ticket workspace en draft; consume ViewDocs de WS18; no exige un renderer nuevo por clase; depende de G_UI_READ; promoción no autorizada.

## AMBIGUEDADES
1. «Vecindad = hasta 2 hops.» No fija dirección ni tipos de arista: obliga a inventar si incluye relaciones entrantes, salientes o ambas, y si los backlinks cuentan dentro de la vecindad.
2. «es visible y navegable en la vista de documento genérica con su ruta de origen.» No define de dónde se obtiene esa ruta (ruta de archivo, identidad del store u origen declarado) ni qué mostrar si falta; obliga a inventar fuente y fallback.
3. «La vista muestra la clasificación (tipo y tags)» junto a «un soporte no modelado (Markdown sin modelo)», que no tiene tipo ni tags. No aclara si se muestra vacío, se omite o se etiqueta como no modelado; obliga a inventar ese estado.

## DRY-RUN
**Lecturas:** WS24, vecinos WS13/WS18, guía, brief, alcance, cobertura, reconciliación y decisiones; `auditoria/infraestructura.md` (WS03), `deskops/models/materialization.py`, `shell/registry.js` del ticket draft.
**Cambios previstos:** vistas en `graph/` y Context, más tests.
**Dependencias:** WS13 y WS18 cerrados; G_UI_READ resuelto por WS11 mediante acta; inventario WS02 y catálogo WS09 transitivos.
**Validaciones futuras:** navegación ida/vuelta, backlinks derivados, soporte no modelado con ruta, clasificación y vecindad de 2 hops; aceptación manual en WS30.

## FUTURO
WS11 produce el acta y G_UI_READ; WS03 la auditoría de infraestructura; WS18 los ViewDoc; WS02/WS09 inventario y catálogo. La promoción la decide un humano; WS30 valida. Nada ejecutado.
