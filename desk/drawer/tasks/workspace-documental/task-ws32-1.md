---
id: WS32.1
status: candidate
owner_repo: deskops
node_role: delivery
parent_id: WS32
depends_on:
- WS05
- WS12
requires:
- G_CLOSEOUT
- G_SCION
- G_WRITE_CONTRACT
---

# Separar identidad de intento y dispatch

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

deskops/runtime/scion.py; models/run.py; services/closure.py; tests/

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Refinar el candidato de drawer de external_references.scion (no es ticket del Board), sin segundo pipeline: intento no es slug; dispatch intent (intención local registrada) y confirmed (solo respuesta Hub observada) como hechos separados del RunDoc; ambos se registran en el registro por intento que WS32.2 vuelve manifiesto canónico. Confirmed = respuesta de la API pública de Scion con la identidad que exponga, a comprobar en WS05/WS44. WS12 especifica contrato/ubicación del registro por intento (input de WS32.2), derivado del runtime real inventariado WS05; WS32.1 materializa ese registro e identidades según contrato, no inventa almacenamiento. Código models/run.py se cambia como código de modelo con registro/validación SLDB; instancias RunDoc trackeadas se crean/editan por API/CLI SLDB, sin ad hoc Markdown. Solo identidad/persistencia mediante operaciones locales reales en store temporal, SIN dispatch/reply de red ni evento Hub fingido. Registro local intent/no confirmado no afirma fallo/éxito de Hub.

## Aceptación

Dos intentos locales generan IDs distintos antes de dispatch y registro intent/no confirmado mediante operaciones reales del store temporal, sin simular respuesta Hub ni invocar red. Ningún no confirmado se etiqueta como fallo/aceptado Hub sin evidencia. WS34 (con G_EXEC) y WS37 demostrarán dispatch real fallido/confirmado y correlación exacta al id previo; contrato de integración explícito. Código modelos se registra/valida SLDB y RunDoc trackeado se edita por API/CLI, no ad hoc.

## Dependencias

Tareas: WS05, WS12. Gates: G_CLOSEOUT, G_SCION, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `scion` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS32.1/0c981e16b775b027061ed0680b7df5430c546898e56c4a2cf57d4441223f0648/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
