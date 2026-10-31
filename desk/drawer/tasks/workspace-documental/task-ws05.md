---
id: WS05
status: candidate
owner_repo: deskops
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

Leer runtime/templates/RunDoc y API pública de Scion; separar slug/agente/intento/dispatch/mensaje/conversación y permisos. Puede registrar observaciones de API ya disponibles sin crear un segundo recibo: solo el probe de WS44 es evidencia de G_SCION. Sin agentes/mensajes/config ni mostrar tokens. WS05 no produce G_SCION; el probe y sus reintentos son responsabilidad explícita de WS44, incluso si el inventario aporta observaciones.

## Aceptación

No usar tablas internas como interfaz; señalar campos internos no expuestos y capacidades que requieren API real.

## Dependencias

Tareas: WS01. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
