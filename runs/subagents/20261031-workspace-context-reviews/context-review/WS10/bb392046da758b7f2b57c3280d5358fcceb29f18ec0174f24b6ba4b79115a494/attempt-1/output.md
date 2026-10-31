## REFORMULACION
**Propósito:** precisar el índice y la convención editorial del manual documental, incluyendo ejemplo fijo y etiquetas de disponibilidad, reutilizando el manual CLI.
**Resultado:** `borradores/manual.md` actualizado con índice, capítulos conceptuales, convención de etiquetas, ejemplo Taller descrito como corpus futuro y sin capturas ni pasos inventados.
**Repo dueño:** `deskops`; `output_scope: borradores/manual.md`.
**Límites:** no escribir pasos ni capturas ficticios; usar auditorías WS02–WS04; el ejemplo Taller depende de WS40 y hasta entonces es corpus futuro; no implementar UI; promoción no autorizada.

## AMBIGUEDADES
1. **«Índice y capítulos conceptuales, ejemplo fijo y etiqueta de disponibilidad»**: no queda claro si debe redactar los capítulos conceptuales o solo precisar índice, convención y etiquetas. Obligaría a inventar qué capítulos son “conceptuales”, cuánto contenido redactar y dónde termina el encargo, con riesgo de exceder el alcance.
2. **«Definiciones verificables de disponible/propuesto/bloqueado»**: no fija contra qué evidencia se verifica cada etiqueta ni dónde se registra ese criterio. Aunque el scope indica «Usa auditoria WS02–WS04», no afirma que la verificación deba contrastarse con ellas. Obligaría a inventar el criterio de verificabilidad y el soporte de la comprobación.

## DRY-RUN
**Lecturas previstas:** nodo WS10 y gates en `dag.yaml`; `brief.md`; `alcance.md`; `decisiones.md` (P08); `cobertura.md`; `borradores/manual.md`; auditorías WS02–WS04 si están disponibles.
**Cambios previstos:** editar `borradores/manual.md` para fijar índice, convención de etiquetas, ejemplo Taller como corpus futuro y referencia al manual CLI existente.
**Dependencias:** WS02 (auditoría de superficies), WS07 (registro de decisiones y G_PRODUCT), WS04/WS03 transitivas vía WS06/WS07, WS40 para el corpus Taller.
**Validaciones futuras:** comprobar que las definiciones permitan a WS09 asignar estado; que las etiquetas tengan criterio verificable; que no haya capturas o pasos ficticios; que el ejemplo no se presente como existente antes de WS40; que se enlace —no duplique— el manual CLI; y que no se redacten capítulos operativos fuera de alcance.

## FUTURO
WS40 genera el corpus Taller; WS09 consumirá las definiciones de estado de WS10; WS31 publicará el manual probado tras WS30/WS43; el solicitante acepta deltas por repo; el TaskDoc de promoción fijará archivos exactos, pills y preflight.
