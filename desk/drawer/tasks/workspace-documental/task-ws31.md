---
id: WS31
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS30
- WS10
- WS43
requires:
- G_HUMAN_MANUAL
---

# Publicar manual documental básico probado

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

docs/workspace-user-manual.md; docs/assets/workspace-user-manual/; desk/atoms/ vinculados

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Publicar navegación, edición, captura, trabajo manual y revisión demostradas; incorporar el índice de borradores/manual.md, capturas y limitaciones a docs/workspace-user-manual.md.

## Aceptación

Cada instrucción remite al acta de WS30 o al acta de publicación de WS43 de la versión publicada; un átomo por cada decisión Pxx humana o técnica ya registrada y vigente en decisiones.md y por cada contrato en contratos/ (navegacion.md, operaciones.md u otros de WS11/WS12); no atomizar permisos o aceptación técnica que aún no existen; etiquetas, links y atom->doc verificados. Scion se incluye solo como capítulo marcado propuesto hasta WS38. Para capítulos que mencionen personalización o impacto, comprobar G_HUMAN_MODEL/WS29 o mantener etiqueta propuesta; no bloquear manual básico por esos extras. contratos/ se resuelve en deskops:desk/drawer/plans/workspace-documental/contratos/ según output_base WS11/12; otros contratos solo si dichos productores los inventarían explícitamente. Para WS29 exigir referencia a pruebas reales/recibo y commit de su TaskDoc de ejecución; sin ella capítulo sigue propuesto. Executor del manual comprueba links resolubles, etiquetas coherentes con actas/commits y atom→doc con fuente declarada; Tester independiente verifica esos criterios antes del cierre.

## Dependencias

Tareas: WS30, WS10, WS43. Gates: G_HUMAN_MANUAL. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS31/adb1bcdd64907ba61a4b215b9975b8c25c42c2d33a8ff1b9060866762b1b414f/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
