---
id: WS44
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS05
- WS07
requires:
- G_PRODUCT
---

# Comprobar y revalidar acceso público a Scion

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

auditoria/scion-probe.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Responsable de instalación Scion, designado por solicitante al abordar ramal E, realiza probe read-only de API con acceso ya autorizado; verifica capacidades/identidad necesarias para intento y mensajes. Sin crear agentes, enviar mensajes, cambiar config o mostrar secretos. Puede repetir el probe si el inventario WS05 terminó sin acceso. El solicitante registra en autorizaciones/scion.md qué acceso read-only tiene el operador; sin ese registro no se ejecuta el probe. El operador indica el Hub desde la configuración existente. Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33; si no las mapea por nodo, WS44 se detiene y registra el hueco antes del probe.

## Aceptación

G_SCION se satisface solo con respuesta pública real, identidad del operador (actor del probe) y Hub, fecha y capabilities registrados. Si API o acceso no están, WS44 permanece bloqueada, no se cierra unverified ni se avanza WS32. Tras cambio de Hub/API/credencial, repetir y invalidar recibo previo. Operador/acceso aún no designados: pendiente intencional solo de ramal E; no atribuir autorización al acuerdo de producto.

## Dependencias

Tareas: WS05, WS07. Gates: G_PRODUCT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS44/d7979a413a247af96dffb4ba50b711d61cf3e4992cb152e07ab5dc91b997c6b4/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
