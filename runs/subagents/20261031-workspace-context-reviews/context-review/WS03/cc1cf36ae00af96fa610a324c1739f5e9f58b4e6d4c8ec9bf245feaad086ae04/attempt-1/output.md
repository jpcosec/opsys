## REFORMULACION
Propósito: auditar en solo lectura sldb/pron/spec2viz (fuente/payload, conflictos y locks, referencias documentales, búsquedas y alcance ViewDoc). Resultado: un documento en `auditoria/infraestructura.md`. Repo dueño: deskops. Límites: sin cambios interrepo, Kimun solo como referencia, promoción no autorizada, depende de WS01. No se ejecuta nada.

## AMBIGUEDADES
1. «Inventariar persistencia, consultas y notaciones»: “notaciones” aparece en el título pero no se define en `scope` ni en `acceptance`; obliga a inventar qué sistemas de notación incluir (¿enlaces Markdown, layout/notación spec2viz, representación de grafo?) y dónde termina la auditoría.
2. «referencias documentales»: no precisa si son enlaces entre documentos, citas, referencias externas o relaciones del grafo; obliga a fijar un universo y un formato de inventario no definidos.
3. «alcance real ViewDoc»: obliga a decidir la frontera entre spec2viz/ViewDoc, el evaluador de graph_ui y el render; el brief declara ViewDoc opcional y no da criterio de “real”, por lo que el ejecutor debe inventar qué parte audita y qué declara fuera.

## DRY-RUN
Lecturas previstas: `dag.yaml` (nodo WS03 y aristas de contrato), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y esta guía. Cambios previstos: ninguno interrepo; al promover, crear/editar `auditoria/infraestructura.md` bajo el `output_base` de deskops. Dependencias: WS01 aporta brief/glosario; no hay `requires`. Validaciones futuras: comprobar que la salida distingue API comprobada con lectura citada, ausencia y hueco; confirmar ausencia de cambios interrepo; preflight y TaskDoc antes de promover.

## FUTURO
WS06 consumirá esta auditoría para su matriz de alcance. Un humano/coordinador decide la promoción y verifica el recibo. WS11/WS12 pueden enlazar hallazgos como fuente de contrato; WS18 cubre ViewDoc. P01/P02 ya están registradas y no se reabren. No se crean gates nuevos.
