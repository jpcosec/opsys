## REFORMULACION

**Propósito:** producir la correspondencia de alcance entre las capacidades/deltas del plan y sus repos dueños, dejando en `reconciliacion.md` una matriz que clasifique cada fila como ya cubierta, extensión de ticket existente o nuevo delta.

**Resultado:** `reconciliacion.md` actualizado con filas agrupadas por repo dueño, no por nodo del DAG, indicando correspondencia ticket/delta y responsable P01.

**Repo:** deskops (`owner_repo: deskops`).

**Límites:** no notificar, despachar ni modificar el Board de graph_ui; no producir gates de aceptación ni aprobar deltas aún indefinidos; Scion queda como ramal E con tratamiento ya registrado (WS32/33).

## AMBIGUEDADES

1. **Criterio para elegir entre extender ticket y nuevo delta.**
   Cita: «ya cubierto (...), extender ticket existente (incluido un draft del Board) o nuevo delta».
   Qué obligaría a inventar: la regla que decide cuándo una capacidad no cubierta se adjunta a un ticket/draft existente y cuándo exige un delta nuevo, pues solo se enumeran las categorías, no el criterio de elección.

2. **Granularidad de «capacidad única».**
   Cita: «una fila por delta o capacidad única (varios nodos pueden remitir a la misma fila)».
   Qué obligaría a inventar: el límite que agrupa varias capacidades en una sola fila o las separa, ya que la unidad de agrupación no queda definida.

## DRY-RUN

**Lecturas previstas:** `reconciliacion.md` existente, `dag.yaml`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`; salidas de WS02 (`auditoria/deskops.md`), WS03 (`auditoria/infraestructura.md`) y WS04 (`auditoria/ui.md`).

**Cambios previstos:** actualizar únicamente `reconciliacion.md` con la matriz agrupada por repo dueño; sin tocar Board ni tareas externas.

**Dependencias:** WS02, WS03 y WS04 como insumos de inventario y reconciliación.

**Validaciones futuras:** comprobar que cada fila tenga repo dueño, clasificación, correspondencia ticket/delta, evidencia de path/símbolo/commit cuando aplique, y responsable P01; verificar que no se hayan creado gates ni modificado el Board de graph_ui.

## FUTURO

WS07 reutiliza el registro de decisiones; WS11/12 obtienen la aceptación específica por repo receptor; el solicitante P01 acepta por delta. La designación del operador Scion corresponde al ramal E. La promoción de WS06 sigue `not_authorized` hasta preflight y decisión humana.
