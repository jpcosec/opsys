## REFORMULACION

**Propósito:** precisar el catálogo de renderizaciones del workspace documental, convirtiendo `borradores/vistas.md` en un inventario planificable. **Resultado:** cada fila con origen, contrato o «sin contrato», renderer, acción/dueño, error y estado, más la ficha completa; clasificación authored/derivado/preferencia local; campos sin evidencia marcados no definidos con productor WS11/12 o futura implementación. **Repo dueño:** deskops; único output: `borradores/vistas.md`. **Límites:** no implementa UI, no convierte ViewDoc en contrato universal de UI, no inventa actores/APIs, no promociona ni ejecuta; depende de WS07/WS10/WS08 y G_PRODUCT ya satisfecho. Es un nodo de planificación, no un paquete ejecutable de producto.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas:** dag WS09 y gates; brief, alcance, decisiones, cobertura; `borradores/vistas.md`; auditorías WS02–04 (`auditoria/ui.md`, deskops, infraestructura); `borradores/user-flows.md` de WS08; `borradores/manual.md` de WS10; `owner-decisions.json`. **Cambios previstos:** solo editar `borradores/vistas.md`: completar cada fila y ficha; añadir estado y error; marcar «sin contrato»/«no definido»; separar filas compuestas solo con evidencia/estado independiente; clasificar componentes. **Dependencias consumidas:** WS07 (decisiones), WS10 (definiciones disponible/propuesto/bloqueado), WS08 (UFs), auditorías transitivas WS02–04. **Gates:** G_PRODUCT satisfecho; no hay gate de ejecución propio. **Errores esperados:** evidencia ausente → no definido; contrato ausente → «sin contrato»; no crear sustituto. **Validación futura:** toda fila con los seis campos, ficha completa, estados según WS10, disponibilidad actual según WS04, UFs referenciadas, sin actor/API inventados y sin cambios fuera de output_scope. No se ejecuta nada.

## FUTURO

WS11 consume el catálogo para cerrar navegación/identidad y mapear deltas; WS12 lo usa para operaciones/efectos; WS18, opcional, solo podría fijar ViewDoc si WS09/WS11 aportan selección, y se detiene si falta. La promoción de WS09 y su TaskDoc quedan a autorización humana/planificación posterior.
