---
id: WS02
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS01
requires: []
---

# Inventariar superficies y operaciones Deskops

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

auditoria/deskops.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Superficie = cada archivo, comando público o modelo registrado concreto de las categorías enumeradas; una fila por superficie. Modelos y Markdown no modelado; inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs; firmas públicas, efectos Git y cierre. Modelado = tiene modelo registrado en el store (`sldb models list`); Markdown no modelado = el resto. Firmas públicas = comandos CLI de deskops y métodos de DeskopsOperations. Cierre = `deskops closeout verify|commit`.

## Aceptación

Cada fila incluye ubicación (archivo o símbolo de código) y la operación expuesta (comando o método que la lee o muta, o «dato pasivo»), con estado comprobado; no inferir modelo por carpeta. Estado comprobado = lectura citada con archivo:línea o salida de comando de solo lectura; lo no comprobado se marca «no comprobado» con causa (ausente, inaccesible o no encontrado).

## Dependencias

Tareas: WS01. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS02/13abece72d860f563c79e265f2607c2130f38e4f374549810b4cd50cb69720f2/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
