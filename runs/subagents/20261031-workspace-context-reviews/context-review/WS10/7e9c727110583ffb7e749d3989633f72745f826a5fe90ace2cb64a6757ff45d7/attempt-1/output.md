## REFORMULACION
Propósito: fijar en `borradores/manual.md` el índice, capítulos conceptuales, un ejemplo fijo y el etiquetado de disponibilidad del manual documental, reutilizando el manual CLI y la auditoría WS02–WS04. Resultado: manual conceptual con definiciones verificables de disponible/propuesto/bloqueado, sin pasos ni capturas ficticios. Repo dueño: `deskops`. Límites: solo planificación/borrador; no implementa UI, no promete capacidades, no sustituye `docs/operator-manual.md`; promoción no autorizada.

## AMBIGUEDADES
1. Cita: «Definiciones verificables de disponible/propuesto/bloqueado» y «etiqueta de disponibilidad». No se fija qué evidencia o criterio hace verificable cada etiqueta —auditoría WS02–WS04, gate pendiente, capacidad no implementada— ni si deben aplicarse por capítulo o por capacidad. El ejecutor tendría que inventar la regla de clasificación y su comprobación.

## DRY-RUN
Lecturas: `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `manual.md`, nodo WS10, aristas WS02/WS07 y gate `G_PRODUCT`; manual CLI en `docs/operator-manual.md`; auditorías WS02–WS04 por dependencia transitiva. Cambios previstos: editar solo `borradores/manual.md` —índice, capítulos conceptuales, ejemplo fijo, etiquetas—, sin crear pasos ni capturas. Dependencias: WS02 y WS07; `G_PRODUCT` pendiente; WS03/WS04 transitivas; P08 y `source_mode` desde WS07. Validaciones futuras: contraste de definiciones con auditorías, ausencia de ficción, gate resuelto, consumo por WS09/WS31.

## FUTURO
El humano resuelve P08 —ejemplo— y P01–P09; WS07 registra `G_PRODUCT`, `source_mode` y responsables. WS02–WS04 producen auditorías; WS09 usará las etiquetas de WS10; WS31 publicará el manual probado. `G_PRODUCT` pendiente es intencional.
