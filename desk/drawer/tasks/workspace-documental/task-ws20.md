---
id: WS20
status: candidate
owner_repo: sldb
node_role: delivery
depends_on:
- WS12
requires:
- G_SLDB_WRITE
- G_WRITE_CONTRACT
---

# Comprobar o completar guardado fuente reversible

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `sldb`. Tamaño relativo: M.

src/sldb/api/documents/; src/sldb/cli/serve/; tests/

Base explícita: `sldb:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Primero verificar capacidad existente. Un documento raw-source se extrae/valida y guarda por API pública con revisión y preservación de campos protegidos; no sobrescribir Markdown desde browser.

## Aceptación

Reversible = guardar y volver a extraer conserva campos y secciones sin pérdida. En ambas ramas G_SOURCE exige API pública y tests de roundtrip, conflicto, recuperación tras fallo y campos protegidos. Si la capacidad existe, esos tests bastan y no se duplica código. Si falta, se implementa en sldb mediante tarea propia aceptada en G_SLDB_WRITE.

## Dependencias

Tareas: WS12. Gates: G_SLDB_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Variante

enabled_when:
  parameter: source_mode
  equals: editable

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS20/ea3dd3d1769edb6f19b5d03834decf3ce1f8c227c7a694ee1f0157536b77863a/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
