## REFORMULACION
**Propósito:** precisar el manual documental como encargo de planificación: índice, convención editorial, capítulos conceptuales, ejemplo fijo y etiqueta de disponibilidad.  
**Resultado:** `borradores/manual.md` actualizado, con definiciones verificables de disponible/propuesto/bloqueado y sin pasos ni capturas ficticios.  
**Repo:** deskops.  
**Límites:** no implementa UI, no publica el manual, no produce capturas reales; reutiliza el manual CLI existente. Depende de WS02 y WS07/G_PRODUCT; usa auditorías WS02–WS04, con WS03/WS04 por vía transitiva.

## AMBIGUEDADES
ninguna.

## DRY-RUN
**Lecturas previstas:** nodo WS10 y gate G_PRODUCT; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`; auditoría de WS02 (`auditoria/deskops.md`) y, si están disponibles por la vía transitiva declarada, WS03/WS04; `validacion-humana.md` para el ejemplo.  
**Cambios previstos:** solo `borradores/manual.md`: índice, convención, capítulos conceptuales, ejemplo fijo y etiquetas; enlaces al manual CLI. Sin código, UI, capturas ni publicación.  
**Dependencias:** WS02 y WS07/G_PRODUCT; consumo posterior por WS09 y WS31.  
**Validaciones futuras:** cada etiqueta debe apoyarse en la auditoría; las definiciones deben ser comprobables; no debe haber pasos ni capturas ficticios; el ejemplo debe ser el fijado; los enlaces deben resolver. No se ejecuta nada.

## FUTURO
WS07 resuelve G_PRODUCT y las Pxx; P08/`validacion-humana.md` fija el ejemplo y sus umbrales. WS02–WS04 producen las auditorías. WS09 usará las etiquetas de WS10 y WS31 publicará el manual. La promoción de WS10, archivos exactos, pills, átomos y evidencia quedan para el TaskDoc y el preflight, no autorizados aquí.
