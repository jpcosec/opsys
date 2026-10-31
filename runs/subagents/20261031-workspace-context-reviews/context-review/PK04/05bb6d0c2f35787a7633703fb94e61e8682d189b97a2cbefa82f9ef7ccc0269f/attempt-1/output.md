## REFORMULACION
- **Propósito:** agrupar la revisión de navegación y representaciones del desk sobre una identidad común; PK04 no se ejecuta ni autoriza tareas.
- **Resultado:** paquete coherente en el que índices authored (WS17), Board (WS22), procedimiento (WS23) y conocimiento/grafo (WS24) abren los mismos documentos/soportes; ViewDoc (WS18) es extensión opcional. Ningún renderer escribe estado ni marca pasos por lectura.
- **Repo:** deskops coordina; hijos en deskops, spec2viz y graph_ui.
- **Límites:** sin ejecución propia, sin aristas nuevas, sin mutaciones desde representaciones; los índices siguen sus fuentes.

## AMBIGUEDADES
Ninguna. El alcance y la aceptación delegan en los hijos y en contratos ya nombrados; no obligan a inventar resultado, repo, actor ni aceptación.

## DRY-RUN (hipotético, sin ejecutar)
1. **WS17** consume contrato WS11 y manifiesto/corpus WS40; produce plantillas `ejemplo/nav/`; WS40 regenera el destino temporal sin tocar el registry real.
2. **WS22 y WS23** consumen lector/identidad WS13 y catálogo WS09; producen vistas Board y procedimiento en graph_ui, solo lectura.
3. **WS24** reutiliza el lector WS13, la API de grafo sldb (WS03) y el catálogo WS09; produce vista genérica y grafo local.
4. **WS18**, opcional, consume WS09/WS11 y requiere G_SPEC_VIEW; produce ViewDoc/NotationDoc portable en spec2viz sin bloquear WS24.

**Integración futura:** la identidad WS11 enlaza lista, tablero, dependencias, procedimiento y conocimiento; se validaría con corpus WS40/WS16 y WS30 que los mismos TaskDoc abren en todas las representaciones, que no hay escritura de estado y que los índices se regeneran desde plantillas.

## FUTURO
WS11, WS40, WS09 y WS13 producen contrato, corpus, catálogo y lector; WS03 aporta la API de grafo. G_SPEC_VIEW lo resuelve el receptor P01 al preparar el delta de WS18. WS16/WS30 validan y WS43 publica; la aceptación humana de esos resultados no corresponde a PK04.
