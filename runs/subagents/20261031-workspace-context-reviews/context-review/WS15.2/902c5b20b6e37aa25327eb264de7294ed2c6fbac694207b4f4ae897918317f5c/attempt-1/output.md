REFORMULACION  
WS15.2 encarga a graph_ui orientar un proyecto sin desk: mostrar la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`, sin inicializar ni mutar desde la UI; tras un init externo, un refresco debe mostrar el desk real. Salida en `frontends/mindmap/views/workspace/orientation/`, rutas de lectura según WS11 y tests. Depende del lector integrado WS13 y de G_UI_READ; no crea desks, no ejecuta init y no promete escritura.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Leería el TaskDoc `task-ws15-2.md`, el contrato WS11, el estado de WS13 y el código graph_ui de workspace/orientation. Añadiría la vista/ruta de orientación y pruebas; consumiría las rutas de lectura y el shell del lector de WS13. Verificaría el acta G_UI_READ del delta. Si faltan WS11/WS13, se detendría y registraría el hueco en graph_ui. No invocaría init desde la UI. Validaría con un directorio sin desk: orientación, ruta absoluta y comando visibles, sin cambios en disco; luego ejecutaría `deskops init` fuera de la UI y refrescaría para comprobar el desk real. Errores esperados: contrato ausente, gate sin recibo; no se sustituyen. Respetaría `overlap_with: workspace` sin duplicar implementación.

FUTURO  
WS11 produce el contrato de rutas; WS13 entrega el lector; el receptor P01 emite el acta G_UI_READ por delta; un humano o CLI ejecuta el init externo y aporta la comprobación; el TaskDoc de promoción fija archivos, pruebas y textos; WS16 valida el lector. La promoción de WS15.2 no está autorizada.
