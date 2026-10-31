## REFORMULACION

Propósito: definir el nodo que muestra errores de lectura (referencia rota, documento ausente, modelo no importable, backend caído, fuente no editable) y modo degradado en el workspace, sin borrar historial ni simular vacío. Resultado: deltas de UI y tests en `frontends/mindmap/views/workspace/errors/`, con CDN diagnosticado. Repo dueño: `graph_ui`. Límites: solo lectura; delta o ticket existente tras WS06, nunca duplicado paralelo; sin empaquetado offline; bloqueado hasta `G_UI_READ` y promoción no autorizada.

## AMBIGUEDADES

1. «error localizado sin borrar historial ni fingir vacío» (scope). Obliga a inventar el grano del error: ¿por panel, por documento, inline o global? «Localizado» también podría leerse como traducción i18n.
2. «recuperar conexión sin perder contexto» (acceptance). No define mecanismo (reintento manual, automático, backoff) ni qué contexto debe preservarse; no es comprobable sin inventar estados y criterio de éxito.
3. «CDN actual diagnosticado» (acceptance). No indica dónde se registra el diagnóstico ni qué evidencia lo demuestra; `output_scope` no incluye artefacto de evidencia, obligando a inventarlo.
4. «Leer Markdown existente cuando el soporte lo permita, informar límites reales» (acceptance). La lectura corresponde a WS13; «límites reales» no enumera cuáles ni con qué mensaje, obligando a inventar el catálogo de errores y su verificabilidad.
5. «modelo no importable, backend caído» (scope). No se especifica taxonomía ni distinción observable entre ambos; el ejecutor debe inventar detección y mensajes.

## DRY-RUN

Lecturas: guía, brief, alcance, decisiones, `dag.yaml` (WS15.1, vecinos WS13/WS15, gate `G_UI_READ`). Cambios previstos: `task-ws15-1.md`, UI en `errors/`, tests. Dependencias: WS13 (agregado), `G_UI_READ` producido por WS11, `source_mode` P04. Validaciones futuras: acta `G_UI_READ`, preflight de promoción con archivos/pills/evidencia, gate de aceptación de WS15/WS16. Sin ejecución.

## FUTURO

WS11 produce el acta `G_UI_READ`; WS06 decide integración delta/ticket; el humano resuelve P04 (`source_mode`), que determina si «fuente no editable» es caso visible; la promoción define task file y evidencia; WS16 valida lectura.
