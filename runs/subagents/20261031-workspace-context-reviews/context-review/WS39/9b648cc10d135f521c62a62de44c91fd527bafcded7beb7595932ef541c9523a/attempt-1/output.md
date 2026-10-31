REFORMULACION
Propósito: hacer navegable desde el lector la inspección/edición de Schema y clases ya existentes, reutilizando draft/validate/promote de sldb. Resultado: nodo de implementación en graph_ui con punto de entrada en el panel Context de WS13, prueba UF09 de inspección y mutación en store temporal real, y acta humana en `graph_ui:runs/.../modelos/acta.md`. Repo: graph_ui (`output_base: graph_ui:repository_root/`; salidas `shell/dialogs.js`, `views/models/`, `tests/`, `runs/.../modelos/`). Límites: no reimplementar modelos; no habilitar promover sin API/autoridad; G_HUMAN_READ solo habilita uso de mutaciones; G_HUMAN_MODEL antes de marcar disponible el capítulo 15 del manual de WS31; promoción no autorizada.

AMBIGUEDADES
1. «acceso desde documento activo muestra Schema/clase origen de ese documento». Obliga a inventar el resultado cuando el documento activo no tiene una Schema/clase origen única (sin modelo, varias o fuera del inventario WS04): ocultar el acceso, mostrar vacío o listar candidatos. La aceptación no fija ese comportamiento; el TaskDoc solo fija «ruta/selector exacto».

DRY-RUN
Lecturas: dag.yaml, guía, brief, alcance, decisiones, cobertura; al ejecutar, `task-ws39.md`, contrato WS12, inventario WS04, WS13 (`node/workspace-view.js`), `shell/registry.js` y manual. Cambios previstos: integrar punto de entrada en `shell/dialogs.js` y `views/models/`; pruebas en `tests/`; acta en `runs/.../modelos/`. Dependencias: WS12 (contrato/whitelist) y WS13 (lector/contexto); gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT per delta. Validaciones futuras: UF09 inspección/mutación en store temporal real; efectos/errores según WS12; acta humana P08; G_HUMAN_MODEL; no promover si falta API/autoridad. Sin ejecución.

FUTURO
WS12 produce contrato y recibo G_WRITE_CONTRACT por delta; WS04, inventario del editor; WS13, lector y panel Context; WS16 produce acta G_HUMAN_READ; el receptor P01 produce acta G_UI_WRITE del delta; la persona P08 valida y produce G_HUMAN_MODEL; WS31 publica el capítulo 15 del manual; la autorización de promoción queda a humana.
