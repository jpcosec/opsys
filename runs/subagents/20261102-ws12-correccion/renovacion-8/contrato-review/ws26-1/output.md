## REFORMULACION

Nodo WS26.1 (implementación, graph_ui): construir la autoría que **prepara un candidato** en `desk/drawer/tasks/` con dos recorridos: rastreado, `update` con `expected` (S02); no rastreado, propuesta + handoff a `deskops edit task` + refresco posterior. Incluye pills con reemplazo visible y validado, y `closeout_evidence` con el vocabulario cerrado. Resultado: código en `frontends/mindmap/views/workspace/authoring/` y tests. Límites: no crea tarea activa ni toca el Board (WS26.2), no rastrea por reflejo, no amplía S06 ni inventa API; depende de WS12, WS22, WS47 y WS48.

## AMBIGUEDADES

1. «endpoints autorizados por el contrato WS12»: el contrato no enumera endpoints para WS26.1; §4.2 remite la ruta y la forma de error a HO-01. Obligaría a inventar el conjunto de rutas y su contrato de error.
2. «depends_on: - WS22»: el input solo dice que WS22 corrige llamadas a métodos privados en lectura (§4.1). No precisa qué necesita WS26.1 de WS22 ni si bloquea solo lectura o también autoría; obligaría a inventar el efecto de esa dependencia.
3. «un guardado obsoleto se rechaza con 409 sin perder el texto local»: no dice si el recorrido A escribe por `POST /save` de sldb o por `/api/save` local (U01), que exige además `viewRevision`. Obligaría a inventar el canal y si la autoría tiene vista/revisión.
4. «closeout_evidence validada con el vocabulario cerrado existente» junto a «puede conservar evidencia vacía o incompleta como pendiente»: no aclara si una lista vacía se valida o se omite. Obligaría a inventar la secuencia validar/marcar pendiente.

## DRY-RUN

El ejecutor leería WS12 §3.3, 4.4, 6.3, 6.7 y el código citado de graph_ui y sldb; escribiría la vista y sus rutas bajo `output_scope`, consumiendo WS47 (guarda de contenido) y WS48 (admisión) como prerrequisitos: sin ellos, el recorrido A queda deshabilitado y se declara. Validaría con tests: A, 409 sin pérdida local y persistencia visible al recargar; B, cero escrituras HTTP, comando exacto por campo y refresco; selector con tarea activa coincidente (idéntico y prefijo) sin comando; pills validadas. Gates: `G_PAYLOAD_PRECONDITION` (WS45), acta P01 `G_UI_WRITE`, `G_HUMAN_READ` antes de usar mutaciones en la UI.

## FUTURO

WS26.2 crea la tarea activa y la enruta; WS47 y WS48 entregan las capacidades que WS26.1 consume; WS45 verifica la precondición; la autorización humana, la promoción (`not_authorized`) y el acta P01 quedan fuera del nodo.
