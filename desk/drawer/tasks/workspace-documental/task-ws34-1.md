---
id: WS34.1
status: candidate
owner_repo: deskops
node_role: delivery
parent_id: WS34
depends_on:
- WS33
- WS12
requires:
- G_EXEC
- G_SCION
- G_WRITE_CONTRACT
---

# Exponer dispatch autorizado

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

runtime/; cli/commands/runtime.py o la API que fije el contrato WS12; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Adaptador público restringido para dispatch, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Confirmación = respuesta de la API de Scion. Autoridad del coordinador según contrato WS12.

## Aceptación

G_SCION/G_EXEC pasan; agente real demuestra un dispatch aceptado y uno rechazado o vencido por timeout. No shell arbitrario ni duplicar transporte. Dispatch real aceptado y rechazado/timeout se correlacionan al id de intento local previo WS32.1 y registros WS32.2; confirmed solo con respuesta observada Hub, sin convertir ausencia de confirmación en éxito/fallo remoto no observado.

## Dependencias

Tareas: WS33, WS12. Gates: G_EXEC, G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS34.1/104ad7961711b2dcfb9a163b3f176f9d1bc4daca4636989facf5c7313724d2bb/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
