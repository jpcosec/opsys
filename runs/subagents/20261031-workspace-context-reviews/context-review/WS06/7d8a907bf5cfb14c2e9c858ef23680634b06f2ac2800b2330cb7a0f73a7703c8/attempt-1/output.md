## REFORMULACION
WS06 es un encargo de planificación en `deskops`: partiendo de las auditorías WS02–WS04, debe producir una matriz por implementación que distinga “ya cubierto”, “extender ticket existente” o “nuevo delta”, con correspondencia ticket/delta y responsable por designar, y proponer atomización al dueño de `graph_ui` sin despachar ni modificar su Board. Resultado: `reconciliacion.md`. Límites: no ejecuta, no aprueba deltas, no produce gates y no sustituye la aceptación de WS11/12.

## AMBIGUEDADES
1. **“Registrar acuerdos de alcance con repos dueños”** frente a **“Matriz propuesta con correspondencia ticket/delta y responsable por designar; no produce gates de aceptación ni aprueba deltas que aún no están definidos.”**  
   Queda indefinido si el nodo debe obtener/registrar acuerdos reales con los repos o solo proponer una matriz. Obliga a inventar si existe consentimiento del repo dueño y si el output debe contener acuerdos o propuestas.

2. **“Proponer atomización a dueño graph_ui sin despachar ni modificar su Board.”**  
   No se identifica al dueño de `graph_ui`; P01 sigue pendiente y WS07 —que depende de WS06— es quien debe designarlo. Obliga a inventar el destinatario o a decidir si basta dejar constancia en `reconciliacion.md` sin notificar a nadie.

## DRY-RUN
- **Lecturas previstas:** `auditoria/deskops.md` (WS02), `auditoria/infraestructura.md` (WS03), `auditoria/ui.md` (WS04), `reconciliacion.md`, `dag.yaml` y fuentes de contexto (`brief.md`, `alcance.md`, `decisiones.md`, guía).
- **Cambios previstos:** actualizar `reconciliacion.md` con la matriz; ningún cambio en Board ni tareas de `graph_ui`.
- **Dependencias:** salidas de WS02–WS04; designación de responsables en P01/WS07; G_UI_READ/G_UI_WRITE pendientes.
- **Validaciones futuras:** WS11/12 obtienen aceptación específica por repo; WS07 registra designaciones; promoción no autorizada.

## FUTURO
WS11/12 obtienen la aceptación concreta de cada repo receptor. WS07 designa responsables de `graph_ui`, `sldb`, `spec2viz` y operador Scion, y registra decisiones humanas. El responsable de `graph_ui` acepta cómo integrar cada delta. WS04 puede recompobar Board/alcance. Nada de esto produce gates ni aprobación desde WS06.
