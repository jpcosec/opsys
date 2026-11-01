REFORMULACION
WS01 fija en deskops el brief y glosario autosuficientes del workspace documental: `brief.md` debe enlazar `decisiones.md` como registro Pxx completo, conservar acuerdos textuales con actor/fuente y distinguir documento/nodo/vista/renderer/consulta/foco. Resultado: `brief.md` verificado o ajustado; repo dueño deskops; límites: no editar `decisiones.md`, no reescribir si no cambió decisión/contrato, solo `brief.md`, sin chat invisible; no cierra lifecycle ni autoriza producto. Es nodo de planificación, no agregado.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: `brief.md`, `decisiones.md`, nodo WS01 con `covered_work` y, al promover, `task-ws01.md`. Comprobar SHA256 `c36f...` de `brief.md` y que el alcance siga cubierto. Cambios previstos: ninguno si hash y decisiones/contrato no cambiaron; si cambió realmente el encargo, editar únicamente `brief.md` para mantener enlace a `decisiones.md`, acuerdos con actor/fuente y vocabulario requerido. Dependencias: ninguna en `depends_on`; consume `decisiones.md` como fuente enlazada, no como entregable propio. Gates: promoción no autorizada; revisión de coordinación. Errores esperados: archivo ausente, hash discordante, enlace roto o deriva de alcance; se registra el hueco y no se inventa sustituto. Validación futura: leer `brief.md`, verificar enlace Pxx, confirmar que `decisiones.md` no se modificó, comprobar distinciones del glosario y revisión explícita del coordinador comparando reformulación/dry-run con la intención; APTO no basta.

FUTURO
El coordinador emite hallazgos y disposición explícita; la promoción exige task-only preflight y TaskDoc. WS02–WS05 consumen el brief como base de sus auditorías. No produce autorización de producto, lifecycle cerrado ni permiso Scion.
