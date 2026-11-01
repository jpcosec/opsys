REFORMULACION

Propósito: dejar `brief.md` y su glosario autosuficientes para la planificación del workspace documental. Resultado: brief enlazado a `decisiones.md` como registro Pxx completo, con acuerdos textuales atribuidos y vocabulario legible. Repo dueño: `deskops`; salida limitada a `brief.md`. Límites: no implementa UI/backend, no edita `decisiones.md`, no crea chat invisible; la promoción sigue `not_authorized`. No es un agregado ni un paquete con hijos: es un nodo de entrega ya cubierto por `covered_work`, así que la ejecución hipotética es verificación y ajuste mínimo, no redacción desde cero.

AMBIGUEDADES

ninguna.

DRY-RUN

Lecturas: `brief.md`, `decisiones.md`, `dag.yaml#node:WS01` y la evidencia de `covered_work`. Cambios: si el SHA256 y el alcance coinciden, ninguno; si cambió realmente una decisión o contrato, editar solo `brief.md` para actualizar acuerdos textuales, vocabulario documento/nodo/vista/renderer/consulta/foco y el enlace a `decisiones.md`; no tocar `decisiones.md`. Dependencias: registro Pxx de `decisiones.md` y recibo `covered_work`. Gates: verificación de hash/alcance y comparación del coordinador; promoción pendiente de TaskDoc/preflight. Errores: hash distinto sin cambio justificado, Pxx ausente, enlace roto o fuente/actor no identificable → detenerse y registrar el hueco con repo dueño, sin inventar sustituto. Validación esperada: brief enlaza `decisiones.md`, Pxx completo, acuerdos con actor/fuente y glosario legible; ningún cambio fuera de `brief.md`.

FUTURO

El coordinador compara la reformulación/dry-run del review barato aislado con la intención y explicita hallazgos/disposición; APTO no basta. La promoción fija TaskDoc, archivos/pills/átomos/evidencia y preflight. Al promover auditorías, otro actor verifica el recibo `covered_work`.
