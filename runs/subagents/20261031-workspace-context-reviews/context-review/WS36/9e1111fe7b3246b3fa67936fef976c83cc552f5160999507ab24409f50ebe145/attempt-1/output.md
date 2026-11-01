REFORMULACION
Propósito: integrar en el workspace la delegación e intervención humanas sobre ejecuciones. Resultado: UI en graph_ui que invoca solo el adaptador WS34 para dispatch/reply, registra decisiones con WS33.2 y muestra revisión con actor humano y evidencia enlazada de WS33.1/WS33.2; los fallos de API o permisos se muestran en pantalla; sin autoaprobación ni simulación. Repo: graph_ui. Límites: no crear canales ni adaptadores propios, no escribir decisiones fuera de WS33.2, no simular aprobaciones; promoción no autorizada y gates pendientes.

AMBIGUEDADES
1. «registrar decisiones con WS33.2» y «evidencia enlazada de WS33.1/WS33.2»: WS33.2 no figura en `depends_on` de WS36; solo aparece en `review_context_nodes`, que no es una arista. Tampoco consta en el input que WS33 —del que depende WS35— sea un aggregate que incluya WS33.1/WS33.2. El ejecutor tendría que asumir su disponibilidad y orden, o inventar la integración/registro. Falta declarar la dependencia o justificar la clausura transitiva.

DRY-RUN
Lecturas: dag.yaml, guía, brief, alcance, decisiones, cobertura, contratos WS12/WS34/WS35/WS33.2 y gates. Cambios previstos: vistas en `frontends/mindmap/views/workspace/execution/`, ruta fina hacia el adaptador WS34 y tests; sin tocar deskops ni el adaptador. Dependencias: WS34 y WS35; transitivas WS33/WS12/WS27 y, si WS33 es aggregate, WS33.1/WS33.2; gates G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT. Validaciones futuras: respuesta vinculada al intento, revisión con actor/evidencia, error por API o permisos ausentes y ausencia de autoaprobación; WS37 validará con agente real. No se ejecuta nada.

FUTURO
WS12 fija operaciones y actor; WS34.1/WS34.2 producen el adaptador; WS35 aporta la traza; WS33.1/WS33.2 producen resultado y decisión; el humano y WS44/G_SCION resuelven permisos y ejecución; WS37 valida; promoción/TaskDoc fijan archivos y pruebas.
