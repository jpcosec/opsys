## REFORMULACION

**Propósito:** que el Board permita enrutar explícitamente una tarea ya autorada y mostrar una capa “lista” calculada por dependencias pendientes y solapamiento de archivos, sin confundir enrutar con ejecutar.
**Resultado:** vista de enrutamiento en `frontends/mindmap/views/workspace/routing/`, usando solo endpoints autorizados por el contrato WS12, más pruebas. Enrutar añade la tarea a `tasks` del BoardDoc por operación pública; la capa lista se separa de tareas en ejecución, con dependencias pendientes o archivos solapados.
**Repo dueño:** `graph_ui` (`output_base: graph_ui:repository_root/`).
**Límites:** no se autoriza promoción (`promotion: not_authorized`); no edita status para avanzar; si falta contrato/API/permiso, la operación queda no disponible y se registra el hueco; no incluye ejecución de tareas ni closeout HTTP.

## AMBIGUEDADES

1. «la UI la distingue de una tarea en ejecución»: el input no define qué estado o campo de deskops/lifecycle significa “en ejecución” ni cómo se relaciona con “enrutada”. Obligaría a inventar el mapeo estado→representación y el criterio de distinción visual.
2. «sin archivos solapados según los `files` declarados en cada TaskDoc»: no se aclara si el solapamiento se evalúa solo dentro del repo receptor, entre repos, o por prefijo/ruta exacta. Obligaría a inventar la semántica de comparación y el alcance del cálculo.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (nodo WS26.2, vecinos WS12/WS22/WS26.1, gates), guía, brief, alcance, decisiones y cobertura.
**Cambios previstos:** archivos bajo `views/workspace/routing/`, endpoints ya autorizados por WS12 y tests; el TaskDoc de promoción fijará archivos, escenarios y textos exactos.
**Dependencias:** contrato WS12 con capability de enrutamiento y promoción; representación Board de WS22; autoría de WS26.1; gates G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.
**Validaciones futuras:** `deskops show board` tras enrutar; separación visual de capa lista; respeto de commits previos por canal autorizado; pruebas con store temporal real o corpus WS40.

## FUTURO

WS12 debe producir la whitelist/capability y el acta G_UI_WRITE; WS16 aporta G_HUMAN_READ; el agregado WS26 cierra cuando cierren sus hijos. La promoción concreta y su preflight pertenecen al TaskDoc y a la autorización humana. Las propuestas P01/P03–P06 siguen pendientes de decisión humana; no se resuelven aquí.
