# Disposición WS16, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Gate humano de lectura (UF01/03/07/08/10), consume el manifiesto de WS40 sin corpus propio, acta en graph_ui con mediciones P08, repo graph_ui, depende de WS14, WS15, WS08, WS40, WS41: coincide (los umbrales p95 ≤2 s y arranque ≤10 s figuran en validacion-humana.md).

**Ambigüedades.**

1. «supervisor del repo receptor atribuye el fallo» (rol/repo). Clase: `futuro asignado`. actor nombrado en el input: el supervisor del repo receptor (graph_ui) atribuye; WS16 solo «lo registra» y no corrige; si no aísla la causa, registra incidente.
2. «Preparar corpus por WS40» frente a «sin crear corpus propio». Clase: `no es ambigüedad`. «consume el manifiesto de WS40… sin crear corpus propio»: el corpus lo produce WS40; si WS16 ejecuta el comando del generador lo fija el TaskDoc. Ver promotion-notes.md.
3. «segundo desk real» frente a repos temporales de WS40. Clase: `no es ambigüedad`. el scope liga UF08 al manifiesto WS40 («consume el manifiesto de WS40»); WS17 llama «los dos desks del manifiesto WS40» a los mismos; «real» = desk inicializado, no mock.
4. «registra incidente/diagnóstico en repo/superficie» (ubicación y contenido). Clase: `detalle de promoción`. formato y ubicación del registro del incidente son detalle del acta/TaskDoc; la condición (causa no aislada) y el actor están en el input.
