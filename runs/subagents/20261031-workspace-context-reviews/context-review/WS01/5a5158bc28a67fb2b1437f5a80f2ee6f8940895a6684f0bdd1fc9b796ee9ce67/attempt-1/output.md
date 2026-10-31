## REFORMULACION
- **Propósito:** fijar `brief.md` como brief y glosario autosuficientes, separando acuerdos explícitos de propuestas.
- **Resultado:** un `brief.md` revisado que permita reformular el producto sin depender de historial invisible.
- **Repo dueño:** `deskops`.
- **Límites:** nodo `planning`, `candidate`, sin ejecución autorizada; `output_scope: brief.md`; sin dependencias (`depends_on: []`); no implementa UI ni modifica tareas ajenas. No valida Pxx ni sustituye WS07.

## AMBIGUEDADES
1. **Aceptación no comprobable.** Cita: «Leer brief y reformular producto sin historial; acuerdos separados de propuestas.» No define qué evidencia demuestra que la reformulación es posible sin historial ni cómo se comprueba que acuerdos y propuestas quedaron separados. Obligaría a inventar un formato, una sección o un criterio de revisión.
2. **Alcance editorial de «fijar».** Cita: «Fijar brief y glosario autosuficientes», junto a `output_scope: brief.md`. No aclara si el ejecutor debe reescribir el brief, añadir secciones, conservar el texto actual y verificar, o producir una reformulación separada. Obligaría a inventar el artefacto y el grado de edición permitido.

## DRY-RUN
- **Lecturas previstas:** `brief.md`, `decisiones.md`, `alcance.md`, `cobertura.md`, `vision.md` y esta guía; `dag.yaml` solo para WS01.
- **Cambios previstos:** editar únicamente `brief.md` dentro de `desk/drawer/plans/workspace-documental/`.
- **Dependencias:** ninguna; WS02–WS05 dependen de WS01.
- **Validaciones futuras:** revisión humana de autosuficiencia y separación acuerdos/propuestas; promoción sigue `not_authorized` y requiere preflight task-only.

## FUTURO
La revisión humana o WS07 confirma el texto y el estado de las propuestas; WS02–WS05 consumen el brief fijado. La promoción y cualquier cambio fuera de `brief.md` corresponden a otro nodo o decisión humana, no a este encargo.
