## REFORMULACION

**Propósito:** documentar en el manual la operación de delegación y la revisión trazable resultantes de WS37. **Resultado:** capítulo verificado en `docs/workspace-user-manual.md` y átomos vinculados en `desk/atoms/`. **Repo dueño:** `deskops`. **Límites:** no ejecutar delegación ni sustituir el acta de WS37; no prometer operación sin `G_EXEC`; no publicar capacidades no demostradas; no salir del manual ni de átomos vinculados.

## AMBIGUEDADES

1. «cada acuerdo durable deja su átomo vinculado»: no define qué acuerdos son «durables» ni quién los identifica. Obliga al ejecutor a inventar un criterio de selección y el conjunto de átomos exigidos. Si el acta de WS37 los enumera, la ambigüedad se resuelve con ella; el input no lo garantiza.

## DRY-RUN

- **Lecturas previstas:** `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`, nodo WS38, edges WS37/WS31 y gates `G_HUMAN_DELEGATE`/`G_EXEC`.
- **Cambios previstos:** añadir sección/capítulo a `docs/workspace-user-manual.md`; crear o vincular átomos en `desk/atoms/`.
- **Dependencias:** acta de WS37 y `G_HUMAN_DELEGATE`; manual base de WS31; `G_EXEC` solo como advertencia documentada.
- **Validaciones futuras:** cada paso enlaza al acta y a operaciones reales; existe átomo vinculado por acuerdo durable; los fallos del acta quedan documentados; se indica `G_EXEC`; etiquetas, links y relación átomo→documento verificados. Nada ejecutado.

## FUTURO

WS37 produce el acta y satisface `G_HUMAN_DELEGATE`; el humano resuelve `G_HUMAN_DELEGATE` y `G_EXEC`. El TaskDoc de promoción fijará archivos, átomos y evidencia. WS31 entrega el manual base sobre el que WS38 añade el capítulo.
