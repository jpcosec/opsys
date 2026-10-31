## REFORMULACION

**Propósito:** integrar en la UI de autoría el trabajo sobre tareas: autorar desde candidato, declarar evidencia, vincular dependencias, pills y contexto, enrutar en Board y mostrar la capa lista. **Resultado:** WS26 es un agregado no ejecutable; su resultado es el de WS26.1 y WS26.2. **Repo:** `graph_ui` (`repository_root/`). **Límites:** no confundir ruta de Board con ejecución; no editar `status` para avanzar; promoción solo mediante operación completa ya admitida por WS12 o handoff; mutaciones de UI sujetas a `G_HUMAN_READ`, con desarrollo/pruebas aisladas de API posibles antes.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS26, contratos de WS26.1/WS26.2, WS12, WS22, guía, brief, alcance, decisiones, cobertura y gates. Sin ejecución.

**Cambios previstos:** ninguno en WS26 por ser agregado no ejecutable. Los hijos afectarían `frontends/mindmap/views/workspace/authoring/`, `routing/`, endpoints autorizados por WS12 y tests.

**Dependencias:** WS12 debe publicar el contrato técnico; WS22 debe entregar Board navegable; `G_CLOSEOUT` está satisfecho; `G_HUMAN_READ` lo produce WS16; `G_UI_WRITE` y `G_WRITE_CONTRACT` se reciben por delta concreto, sin aceptación conjunta.

**Validaciones futuras:** aceptación de WS26.1 sobre TaskDoc real (UF04, recarga, evidencia/dependencias/pills visibles, handoff si falta contrato Git); aceptación de WS26.2 (`deskops show board` muestra la tarea, distinción respecto de ejecución, capa lista separada, solapamiento por rutas normalizadas, no promoción nueva); WS30 valida autoría/revisión manual completas.

## FUTURO

WS12 produce el contrato de operaciones y promoción. WS22 produce la representación de Board. WS26.1 y WS26.2 ejecutan y aportan sus aceptaciones. WS16/humano produce el acta de lectura que habilita mutaciones en UI. El receptor P01 en `graph_ui` emite actas por delta para `G_UI_WRITE`; el contrato WS12 sostiene `G_WRITE_CONTRACT`. La promoción concreta (archivos, pills, átomos, evidencia y preflight) queda para el TaskDoc de promoción y la autorización humana correspondiente.
