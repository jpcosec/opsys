REFORMULACION

Propósito: integrar conocimiento y grafo local en graph_ui reutilizando el grafo actual y una vista genérica de documento registrada en `shell/registry.js` para átomos, protoátomos, crossroads, materializaciones y pills, con clasificación y vecindad. Resultado: navegación ida/vuelta por fuentes y backlinks, Markdown no modelado visible con su ruta de origen, clasificación tipo/tags y vecindad de hasta 2 hops, sin renderer nuevo obligatorio por clase. Repo dueño: graph_ui; `output_scope`: `views/workspace/graph/`, `node/workspace-view.js`, `shell/registry.js`, `tests/`. Límites: preservar Code local de a1b2b22; no segundo lector para Markdown no modelado; no inferir tags por carpeta; ViewDoc de WS18 solo extensión opcional; G_UI_READ por delta; no duplicar implementación.

AMBIGUEDADES

1. «un soporte no modelado (Markdown sin modelo) es visible y navegable en la vista de documento genérica» frente a «Markdown no modelado se hereda del lector WS13.1/explorador WS13.2 (vía WS13), no segundo lector» y «vista de documento genérica única registrada en shell/registry.js para átomos/protoátomos/crossroads…». Obliga a inventar si el Markdown sin modelo se muestra en la vista genérica de WS24 o en la de WS13, y si hay que registrar un caso sin modelo.

2. «La vista muestra la clasificación (tipo y tags)» frente a «tags del documento cuando el modelo los declare»: para un documento modelado sin tags declarados no queda dicho si la ausencia de tags cumple la aceptación o si debe mostrarse otra clasificación; obliga a fijar un comportamiento no definido.

DRY-RUN

Lecturas: `dag.yaml` (WS24, WS13, WS09, WS29/WS42 y gates), guía, brief, alcance, decisiones, cobertura, reconciliacion y referencia externa. Cambios previstos: extender grafo y panel Context; registrar vista genérica; mostrar tipo/tags; consumir backlinks de la API de grafo de sldb; vecindad 2 hops; preservar Code; pruebas. Dependencias: WS13 (lector/explorador y WS13.1–13.3), WS09 (catálogo), WS11/WS03/WS02 transitivas; G_UI_READ por delta. Validaciones futuras: store temporal real o corpus WS40; ida/vuelta; Markdown no modelado con ruta; clasificación; vecindad; ausencia de renderer por clase; después WS30. Sin ejecutar.

FUTURO

WS13.1/13.2 producen lector y explorador, incluido el Markdown no modelado; WS09 el catálogo; WS11 el contrato de navegación; WS03 el inventario. El solicitante P01 emite el acta G_UI_READ por delta en graph_ui. WS18/ViewDoc solo se conecta tras G_SPEC_VIEW. WS30 realiza la validación humana. El TaskDoc de promoción fija archivos, escenarios y textos. WS42 valida materializaciones más adelante.
