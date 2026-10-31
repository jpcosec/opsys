## REFORMULACION
**Propósito:** integrar en graph_ui un grafo local y una vista de documento genérica única, registrada en `shell/registry.js`, para átomos, protoátomos, crossroads, materializaciones y pills, con clasificación, vecindad y backlinks derivados.

**Resultado:** delta sobre el ticket workspace con navegación ida/vuelta por fuentes y backlinks, Code local preservado y Markdown no modelado visible y navegable con su ruta de origen.

**Repo:** `graph_ui`; `output_scope: frontends/mindmap/views/workspace/graph/; Context; tests/`. Depende de WS13 y WS18; requiere `G_UI_READ` pendiente.

**Límites:** no crear un renderer obligatorio por clase; no modificar spec2viz; promoción no autorizada; no ejecutar.

## AMBIGUEDADES
1. **Cobertura de aceptación incompleta.** El scope exige «clasificación y vecindad» y define «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare. Vecindad = hasta 2 hops», pero la aceptación solo exige «Navegación ida/vuelta por fuentes y backlinks derivados» y el caso Markdown no modelado. Obliga a inventar si clasificación y vecindad deben probarse o solo mostrarse.
2. **«crossroads» sin definición suministrada.** Aparece en «átomos/protoátomos/crossroads (inventariados en WS02 y catalogados en WS09)», pero no está definido en brief ni glosario. Aunque WS09 lo catalogue, el nodo no fija qué entidad es ni qué representación mínima debe tener; el ejecutor tendría que inventarlo antes de esa dependencia.
3. **Alcance del Code local impreciso.** «preservar Code local del ticket workspace en draft que identifique el acta WS11» no fija si el nodo debe implementar Code o solo conservarlo; obliga a decidir el límite de cambios en esa proyección.

## DRY-RUN
**Lecturas previstas:** nodo WS24 en `dag.yaml`; guía; brief, alcance, decisiones, cobertura y reconciliación; contratos vecinos WS13/WS18 (no revisados); referencias nombradas: inventario WS02, catálogo WS09, `auditoria/infraestructura.md` de WS03, acta WS11 y modelo `deskops/models/materialization.py`.

**Cambios previstos:** delta en `frontends/mindmap/views/workspace/graph/`, Context y tests; registro de la vista genérica en `shell/registry.js`; consumo de API de grafo sldb para backlinks. Sin ejecución.

**Dependencias:** WS13 como agregado completo; WS18 para ViewDoc/NotationDoc; `G_UI_READ` pendiente; WS11/WS12 transitivas.

**Validaciones futuras:** navegación ida/vuelta y backlinks; Markdown no modelado visible con ruta; ausencia de renderer nuevo por clase; clasificación y vecindad según lo que se aclare; recorrido humano en WS30.

## FUTURO
WS11 produce el acta y resuelve `G_UI_READ`; WS07 identifica al responsable de graph_ui; la promoción fija archivos, pills, átomos y evidencia; WS30 valida el flujo humano. La matriz WS06 llega transitivamente por WS11/WS12.
