## REFORMULACION

**Propósito:** integrar en graph_ui el grafo local y una vista de documento genérica para conocimiento (átomos, protoátomos, crossroads, materializaciones y pills), con clasificación, backlinks y vecindad.

**Resultado:** delta sobre el ticket workspace en draft, reutilizando el grafo y `shell/registry.js`; navegación ida/vuelta, backlinks derivados, soporte no modelado visible y sin renderer obligatorio por clase.

**Repo:** `graph_ui`; salida en `frontends/mindmap/views/workspace/graph/`, `Context` y `tests/`.

**Límites:** depende de WS13, WS18 y G_UI_READ (pendiente, producido por WS11); no autoriza ejecución, no modifica spec2viz ni duplica el ticket receptor.

## AMBIGUEDADES

1. **Clasificación en soportes no modelados.** Cita: «Clasificación = tipo del modelo y tags del documento cuando el modelo los declare» y «La vista muestra la clasificación (tipo y tags)». No se define qué mostrar para Markdown sin modelo ni de dónde salen los tags si el modelo no los declara. Obliga a inventar si se muestran vacíos, se omiten o se leen del frontmatter.

2. **Uso concreto de WS18.** Cita: «Reutilizar el gráfico actual y una vista de documento genérica única registrada en shell/registry.js» junto con `depends_on: WS18`. El nodo no dice qué salida de WS18 consume —ViewDoc o NotationDoc— ni cómo condiciona el grafo o la vista. Obliga a inventar la integración o a ignorar la dependencia.

3. **Ubicación del soporte no modelado.** Cita: «un soporte no modelado (Markdown sin modelo) es visible y navegable en la vista con su ruta de origen». No precisa si «la vista» es el grafo local o la vista de documento genérica. Obliga a inventar dónde debe aparecer y qué aceptación se prueba.

## DRY-RUN

**Lecturas previstas:** WS24 y vecinos en `dag.yaml`; acta WS11; `auditoria/infraestructura.md` de WS03; inventario WS02 y catálogo WS09; `deskops/models/materialization.py`; `shell/registry.js`; ticket workspace draft; brief, alcance y reconciliación.

**Cambios previstos:** vista genérica registrada en `shell/registry.js`; backlinks vía API de grafo de sldb; clasificación y vecindad; preservar Code local; pruebas en `tests/`. Sin cambios en spec2viz.

**Dependencias:** WS13 (agregado), WS18, G_UI_READ. No requiere contrato de escritura.

**Validaciones futuras:** pruebas de navegación ida/vuelta, backlinks, no modelados, clasificación y vecindad ≤2 hops; aceptación humana en WS30; gate G_UI_READ.

## FUTURO

WS11 debe emitir el acta G_UI_READ con responsable graph_ui y ticket receptor; el dueño de spec2viz debe promover WS18; WS03 produce la auditoría de infraestructura; WS30 valida UF01/UF03; el humano resuelve P01 y demás decisiones pendientes.
