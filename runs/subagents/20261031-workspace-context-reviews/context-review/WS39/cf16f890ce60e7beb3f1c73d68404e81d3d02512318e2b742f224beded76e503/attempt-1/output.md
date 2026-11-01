REFORMULACION
Propósito: integrar en el lector WS13 la inspección y edición de modelos ya existentes desde el documento/contexto activo, sin reimplementar modelos. Resultado: entrada navegable Schema/clase origen que abre el editor inventariado WS04 y permite UF09 (inspección/mutación) usando draft/validate/promote de sldb. Repo dueño: graph_ui. Límites: no reimplementar modelos; no habilitar promover sin API/autoridad; mutaciones UI sujetas a G_HUMAN_READ; ruta/selector exacto en TaskDoc; output_scope declarado.

AMBIGUEDADES
1. «Contexto = panel lateral Context del lector WS13 (node/workspace-view.js)» frente a «output_scope: shell/dialogs.js; views/models/; tests/; runs/subagents/workspace-documental-acceptance/modelos/». El punto de entrada se sitúa en un archivo que no está en output_scope; el ejecutor tendría que inventar si puede modificar node/workspace-view.js o cómo enganchar el acceso sin tocarlo. El TaskDoc fija el selector, no la propiedad del archivo.
2. «acceso desde documento activo muestra Schema/clase origen de ese documento» no define qué mostrar si el documento no tiene Schema/clase origen o tiene varias; obliga a inventar estado vacío o criterio de selección.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura y nodo/gates. Sin ejecutar. Cambios previstos: integración en graph_ui, vistas/modelos, pruebas y acta. Dependencias: contrato WS12, lector WS13, inventario WS04; gates G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Validaciones futuras: UF09 en store temporal real; efectos/errores del contrato WS12; acta humana con participante P08; G_HUMAN_MODEL; capítulo 15 del manual WS31.

FUTURO
WS16 produce G_HUMAN_READ; WS12 publica el contrato; WS04 aporta el inventario del editor; P01/receptor decide G_UI_WRITE por delta; WS31 publica el manual; la persona P08 participa en la validación y se resuelve G_HUMAN_MODEL; WS45 cubre la precondición de payload si aplica.
