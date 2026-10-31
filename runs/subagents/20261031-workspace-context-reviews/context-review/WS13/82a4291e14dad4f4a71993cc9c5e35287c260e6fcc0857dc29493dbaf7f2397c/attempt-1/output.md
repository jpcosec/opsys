## REFORMULACION
**Propósito:** integrar en el workspace el lector documental con contexto, enlaces, explorador, pestañas, divisiones, foco e historia, mediante tres hijos coordinados.
**Resultado:** agregado no ejecutable de los deltas de WS13.1–WS13.3 sobre el ticket workspace en draft, con implementación o delta conciliado.
**Repo dueño:** `graph_ui`; rutas base `frontends/mindmap/views/workspace/`.
**Límites:** documento/fuente solo lectura; conservar Code local y rutas del host; no exigir índices nuevos; no crear otro workspace independiente; disposición como estado local; sin mutaciones.

## AMBIGUEDADES
1. **Dependencia faltante de WS06.** Cita: `integration_mode: delta_or_existing_ticket_only_after_WS06` y `depends_on: WS11, WS13.1, WS13.2, WS13.3`. WS13 exige esperar a WS06, pero no lo declara como dependencia. Obligaría a inventar si la matriz de WS06 ya está disponible, si condiciona el alcance del delta o si basta el acta de WS11.

2. **Alcance del “registro de renderer”.** Cita: `Registro de renderer en código permitido; organización de contenido procede de documentos/consultas.` No aclara si se reutiliza un registro existente o se crea uno nuevo. Obligaría a decidir una arquitectura no fijada por el nodo; si se interpreta como permiso amplio, podría exceder el delta de lector.

## DRY-RUN
**Lecturas:** guía, brief, alcance, decisiones, cobertura, reconciliación y nodos/aristas suministrados. Sin herramientas.
**Cambios previstos:** ninguno; WS13 es `aggregate` y no se ejecuta. No hay código ni artefactos que producir aquí.
**Dependencias:** WS11 y WS13.1–WS13.3; `G_UI_READ` pendiente; WS06 implícito por `integration_mode`.
**Validaciones futuras:** acta WS11 y `G_UI_READ`; cierre de los tres hijos con su aceptación; no duplicar ticket; fuente solo lectura; pruebas de los hijos.

## FUTURO
WS06 produce la matriz de correspondencias; WS11 cierra contrato y acta de aceptación; WS07 designa responsables; el humano resuelve P01/P04/P07. Los hijos implementan y WS14/15/22/23/24/27/41 consumen el agregado. La promoción sigue no autorizada y requiere preflight específico.
