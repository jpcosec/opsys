## REFORMULACION
- **Propósito:** implementar lectura segura entre dos desks/stores en graph_ui, resolviendo solo aliases/roots autorizados por el contrato WS11 y usando APIs públicas.
- **Resultado:** leer un segundo desk desde el workspace, seguir enlaces authored del corpus y volver por la historia; cada request conserva su proyecto/store sin alterar el global `SLDB_STORE`; alias no autorizado, path escapado o store ausente producen error visible.
- **Repo dueño:** graph_ui.
- **Límites:** sin mutaciones cruzadas, sin federación por copia de contenido, sin roots arbitrarios; no se revisan aquí los contratos vecinos.

## AMBIGUEDADES
1. **«Leer segundo desk y volver, sin mutaciones cruzadas»** frente a la aceptación: esta exige lectura, enlaces, historia y errores visibles, pero no indica cómo comprobar que no hubo mutaciones cruzadas. El ejecutor tendría que inventar la evidencia (estado git, hash del store, ausencia de llamadas de escritura) y el criterio de fallo. Cita: «Leer segundo desk y volver, sin mutaciones cruzadas» y «UF08 lectura sobre dos stores de WS40: identidad/origen visibles, seguir enlaces authored del corpus entre desks y volver por la historia».

## DRY-RUN
- **Lecturas previstas:** contrato WS11 (pendiente), manifiesto/corpus WS40, salidas de WS13, código de workspace en graph_ui y tests existentes.
- **Cambios previstos:** resolución de aliases/roots autorizados por request, lectura de un segundo store, integración con historia/foco, errores visibles y pruebas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.
- **Dependencias:** WS13 completo, contrato WS11, corpus WS40 y recibo G_UI_READ específico de WS41; si falta alguno, detenerse y registrar el hueco.
- **Validaciones futuras:** pruebas con dos stores temporales reales; casos de alias no autorizado, path escapado y store ausente; lectura/retorno por historia; validación humana UF08 en WS16 sobre el corpus WS40.

## FUTURO
- WS11 produce el contrato de identidad, resolución, enlaces e historia multidesk.
- WS40 produce el corpus y manifiesto con dos desks enlazados.
- WS13 entrega el workspace con historia y foco.
- P01/receptor emite el acta G_UI_READ por delta; sin ella no se promueve.
- WS16 ejecuta la validación humana UF08; otro nodo prepara TaskDoc/promoción y preflight.
