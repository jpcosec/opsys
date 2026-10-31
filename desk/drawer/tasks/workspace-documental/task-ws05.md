---
id: WS05
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS01
requires: []
---

# Inventariar identidad y API Scion

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

auditoria/scion.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Leer runtime/templates/RunDoc y API pública de Scion (endpoints/SDK documentados o exportados; no tablas ni funciones internas); separar slug/agente/intento/dispatch/mensaje/conversación y permisos (roles, scopes y operaciones autorizadas según la API pública). Lee código y documentación en deskops y en el repo scion (../scion); no contacta endpoints vivos ni usa credenciales: solo el probe de WS44 es evidencia de G_SCION. Sin crear agentes, enviar mensajes ni modificar configuración; puede leer configuración sin secretos y no muestra tokens. WS05 no produce G_SCION; el probe y sus reintentos son responsabilidad explícita de WS44, incluso si el inventario aporta observaciones.

## Aceptación

No usar tablas internas como interfaz; señalar los campos internos que no figuren en la API pública definida en el scope y capacidades que requieren API real; el inventario separa slug/agente/intento/dispatch/mensaje/conversación y permisos; marca qué capabilities requieren WS32 y WS33.

## Dependencias

Tareas: WS01. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS05/20b4bba263d18fbba66a9a5fa46157b4383c150e954dcd50b9cefd2b67c02bd7/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
