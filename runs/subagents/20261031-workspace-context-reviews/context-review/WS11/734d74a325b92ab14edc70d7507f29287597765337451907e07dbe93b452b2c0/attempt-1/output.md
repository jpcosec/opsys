## REFORMULACION

- **Propósito:** cerrar el contrato de navegación e identidad del workspace documental: cómo un Markdown conserva identidad/ruta/modelo opcional, cómo se resuelven repo/store, foco, enlaces/historia y lectura multidesk read-only.
- **Resultado:** `contratos/navegacion.md`, con cada hueco clasificado como instancia, vínculo, consulta, API o renderer y, si falta API, dependencia acotada con repo dueño.
- **Repo dueño:** `deskops`.
- **Límites:** nodo de planificación; no implementa, no migra a Kimun, no inventa modelos ni publica el contrato como cerrado sin recepción en `graph_ui` y `spec2viz`. Queda sujeto a `G_PRODUCT` y a los borradores de WS08/WS09.

## AMBIGUEDADES

1. «graph/code admiten otros nodos con origen»: no se define qué tipos de nodo admite cada representación ni con qué criterio. Obligaría a inventar una taxonomía de nodos admisibles.
2. «obtener aceptación del delta lector en graph_ui»: el input no delimita qué cambios componen ese “delta lector”. Obligaría a inventar el alcance exacto que el responsable de `graph_ui` debe aceptar.
3. «El acta receptora enumera scope_nodes de G_UI_READ/G_SPEC_VIEW, incluidos corpus WS40 y multidesk WS41»: no queda claro si WS40/WS41 deben constar también en el acta de `spec2viz`; en `dag.yaml#gates` solo figuran bajo `G_UI_READ`. Obligaría a decidir a qué acta pertenecen.

## DRY-RUN

- **Lecturas previstas:** guía de revisión, brief, alcance, decisiones, cobertura, nodo WS11 y gates ya suministrados. Sin herramientas ni ejecución.
- **Cambios previstos:** redactar `contratos/navegacion.md`; preparar evidencia para `G_UI_READ` y `G_SPEC_VIEW`; registrar huecos de API con repo dueño.
- **Dependencias:** salidas de WS08 (`borradores/user-flows.md`) y WS09 (`borradores/vistas.md`); `G_PRODUCT` pendiente, resuelto por WS07 con responsables designados; WS12, WS13.x, WS18, WS40 y WS41 consumen después este contrato.
- **Validaciones futuras:** comprobar que cada hueco tiene clasificación y dueño; verificar que las actas enumeran los `scope_nodes`; contrastar que no se introduce migración Kimun ni modelos hipotéticos; confirmar que el contrato no se declara cerrado sin aceptación.

## FUTURO

- WS07 debe resolver `G_PRODUCT` e identificar a los responsables de `graph_ui` y `spec2viz`.
- Los responsables receptores deben firmar las actas de aceptación.
- WS12 y los nodos dependientes consumirán el contrato; cualquier API faltante pasará a dependencia del repo dueño.
- La promoción posterior fijará archivos, pills y evidencia, y requiere preflight de solo tarea.
