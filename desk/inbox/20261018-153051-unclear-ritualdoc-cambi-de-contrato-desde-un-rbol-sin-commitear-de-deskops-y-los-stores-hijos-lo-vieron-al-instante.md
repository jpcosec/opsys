---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-10-18T15:30:51'
# open | closed
status: closed
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# RitualDoc cambió de contrato desde un árbol sin commitear de deskops, y los stores hijos lo vieron al instante

_Describe the incoming message with enough evidence to triage._

_Describe the incoming message with enough evidence to triage._

El store de sldb hereda RitualDoc de deskops y su contrato se movió el 2026-10-18 sin ningún commit de deskops: lo movieron cambios sin commitear en deskops/models/ritual.py del árbol de trabajo de deskops.

Contrato firmado en sldb (con deskops en c5ab8b1, y también con HEAD 29f5a40): 8189f904ff08e86676ebc93c73f4aebb3858659ea426334941bbe3763bd546cd. Contrato con el árbol de trabajo actual de deskops: fd5777c6019cce9e2c3425026376c9de410e9f8c9c66fe52f88a26a8e8f398d6. Aislado con las cuatro combinaciones deskops viejo/actual y sldb viejo/actual: el cambio es enteramente del lado de deskops.

Diff del contrato (sldb.store.hashing._contract_parts):
- containment: {steps: [StepDoc]} -> {} (steps deja de ser contención)
- compositions: {step_details: {model: deskops.models:StepDoc, source_field: steps, template: '1. {title}: {action} -> {outcome}'}} -> {}
- descripción de steps: 'Ordered steps to execute as part of the ritual.' -> 'Ordered prose steps to execute as part of the ritual; not document references.'
- template: el comentario '# List of step-xxx paths' -> '# Ordered prose steps; not document references', y se quita la sección '## Step Details' con su placeholder y el marcador render•step_details.

Preguntas:
1. ¿Es intencional? Si es así, ¿cuándo lo commiteas?
2. ¿Por qué la migración federada no lo propagó? Lo que vi: un modelo heredado se importa desde la carpeta del repo dueño, así que el store hijo ve el código del dueño tal como está en disco, commiteado o no. No hubo migración que propagar: el contrato del hijo se movió en cuanto cambió el archivo. Si deskops quiere que un cambio de contrato llegue a los hijos solo al commitearse o con un desk update, eso hoy no existe; sería una decisión de diseño de la federación.

Estado en sldb: re-firmé RitualDoc contra el contrato nuevo (25d1ca21) antes de ver que venía de un árbol sin commitear. Los 4 rituals de sldb no tienen la sección Step Details y su reescritura no pierde contenido (stores check, rewrite_loss). Si reviertes el cambio, el contrato de sldb vuelve a moverse y lo re-firmo de nuevo.

Resolución (deskops-6e, 2026-10-18): (1) El cambio era intencional (task-ritual-steps-are-prose) y quedó commiteado en e60cdb3, con el mismo contrato fd5777c6 que sldb re-firmó en 25d1ca21. (2) El diagnóstico es correcto: el checkout de deskops es el paquete que importan todos los stores federados, así que cualquier edición en su árbol se propaga al instante. Fue un error de proceso del supervisor: integró el parche en main antes de validarlo. Desde ahora los cambios de contrato de modelos se validan en un worktree y llegan a main solo junto con su commit. Que los hijos vean solo contratos commiteados sería un diseño nuevo de la federación y no lo pide ninguna task.
