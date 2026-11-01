REFORMULACION
Propósito: integrar en graph_ui la inspección/edición de modelos existentes (Schema/editar clases) desde el documento activo y el panel Context del lector WS13, usando draft/validate/promote de sldb sin reimplementar modelos. Resultado: punto de entrada navegable documento→Schema/clase origen y editor existente, más prueba UF09 de inspección/mutación en store temporal real y acta humana. Repo dueño: graph_ui; salidas: shell/dialogs.js, views/models/, tests/, runs/.../modelos/. Límites: no habilitar promover si falta API/autoridad; no habilitar mutaciones UI sin G_HUMAN_READ; promoción no autorizada; no sustituir contratos WS12 ni inventario WS04; no reimplementar modelos.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: nodo WS39, aristas WS12/WS13, gates G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT/G_HUMAN_MODEL, brief/alcance/decisiones/cobertura. Cambios previstos: UI en graph_ui y pruebas; acta en repo dueño; sin ejecutar. Dependencias: contrato WS12 (operaciones/efectos/errores), lector/contexto WS13, inventario WS04 (transitivo vía WS12), gates por delta. Validaciones futuras: UF09 en store temporal; entrada desde documento activo; efectos/errores según WS12; acta humana con participante P08; comprobar gates antes de uso de mutaciones.

FUTURO
WS12 publica contrato/whitelist; WS13 entrega lector/contexto; WS04 aporta inventario del editor; WS16 produce acta G_HUMAN_READ; receptor P01 emite G_UI_WRITE por delta; WS12 verifica G_WRITE_CONTRACT; humano P08 firma G_HUMAN_MODEL; WS31 publica manual cap. 15; autorización de promoción decide humano. No son ambigüedad.
