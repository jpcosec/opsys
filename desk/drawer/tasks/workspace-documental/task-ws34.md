---
id: WS34
status: candidate
owner_repo: deskops
depends_on:
- WS33
- WS12
requires:
- G_EXEC
- G_SCION
- G_WRITE_CONTRACT
---

# Exponer despacho y respuesta Scion autorizados

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

runtime/; cli/commands/runtime.py o API definida; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Un adaptador público restringido para dispatch/reply, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador.

## Aceptación

G_SCION/G_EXEC pasan; agente real demuestra aceptación/fallo/respuesta. No shell arbitrario, no duplicar transporte ni mandar mensajes en la tarea de planificación.

## Dependencias

Tareas: WS33, WS12. Gates: G_EXEC, G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
