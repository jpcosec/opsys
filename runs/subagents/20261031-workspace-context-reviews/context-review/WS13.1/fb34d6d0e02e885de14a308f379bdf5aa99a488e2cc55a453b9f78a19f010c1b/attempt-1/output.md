## REFORMULACION

**Propósito:** encargo de planificación para implementar, o conciliar como delta, el lector de documento en `graph_ui`: fuente Markdown solo lectura, contexto, enlaces y Code local, con selección por documento/nodo y origen preservado.

**Resultado:** código y tests en `frontends/mindmap/views/workspace/document/` —o cierre/evidencia del ticket workspace draft si el acta WS11 eligió integrarlo—.

**Repo dueño:** `graph_ui`.

**Límites:** solo lectura; mantener rutas del host; sin índices nuevos; sin workspace independiente; depende de WS11 y G_UI_READ; promoción no autorizada.

## AMBIGUEDADES

1. «Documento/fuente solo lectura, contexto, enlaces y Code local con selección por documento/nodo». El alcance incluye «contexto», pero la aceptación no lo menciona ni define qué debe mostrar o probar; el ejecutor tendría que inventar su comportamiento y su criterio de aceptación.
2. «frontends/mindmap/views/workspace/document/; endpoints si aplica; tests/». «Si aplica» no fija criterio ni endpoints; podría habilitar crear API no prevista y exceder el alcance.
3. «cambiar texto/graph/code donde exista soporte preserva origen». No define quién determina «donde exista soporte» ni remite expresamente al contrato de WS11; el ejecutor debería inventar qué representaciones cuentan.

## DRY-RUN

**Lecturas:** guide, brief, alcance, decisiones, cobertura, reconciliacion, nodo y gates de dag.yaml; cuando exista, contrato/acta de WS11.

**Cambios previstos:** ninguno en esta revisión. El ejecutor tocaría solo `document/`, endpoints justificados y tests, o cerraría el ticket draft vía acta WS11.

**Dependencias:** WS11 (contrato de navegación y acta), G_UI_READ pendiente (resolver WS11), responsable `graph_ui` designado por WS07.

**Validaciones futuras:** Markdown legible sin modelo; enlace con origen preservado; no exigir ID; no crear workspace paralelo; WS16 para lectura; preflight task-only antes de promoción.

## FUTURO

WS11 produce contrato/acta y decide entre delta o ticket draft; WS07 designa responsable de `graph_ui`; el humano resuelve P01/P07 y G_UI_READ; WS16 valida el lector; WS13.2/WS13.3 consumen esta salida; la promoción exige autorización humana.
