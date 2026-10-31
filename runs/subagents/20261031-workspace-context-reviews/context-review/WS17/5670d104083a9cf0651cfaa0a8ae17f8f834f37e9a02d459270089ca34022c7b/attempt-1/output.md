REFORMULACION
Propósito: escribir entradas e índices authored como plantillas Markdown versionadas en `ejemplo/nav/` para que WS40 las materialice en su corpus temporal. Resultado: links Markdown recorribles sin UI, con dos desks y procedencia resolubles, sin duplicar registry. Repo: `deskops`; base `desk/drawer/plans/workspace-documental/`. Límites: no produce el corpus, no copia inventarios derivados, no escribe repos reales; puede ejecutarse antes de WS16; WS30 integra los índices. Depende de WS11 y WS40.

AMBIGUEDADES
1. «Resolver dos desks y procedencia»: no define qué significa “resolver” ni cómo se comprueba la procedencia. Obliga al ejecutor a inventar el criterio observable de aceptación (enlace, campo, manifiesto o combinación).
2. «no duplicar registry»: no identifica el registry concreto, su ubicación ni su representación. Obliga a inventar qué artefacto debe evitarse y cómo demostrar que no se duplicó.
3. «Resolver dos desks»: no nombra cuáles dos desks del corpus WS40 son exigibles. Aunque WS40 crea dos repos con desk y un tercero sin desk, el nodo no fija la correspondencia; obliga a inferirla del manifiesto.

DRY-RUN
Lecturas previstas: `dag.yaml#node:WS17`; contrato `contratos/navegacion.md` de WS11; generador y manifiesto de WS40; reglas de alcance/decisiones aplicables. Cambios previstos: crear plantillas Markdown bajo `deskops:desk/drawer/plans/workspace-documental/ejemplo/nav/`; no tocar corpus, repos reales ni registry. Dependencias: contrato WS11, generador WS40 y manifiesto con roots/stores/commits; los dos desks y su procedencia. Validaciones futuras: regenerar corpus WS40 con `ejemplo/nav/`, recorrer links Markdown sin UI, comprobar dos desks/procedencia y ausencia de registry duplicado; WS30 integra; WS43 publica en el desk real.

FUTURO
WS40 materializa las plantillas y produce el corpus/manifiesto; WS11 fija navegación e identidad; WS30 realiza la validación humana; WS43 publica en deskops real. La promoción fijará archivos exactos, pills, átomos y preflight. P09/P08 y demás Pxx siguen siendo decisión humana.
