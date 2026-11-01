## REFORMULACION
Encargo de planificación WS10: precisar el índice y la convención del manual documental, no redactarlo completo. Resultado: `borradores/manual.md` con esquema de capítulos conceptuales (propósito/entradas/salidas), definiciones de disponibilidad —disponible/propuesto/bloqueado—, ejemplo fijo Taller descrito como corpus futuro hasta WS40 y referencias a productores de pruebas/actas. Repo dueño: `deskops`. Límites: no inventar pasos, capturas ni estados; reutilizar el manual CLI; contrastar con auditorías WS02–WS04; no implementar UI ni promocionar el nodo. Depende de WS02 y WS07; WS03/WS04 llegan transitivamente; `G_PRODUCT` está satisfecho.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el nodo WS10, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, el borrador `borradores/manual.md`, las auditorías WS02–WS04 y los artefactos de WS07/WS02; comprobaría `G_PRODUCT` satisfecho y que WS03/04 llegan por las aristas transitivas. Cambio previsto: editar únicamente `borradores/manual.md`, fijando índice/convención, definiciones de disponibilidad, etiquetas por capítulo, ejemplo Taller como corpus futuro y remisiones a WS30/WS31/WS38/WS39/WS40/WS43. No escribiría pasos, capturas ni nombres de controles ficticios. Si falta una auditoría o el gate no está satisfecho, se detendría y registraría el hueco con repo dueño, sin sustituirlo. Validación esperada: las tres definiciones están presentes; cada estado se contrasta con las auditorías citadas; las pruebas/actas futuras remiten a sus productores; no hay capturas ni pasos inventados; solo cambió el `output_scope`; se cumple el preflight task-only de promoción.

## FUTURO
WS31 incorporará el índice y las etiquetas a `docs/workspace-user-manual.md` tras WS30/WS43. WS09 consumirá el estado disponible/propuesto/bloqueado. WS40 generará el corpus Taller; WS30/WS43 producirán actas y publicación. La promoción de WS10 sigue `not_authorized` y requiere decisión humana y preflight task-only.
