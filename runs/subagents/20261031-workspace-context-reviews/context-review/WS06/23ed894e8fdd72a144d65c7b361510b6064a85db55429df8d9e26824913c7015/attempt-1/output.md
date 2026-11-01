## REFORMULACION

**Propósito:** producir en `reconciliacion.md` una matriz de correspondencia por repo dueño que clasifique cada delta o capacidad única como ya cubierto (con path/símbolo y commit observado), extender ticket existente o nuevo delta, y registrar la atomización propuesta. **Resultado:** la sección matricial y la atomización en ese archivo. **Repo dueño:** deskops (nodo de planificación; la matriz describe deltas de graph_ui/sldb/spec2viz). **Límites:** no notificar, despachar ni modificar el Board de graph_ui; no ejecutar WS05; no producir gates, firmas, actas ni recepción; WS32/33 conservan sus dependencias y gates; «No designado en P01» para deskops es un dato, no un freno al trabajo local.

## AMBIGUEDADES

1. Cita: «output_scope: reconciliacion.md» y «Registrar en reconciliacion.md la atomización propuesta», frente al input, donde el mismo archivo ya contiene «## Matriz de correspondencia WS06 / Fecha: 2026-10-31» completa y secciones ajenas (Reconciliación verificada, Closeout, Recepción). Obliga a inventar si WS06 debe regenerar, ampliar o verificar lo ya escrito, y si puede sobrescribir secciones que no produce este nodo (riesgo de destruir evidencia verificada).

## DRY-RUN

- **Lecturas:** nodo WS06 y edges WS02–WS04 en `dag.yaml`; brief, alcance, decisiones, cobertura, `reconciliacion.md`; auditorías `auditoria/deskops.md`, `infraestructura.md`, `ui.md` y su `approval.md`; Board y commits citados de graph_ui/sldb/spec2viz.
- **Cambios previstos:** únicamente `reconciliacion.md` (matriz y atomización), pendiente de resolver la ambigüedad 1.
- **Dependencias:** WS02–WS04 entregadas; WS05 no se ejecuta; WS11/12 son fuente de contrato, no WS06.
- **Validaciones futuras:** revisión de este nodo y preflight/promoción vía TaskDoc; aceptación comprobable por revisión de la matriz (fila por repo, path/símbolo/commit, ticket o delta, responsable). Sin ejecución ahora.

## FUTURO

Promoción/autorización de la tarea WS06 por el canal Deskops; acta del receptor P01 por delta, en el repo dueño (no la produce WS06); WS07 reutilizará el registro de decisiones; recepción técnica de cada delta en graph_ui, sldb y spec2viz. La decisión sobre preservar o regenerar la matriz existente corresponde a un humano si se confirma la ambigüedad 1.
