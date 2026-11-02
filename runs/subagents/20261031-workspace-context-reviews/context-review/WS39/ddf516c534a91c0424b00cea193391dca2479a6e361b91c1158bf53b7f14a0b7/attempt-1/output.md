REFORMULACION
Encargo: integrar en graph_ui la inspección/edición de modelos existentes desde el documento activo, mostrando en el panel Context del lector WS13 el Schema/clase origen y abriendo el editor inventariado WS04, usando draft/validate/promote de sldb sin reimplementar modelos. Resultado: punto de entrada navegable y mutación UF09 probada en store temporal, con acta humana y G_HUMAN_MODEL. Repo: graph_ui. Límites: no reimplementar modelos; no habilitar promote sin API/autoridad; G_HUMAN_READ solo habilita uso de mutaciones UI, no desarrollo/pruebas API aisladas; output_scope acota archivos; extensión posterior al lector básico; acta en repo dueño.

AMBIGUEDADES
1. «acceso desde documento activo muestra Schema/clase origen de ese documento y abre editor existente»: no define qué mostrar si no hay Schema/clase. Obliga a inventar estado vacío/oculto/handoff y si entra en aceptación.
2. «acta de prueba humana ... con el participante que fija P08» frente a alcance.md «Las validaciones humanas usan el corpus WS40»: WS39 no depende de WS40. Obliga a inventar corpus alternativo o cómo obtener WS40.
3. «Contexto = panel lateral Context del lector WS13 (node/workspace-view.js)» frente a «output_scope: shell/dialogs.js; views/models/; tests/...»: el punto de entrada parece exigir workspace-view.js, fuera de scope. Obliga a inventar si puede modificarlo o cómo engancharse sin tocarlo; el TaskDoc no amplía output_scope.

DRY-RUN
Lecturas: WS39 y gates; contrato WS12; lector WS13 (workspace-view.js); admisión WS48; inventario WS04; API sldb draft/validate/promote; tests; corpus WS40; manual WS31. Cambios: en graph_ui, integrar en views/models/ y shell/dialogs.js el acceso desde Context, mostrar Schema/clase y abrir editor; pasar mutaciones por WS48 antes de promover; pruebas; acta en runs/.../modelos/. Dependencias: WS12, WS13, WS48; G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT por delta; G_HUMAN_MODEL. Validaciones: UF09 inspección/mutación en store temporal; efectos/errores WS12; punto de entrada; acta P08; G_HUMAN_MODEL antes del capítulo 15. Errores: si falta contrato WS12, admisión WS48, API/autoridad, corpus WS40 o inventario WS04, detenerse y registrar hueco; no crear sustituto; no habilitar promote.

FUTURO
WS12 publica contrato de operaciones; WS13 entrega lector/contexto; WS48 entrega admisión de escritura; WS04 inventario del editor; WS40 corpus; WS16 resuelve G_HUMAN_READ; P01 receptor resuelve G_UI_WRITE por delta; persona P08 realiza acta y G_HUMAN_MODEL; WS31 publica manual.
