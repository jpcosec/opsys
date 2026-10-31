## REFORMULACION

**Propósito:** encargar en `graph_ui` una representación navegable del Board real —trabajo/tareas— como lista/tablero y dependencias, abriendo los TaskDoc/contextos existentes. **Resultado:** vista/componente en `frontends/mindmap/views/workspace/board/` y `tests/`. **Repo dueño:** `graph_ui`. **Límites:** no reemplazar el workflow con drag-and-drop de status; no duplicar tareas; no presentar un predicado satisfecho como test aprobado. Depende de WS13 y WS09; requiere `G_UI_READ` (`pending`).

## AMBIGUEDADES

1. «integration_mode: delta_or_existing_ticket_only_after_WS06» frente a `depends_on: WS13, WS09`. Falta WS06 como arista o el texto contradice las dependencias; obliga a inventar si WS06 debe resolverse antes de ejecutar o solo informa la integración.

2. «Representar Board real como lista/tablero y dependencias». No queda claro si exige ambas representaciones o una alternativa; la aceptación no distingue, obligando a inventar alcance y criterio de comprobación.

3. «abriendo los mismos TaskDoc/contextos». «Contextos» no está definido: puede ser panel, pill, enlace o selección. Obliga a inventar qué se abre y con qué contrato.

4. «estados/gates reales». No se indica la fuente de verdad ni cómo demostrar «real»; ¿Board de graph_ui, gates de `dag.yaml` o ambos? Obliga a inventar la comprobación.

5. «Selección y links comunes con lector». «Lector» remite a WS13, pero no se define cómo se comparte selección entre tareas del Board y documentos; obliga a inventar el comportamiento de foco/enlaces.

## DRY-RUN

**Lecturas:** nodo WS22 y fuentes suministradas (brief, alcance, decisiones, cobertura, reconciliación, dag). `task_file` solo aparece referenciado, sin contenido evaluable. **Cambios previstos:** vista Board y tests dentro de `output_scope`; nada ejecutado. **Dependencias:** WS13, WS09 y `G_UI_READ` producido por WS11. **Validaciones futuras:** WS30 incluye WS22; aceptación de `G_UI_READ`; eventual conciliación WS06; promoción sujeta a autorización humana.

## FUTURO

WS11 produce el acta de `G_UI_READ`. WS09 entrega `borradores/vistas.md`. WS06 propone la matriz de correspondencia e integración con ticket existente. WS30 aporta validación humana. La promoción está `not_authorized` y requiere decisión humana; P01 debe designar al responsable de `graph_ui`.
