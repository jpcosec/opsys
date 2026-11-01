## REFORMULACION

**Propósito:** dejar el brief y el glosario del workspace documental como base autosuficiente de planificación, ya redactados y respaldados por el recibo `covered_work`.

**Resultado:** `brief.md` enlaza `decisiones.md` con el registro Pxx completo, conserva acuerdos textuales con actor/fuente y mantiene legibles las distinciones documento/nodo/vista/renderer/consulta/foco. No se reescribe salvo cambio real de decisión o contrato.

**Repo:** `deskops`; `output_scope: brief.md`.

**Límites:** no editar `decisiones.md`; no usar chat invisible; no promover ni ejecutar tareas; la cobertura documental actual no acredita lifecycle cerrado ni autorización de producto.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

Un ejecutor futuro leería `brief.md`, `decisiones.md`, el nodo `WS01` de `dag.yaml` y la evidencia `covered_work` (`brief.md`, SHA256 `c36f08…`). Calcularía el SHA256 real de `brief.md` y lo compararía con el recibo. Verificaría que `brief.md` referencia `decisiones.md`, que el registro Pxx está completo y que los acuerdos textuales conservan actor/fuente y las distinciones del glosario.

Si el hash coincide y no hay cambio de decisión o contrato, no modificaría archivos: el resultado sería la verificación del recibo y del alcance. Si el encargo cambió realmente, editaría solo `brief.md`, actualizando acuerdos textuales y vocabulario sin tocar `decisiones.md`. No consumiría salidas de WS02–WS05.

Dependencias: ninguna (`depends_on: []`, `requires: []`); consume el recibo `covered_work` y la fuente `decisiones.md`. Gates: no hay gate propio en el nodo.

Errores esperados: hash distinto, falta de enlace o Pxx incompleto, o cambio de encargo no justificado. Ante ellos, detenerse y registrar el hueco; no crear sustituto ni reescribir por iniciativa propia.

Validación esperada: hash coincidente, referencia a `decisiones.md`, Pxx completo, acuerdos con actor/fuente y vocabulario legible; sin cambios fuera de `brief.md`. La comparación de reformulación/dry-run y la disposición corresponden al Coordinator; “APTO” aislado no basta.

## FUTURO

El Coordinator compara esta revisión con la intención y explicita hallazgos y disposición. La promoción sigue `not_authorized` hasta que el TaskDoc fije archivos, pills, átomos y evidencia. Si cambia el encargo, decide el humano y se edita solo `brief.md`; la recepción de auditorías y sus hashes corresponde a los nodos dependientes.
