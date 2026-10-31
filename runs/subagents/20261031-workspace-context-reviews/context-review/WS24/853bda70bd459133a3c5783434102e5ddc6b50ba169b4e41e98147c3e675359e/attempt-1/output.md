REFORMULACION
- **Propósito:** fijar si WS24 se entiende como encargo de planificación para integrar conocimiento y grafo local.
- **Resultado:** vista/grafo que reutiliza el gráfico y una vista de documento genérica para átomos, protoátomos, crossroads y materializaciones, con backlinks, clasificación, vecindad y Code local preservado.
- **Repo:** `graph_ui`; salidas en `frontends/mindmap/views/workspace/graph/`, `Context` y `tests/`.
- **Límites:** consumir ViewDoc de WS18; backlinks según API de sldb y `auditoria/infraestructura.md` de WS03; no renderer nuevo por clase; `G_UI_READ`; sin ejecución.

AMBIGUEDADES
1. «Vecindad = hasta 2 hops.» No fija dirección ni si incluye backlinks. Obliga a inventar el conjunto exacto de nodos/relaciones que se muestra y se prueba.
2. «preservar Code local del ticket workspace en draft que identifique el acta WS11» no aparece en `acceptance` ni define cómo comprobar esa preservación o la identificación del acta. Obliga a inventar criterio y artefacto de verificación.

DRY-RUN
- **Lecturas:** WS24, código actual de `graph_ui`, `shell/registry.js`, ViewDoc de WS18, acta/`G_UI_READ` de WS11, auditoría de WS03 (transitiva), `deskops/models/materialization.py`, inventarios WS02/WS09 y ticket workspace draft.
- **Cambios previstos:** integrar vista genérica y grafo; calcular backlinks; mostrar clasificación y vecindad; preservar Code local; añadir tests.
- **Dependencias:** WS13 cerrado como agregado, WS18 entregado y `G_UI_READ` resuelto; WS03/WS09/WS11 llegan transitivamente.
- **Validaciones futuras:** acceptance de WS24, pruebas sobre store real y validación humana WS30; sin ejecutar.

FUTURO
WS11 resuelve `G_UI_READ` con acta; WS18 produce los ViewDoc; una persona promueve TaskDoc/preflight; WS30 valida; WS29/WS30/WS42 consumen el resultado. Las Pxx no se resuelven aquí.
