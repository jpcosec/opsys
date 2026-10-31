---
id: WS34
status: candidate
owner_repo: deskops
node_role: aggregate
children:
- WS34.1
- WS34.2
depends_on:
- WS33
- WS12
- WS34.1
- WS34.2
requires:
- G_EXEC
- G_SCION
- G_WRITE_CONTRACT
---

# Exponer despacho y respuesta Scion autorizados

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

Agregado: salidas de WS34.1, WS34.2

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Un adaptador público restringido para dispatch/reply, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.

## Aceptación

Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación. Sus dependientes siguen dependiendo de este ID.

## Dependencias

Tareas: WS33, WS12, WS34.1, WS34.2. Gates: G_EXEC, G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS34/9953c6f507c75f69c9a619c79a2e8f2e241b47ac30a7a7594a5e53502d6a1760/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
