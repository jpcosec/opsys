## REFORMULACION

**Objetivo**: aplicar una lista cerrada de diez correcciones documentales en `vistas.md` (F03, F05, F12, F16, F18a, F18b y nota final), derivadas de la revisión root de WS09.

**Alcance**: una sola pasada sobre `desk/drawer/plans/workspace-documental/borradores/vistas.md`, más `runs/subagents/20261101-ws09-correccion/result-summary.md`. Cada cambio se coteja contra su fuente directa, no por rango.

**Repo**: `/home/jp/proyectos/SLDB_1/deskops`.

**Límites**: no editar user-flows, cobertura, manual, decisiones, guía, dag.yaml, helper, validadores, código ni repos hermanos. Sin commits ni revisiones. No preguntar al solicitante. Estados sin cambios: 23 bloqueado.

## AMBIGUEDADES

1. Ítem 3: «NotationDoc se clasifica por su origen real según infraestructura.md, sin cambiarlo por reflejo». No fija si NotationDoc es authored o derivado; obligaría a inventar la clasificación si no se abre `infraestructura.md:132`.
2. Ítem 4: «pendiente de confirmación y registro en WS18 al promover (dag.yaml:1222-1224)». `dag.yaml` no está incluido en el input; sin abrirlo, la redacción exacta obligaría a inventar el contenido de esas líneas.
3. Validación: «Tester independiente de solo lectura deja runs/.../tester-result-summary.md». El Executor solo escribe `result-summary.md`; podría confundirse ese archivo con un entregable propio. El encargo lo excluye, pero la sección Validation no lo aclara.

## DRY-RUN

1. Abrir fuentes citadas: `deskops/models/ritual.py`, `desk/rituals/testing.md` y `execution.md`, `auditoria/infraestructura.md`, `auditoria/deskops.md`, `user-flows.md`, `dag.yaml:1222-1224`.
2. Editar `vistas.md`:
   - F05: reemplazar Error; añadir pasos de prosa en Origen y Campos.
   - F16: corregir Error con el mismo patrón.
   - F18a: separar spec YAML authored de SpecDoc/SpecNodeDoc derivados; clasificar NotationDoc por origen.
   - F18b: cambiar «confirmada» por «prevista, pendiente de confirmación/registro en WS18».
   - F12: registrar efecto conocido de `atoms validate`; conservar advertencia de `stores check`; precisar `Corpus.rank` y `ProjectionDoc`.
   - F03: acotar «ningún comando la calcula».
   - Añadir nota «Candidaturas sin productor».
   - Actualizar Evidencia de fichas tocadas y Clase/Renderer solo si procede.
3. Escribir `result-summary.md` con tabla ítem/cambio/fuente abierta/resultado.
4. Ejecutar validaciones: `grep -c "^### F"`, `build_plan.py --check`, `validate_plan.py --check`, `context_review.py status`.
5. Errores esperables: conteo distinto de 23; fallo de build/validate por dag no renovado; tester ausente (no lo produce el Executor). **Resultado esperado**: diez ítems aplicados y ninguno más; validaciones en verde; tester focal PASS sobre bytes congelados.
