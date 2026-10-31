## REFORMULACION
**Propósito:** encargo de planificación para una vista de workspace que muestre ejecución y trazabilidad.
**Resultado:** lectura de tarea–intento–conversación–resultados–decisión, en `frontends/mindmap/views/workspace/execution/` más `tests/`, en `graph_ui`.
**Límites:** solo lectura (no mutación); depende de WS33 (backend documental) y WS27 (diff/evidencia); requiere `G_SCION` y `G_UI_READ`; promoción no autorizada.

## AMBIGUEDADES
1. «Intento correcto, enlaces origen, evidencia legible» — «Intento correcto» no define qué hace correcto a un intento (campos obligatorios, correspondencia con fuente, estados). Obligaría a inventar el criterio de corrección.
2. «enlaces origen» — no especifica destino del enlace (documento, tarea, mensaje, intento, commit). Obligaría a inventar qué se enlaza y desde dónde.
3. «evidencia legible» — no fija formato ni umbral de legibilidad. Obligaría a inventar la comprobación.
4. «Lectura tarea-intento-conversación-resultados-decisión usando fuente dueña» — «tarea» no aparece en el scope de WS33 («Referencias Hub/proyecto/conversación/mensaje/intento y revisión humana explícita») ni en el de WS27 («Diff Git y artefactos de evidencia junto al encargo»); «fuente dueña» tampoco identifica repo/API por entidad. Obligaría a inventar el proveedor de «tarea» y la autoridad de cada lectura.

## DRY-RUN
- **Lecturas previstas:** nodo WS35 y contratos de vecinos WS33/WS27/gates en `dag.yaml`; `task_file` al promover.
- **Cambios previstos:** vista de lectura en `frontends/mindmap/views/workspace/execution/` y pruebas en `tests/`; sin endpoints ni escritura.
- **Dependencias:** WS33 y WS27 como prerrequisitos; `G_SCION` (producido por WS44) y `G_UI_READ` (resolver WS11) como gates no satisfechos.
- **Validaciones futuras:** prueba de intento correcto, enlaces de origen y evidencia legible; verificación de que `completed` no se muestra como aprobado/cerrado; comprobación de ambos gates antes de promover.

## FUTURO
WS36 consume esta vista para delegación/intervención; WS11 produce `G_UI_READ`; WS44 produce `G_SCION`; el solicitante humano designa responsables y resuelve P04/P01 según `decisiones.md`. La promoción exige preflight y TaskDoc en `graph_ui`.
