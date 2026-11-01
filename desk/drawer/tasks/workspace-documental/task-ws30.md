---
id: WS30
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS17
- WS21
- WS22
- WS23
- WS24
- WS25
- WS26
- WS28
- WS42
requires: []
---

# Validar autoría y revisión manual completas

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

runs/subagents/workspace-documental-acceptance/manual/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Persona recorre UF02/03 edición/04/05; integra conocimiento y tarea en ejemplo; los escenarios de error, conflicto en dos ventanas y navegación por teclado del guion de WS08 y validacion-humana.md. Incluye explícitamente UF01 usando entradas authored WS17 materializadas por generador WS40, además de edición/operación; no limitarlo a búsqueda.

## Aceptación

Registro humano bajo protocolo; un fallo de guion bloquea el gate y el responsable del repo dueño abre tarea en el nodo que lo causó; una observación solo se registra. No llamar ready a un flujo solo por tests. Acta enumera plantillas/entradas WS17 validadas, paths/hashes y recorridos, para que WS43 pueda trazar publicación real. UF03 incluye edición y navegación/lectura necesarias para comprobar origen/resultado; WS16 ya cubre lectura completa. Si causa de fallo no está aislada, registrar incidente con repo/superficie y que supervisor receptor autorice diagnóstico antes de atribuir nodo; no inventar causalidad ni corregir otro repo.

## Dependencias

Tareas: WS17, WS21, WS22, WS23, WS24, WS25, WS26, WS28, WS42. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS30/3ae1d2fddc8d1254113f2f32ae1a4c7fbe792485506b5ad8245d08e37b2c898c/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
