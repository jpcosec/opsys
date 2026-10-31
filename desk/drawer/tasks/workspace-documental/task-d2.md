---
id: D2
status: deferred
depends_on:
- D1
owner: graph_ui + infraestructura
---

# Integrar fuente Markdown y edición estructurada

## Entregable

edición de documentos reales

## Alcance y aceptación

Reutilizar tarea de adaptador/edición existente. Fuente/render comparten identidad; escrituras por APIs del dueño con conflictos explícitos y composición con origen. Si la ruta kimun exige dependencias externas, registrarlas; no bloquear lectura ni borradores por migración.

## Dependencias y promoción

Depende de: D1. Ver [DAG](../../plans/workspace-documental/README.md). Antes de ejecutar: autoría completa, archivos exactos, pills/átomos, pruebas/evidencia, promoción y revisión en contexto limpio. No es tarea activa.

Referencia de planificación citada por softfactory_spec (archivo no disponible al validar; reconciliar en A1): `../UIs/graph_ui/desk/drawer/tasks/task-adaptador-kimun-serve-y-edicion-contextual-bidireccional.md`. Este nodo fija orden/aceptación; no acredita que exista una tarea implementable. Confirmar ubicación, restaurar o authorizar el candidato en el repo dueño antes de promoción.

conditional_prerequisites: desk/drawer/tasks/task-integracion-opsys-kimun-frontera-de-autoridad-y-modelos-desk.md (solo si se adopta backend Kimun; verificar M1/M2/C2 en repo dueño)
