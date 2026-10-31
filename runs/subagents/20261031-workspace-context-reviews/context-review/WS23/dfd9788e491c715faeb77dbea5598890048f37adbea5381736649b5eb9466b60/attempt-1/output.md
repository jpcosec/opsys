## REFORMULACION

**Propósito:** definir e implementar en `graph_ui` una vista de procedimiento que represente RitualDoc/StepDoc y el lifecycle del desk sobre referencias reales. **Resultado:** pasos y fuentes navegables, transiciones visibles pero no accionables, y estado de paso únicamente leído desde deskops. **Repo dueño:** `graph_ui`, con salida en `frontends/mindmap/views/workspace/procedure/` y `tests/`. **Límites:** no escribe estado ni ejecuta transiciones; pruebas con corpus WS40 o store temporal real; depende de WS13 (lector agregado) y WS09 (catálogo de renderizaciones); `G_UI_READ` sigue pendiente de forma intencional.

## AMBIGUEDADES

ninguna.

## DRY-RUN

**Lecturas:** nodo WS23 en `dag.yaml`; glosario de `brief.md` —define RitualDoc, StepDoc, lifecycle, soporte y foco—; reglas comunes de `alcance.md`; aceptación de WS09 y del agregado WS13. Los bloques `edge` son contratos de vecinos y no se revisan.

**Cambios previstos:** renderer/vista de procedimiento y sus pruebas dentro de `output_scope`; sin backend, escritura ni transiciones accionables.

**Dependencias:** WS09 debe aportar la fila de ritual con origen, contrato, renderer, acción/dueño y error; WS13 debe aportar lector, foco e historia. `G_UI_READ` debe ser aceptado por WS11 antes de despachar código de UI; su estado pendiente no es defecto.

**Validaciones futuras:** abrir un procedimiento y sus documentos/soporte; comprobar que leer no auto-marca pasos; contrastar el estado mostrado con deskops y verificar que las transiciones no son accionables; ejecutar con store temporal real o corpus WS40. Si falta contrato, API o dato, aplica la regla común: detenerse y registrar el hueco con repo dueño, sin sustituto.

No se ejecuta nada.

## FUTURO

WS11 resuelve y evidencia `G_UI_READ`; WS30 realiza la validación humana del flujo. La promoción —TaskDoc, archivos exactos, pills, evidencia y preflight task-only— corresponde a otro nodo o a decisión humana. Las propuestas Pxx no se aprueban en esta revisión.
