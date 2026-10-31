REFORMULACION
Propósito: fijar `brief.md` como base autosuficiente para reformular el producto sin historial. Resultado: `brief.md` editado en sitio con acuerdos textuales y las distinciones documento/nodo/vista/renderer/consulta/foco. Repo dueño: `deskops`. Límites: `output_scope: brief.md`; no implementar UI ni modificar tareas de otras sesiones; sin dependencias directas (`depends_on: []`). Aceptación: revisión barata sin historial y trazabilidad de acuerdos/Pxx.

AMBIGUEDADES
1. «cada propuesta del registro Pxx remite a decisiones.md». El `output_scope` es solo `brief.md`, pero el registro Pxx está en `decisiones.md`. Obligaría a inventar si se debe editar `decisiones.md` —fuera de alcance—, si basta con referenciar el registro desde `brief.md`, y qué filas P01–P09 cuentan como «propuesta».
2. «Un review barato sin historial reformula el producto solo con brief.md». No fija quién ejecuta el review ni qué se considera «reformular el producto» —cobertura, fidelidad, umbral—. Obligaría a inventar un protocolo y un criterio de aprobación.

DRY-RUN
Lecturas: nodo WS01, `brief.md`, `decisiones.md`, `alcance.md`, guía; contexto de `dag.yaml`. Los bloques edge no se revisan como contratos. Cambios previstos: solo `brief.md` si se ejecutara; en esta revisión, ninguno. Dependencias: ninguna directa; fuentes humanas ya registradas. Validaciones futuras: revisión aislada sin historial; cotejo de cada cita con el solicitante; cotejo Pxx→`decisiones.md`; presencia de las distinciones documento/nodo/vista/renderer/consulta/foco; ausencia de remisiones a chat invisible.

FUTURO
WS02–WS05 producen inventarios; WS07 verifica/reutiliza el registro de decisiones; el TaskDoc de promoción fija archivos, pills y evidencia; la persona responsable acepta deltas y revisión de uso. La promoción de WS01 sigue no autorizada.
