---
id: WS44
status: candidate
owner_repo: deskops
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

Responsable de instalación Scion, identificado por solicitante en WS07, realiza probe read-only de API con acceso ya autorizado; verifica capacidades/identidad necesarias para intento y mensajes. Sin crear agentes, enviar mensajes, cambiar config o mostrar secretos. Puede repetir el probe si el inventario WS05 terminó sin acceso.

## Aceptación

G_SCION se satisface solo con respuesta pública real, identidad/fecha/capabilities y actor registrados. Si API o acceso no están, WS44 permanece bloqueada, no se cierra unverified ni se avanza WS32. Tras cambio de Hub/API/credencial, repetir y invalidar recibo previo.

## Dependencias

Tareas: WS05, WS07. Gates: G_PRODUCT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
