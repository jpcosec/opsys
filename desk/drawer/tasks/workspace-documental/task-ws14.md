---
id: WS14
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS13
requires:
- G_UI_READ
---

# Integrar búsqueda navegable del workspace

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/source/; views/workspace/; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Texto/campos/semántica solo según API real; resultados abren el documento con su identidad y ruta de origen. Estados diferenciados: búsqueda sin resultados, error y degradación.

## Aceptación

Usar `sldb find` o su ruta en `sldb serve`, según auditoria/infraestructura.md (producido por WS03) y contrato WS11; no parser propio. Con teclado: buscar, abrir un resultado y volver conserva consulta y foco. Sin resultados; error de backend (la API no responde o falla y la UI lo declara sin mostrar vacío); y búsqueda degradada (la API responde con capacidad parcial, p. ej. sin semántica, y la UI declara qué no cubre) se ven como tres estados distintos; no cargar todo grafo en cada tecla. Comprobar en prueba de peticiones que teclear no dispara petición de carga completa del grafo; no exige debounce/umbral nuevo, mecanismo se fija en TaskDoc.

## Dependencias

Tareas: WS13. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS14/b43901d1bf05812c99d481f2d99be88387d35481e52ba17e8d7a1bb744461755/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
