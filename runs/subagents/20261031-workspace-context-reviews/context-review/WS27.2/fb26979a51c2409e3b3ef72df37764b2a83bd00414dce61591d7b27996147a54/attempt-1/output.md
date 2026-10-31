## REFORMULACION
Propósito: que el workspace muestre evidencia en estado declarada, encontrada y verificada, y permita abrir su soporte, incluida la evidencia ausente. Resultado: implementación en `graph_ui` bajo `frontends/mindmap/views/workspace/evidence/` y `tests/`, usando rutas de lectura del contrato WS11. Repo dueño: `graph_ui`. Límites: no inventar `CommentDoc` antes de contrato; dependencias WS13 y WS12; requiere `G_UI_READ`, aún pendiente; promoción no autorizada.

## AMBIGUEDADES
1. «Mostrar declarada/encontrada/verificada y abrir su soporte; una evidencia ausente se ve como ausente.» No se define qué es cada estado, de dónde sale la evidencia, ni cómo se determina «verificada». Obligaría a inventar el modelo de datos, la fuente y el criterio de verificación.
2. «abrir su soporte» no precisa qué debe abrirse —documento fuente, artefacto, ruta o representación— ni el comportamiento esperado. Obligaría a inventar el destino y la interacción de apertura.
3. «Artefactos de evidencia junto al encargo» y «sin inventar CommentDoc antes de contrato»: «encargo» y `CommentDoc` no están definidos, y «contrato» no se identifica. Obligaría a inventar la ubicación/vinculación de artefactos y si los comentarios pueden usarse como soporte.

## DRY-RUN
Lecturas previstas, sin ejecutar: input suministrado; contrato de rutas WS11 y salida de WS12 cuando existan; `task-ws27-2.md` al promocionar. Cambios previstos: vistas de evidencia en la ruta declarada y tests asociados. Dependencias: WS13 para lector/foco, WS12 para contrato, `G_UI_READ` como gate; WS11 aparece de forma transitiva para rutas. Validaciones futuras: los tres estados, ausencia visible, apertura de soporte y aceptación del gate por WS11.

## FUTURO
WS11 produce `G_UI_READ` y las rutas de lectura; WS12 produce el contrato de operaciones; el solicitante o WS07 resuelve las Pxx y `source_mode`. WS27 cierra como agregado cuando cumplan WS27.1 y WS27.2. La promoción exige preflight y autorización humana; nada de ello se decide en esta revisión.
