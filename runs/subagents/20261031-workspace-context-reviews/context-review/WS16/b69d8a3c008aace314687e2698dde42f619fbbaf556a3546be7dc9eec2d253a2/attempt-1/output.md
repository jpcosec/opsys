## REFORMULACION
WS16 es un nodo de validación humana temprana: comprobar que una persona real recorre lectura/descubrimiento (UF01, UF03 lectura), diagnóstico (UF07), multidesk lectura (UF08) y arranque/ausencia de desk (UF10). Resultado: acta humana y recibo de `G_HUMAN_READ` en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/acta.md`. Repo dueño: `graph_ui`. Límites: no implementa correcciones, no muta entre desks, no crea corpus propio, no sustituye la aprobación humana y no prueba guardados.

## AMBIGUEDADES
1. «supervisor del repo receptor atribuye el fallo por evidencia»: no se identifica el rol/actor ni cuál es el “repo receptor” (`graph_ui` o `deskops`). Obliga a inventar quién atribuye el fallo y dónde queda registrado.
2. «Preparar corpus por WS40» contradice «consume el manifiesto de WS40 y sigue el protocolo… sin crear corpus propio». Obliga a inventar si WS16 ejecuta el generador o solo consume el manifiesto ya producido.
3. «UF08 lectura del segundo desk real» frente a WS40, que produce «dos repos temporales». Obliga a inventar si “real” excluye el corpus temporal o exige otro desk no descrito.
4. «registra incidente/diagnóstico en repo/superficie»: no fija repo, superficie ni contenido mínimo del registro. Obliga a inventar ubicación y formato del incidente.

## DRY-RUN
Lecturas previstas: `dag.yaml` (WS16, vecinos y gate), guía, brief, alcance, decisiones, cobertura, validación humana y user-flows. Cambios previstos: acta en `graph_ui` con guion, versiones/commits, corpus, comandos, tiempos, fallos y decisión humana; recibo del gate enlazando commit/blob. Dependencias: manifiesto/corpus WS40, lectura multidesk WS41, búsqueda WS14, errores/degradado WS15, flujos WS08. Validaciones futuras: recorrido UF01/03/07/08/10; 20 aperturas y 10 búsquedas; p95 apertura/búsqueda ≤2 s; arranque ≤10 s; acta versionada; guardados fuera de alcance.

## FUTURO
WS40 produce corpus y manifiesto; WS41 habilita lectura del segundo desk; WS14/WS15 entregan búsqueda y estados degradados; WS08 precisa flujos. El participante humano decide aprobar o mantener pendiente `G_HUMAN_READ`; el supervisor del repo receptor —si existe— atribuye fallos. WS30 probará guardados posteriormente.
