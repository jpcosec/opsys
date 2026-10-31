# Executor comparison — WS39, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION

**Propósito:** integrar en graph_ui la inspección/edición de modelos ya existentes (Schema/editar clases) desde el panel Context del lector WS13, usando `draft/validate/promote` de sldb sin reimplementar modelos.

**Resultado:** punto de entrada desde documento activo que muestra Schema/clase origen y abre el editor inventariado WS04; prueba UF09 de inspección/mutación en store temporal real; acta en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md`.

**Repo dueño:** graph_ui. Salidas: `shell/dialogs.js`, `views/models/`, `tests/` y el acta.

**Límites:** no reimplementar modelos; no habilitar promover sin API/autoridad; G_HUMAN_READ solo habilita mutaciones en UI; ruta/selector exacto y archivos quedan para TaskDoc; depende de WS12 y WS13.

##

## Hallazgos/disposición contra intención

Documento sin modelo no da Schema editable: identidad/modelo opcional WS11 y contrato WS12 determinan capacidad; ausencia/no soportado visible según regla común, no se inventa clase. Ocultar/deshabilitar/aviso exacto es texto/interacción de TaskDoc futuro, pero resultado normativo no prometer disponible ni habilitar promote sin API/autoridad está fijado. Dry-run recupera entrada/errores/acta y límites.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
