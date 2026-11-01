## REFORMULACION
**Propósito:** fijar un brief y glosario autosuficientes del workspace documental, conservando acuerdos textuales y el vocabulario documento/nodo/vista/renderer/consulta/foco.
**Resultado:** `brief.md` en `deskops`, enlazado a `decisiones.md` como registro Pxx completo, con evidencia de `covered_work` y sin editar `decisiones.md`.
**Repo dueño:** `deskops`; `output_scope: brief.md`.
**Límites:** no reescribir si no cambió decisión/contrato; reabrir solo si cambia alcance o evidencia; sin chat invisible; promoción no autorizada y sujeto a preflight task-only.

## AMBIGUEDADES
1. «brief.md enlaza decisiones.md como registro Pxx completo». Obliga a inventar si «enlaza» exige hipervínculo, referencia textual o enumerar P01–P09 dentro de `brief.md`, y qué hace «completo» al registro.
2. «Acuerdos textuales tienen actor/fuente» junto a «Extractos textuales que delimitan intención, conservados aquí para no depender del historial». El brief no asigna actor/fuente por cita; el ejecutor tendría que inventar la fuente exacta de cada extracto.
3. «Si cambia realmente el encargo» y «no reescribir si no cambió decisión/contrato». No se fija qué cambio cuenta como material; obliga a inventar el umbral entre ajuste editorial y reapertura.

## DRY-RUN
Un ejecutor futuro leería `brief.md`, `decisiones.md`, `alcance.md`, el nodo WS01 y `covered_work`; calcularía el SHA256 de `brief.md` y lo compararía con `c36f0805…`. Si coincide y no hay cambio de decisión/contrato, no editaría nada. Si hay cambio material, editaría solo `brief.md`: acuerdos textuales con actor/fuente, glosario requerido y enlace a `decisiones.md`; nunca `decisiones.md`. No hay aristas `depends_on`; consume el registro Pxx y la evidencia existente. No hay gate asociado. Validaría hash, enlace/registro Pxx, actores/fuentes y legibilidad del glosario; el coordinator compararía reformulación/dry-run con la intención y explicitaría hallazgos. Ante `decisiones.md` ausente o hash distinto, registraría el hueco/evidencia y no inventaría sustituto. La promoción exigiría preflight y archivos/pills/evidencia concretos.

## FUTURO
El coordinator o humano compara esta revisión y dispone hallazgos; la promoción autoriza TaskDoc/preflight. WS07 reutiliza el registro de decisiones. WS02–WS05 consumen el brief como base, sin que este nodo los ejecute.
