## REFORMULACION
Propósito: precisar el catálogo de renderizaciones del workspace. Resultado: `borradores/vistas.md` con cada fila inventariada. Repo dueño: `deskops`. Límites: nodo de planificación; no ejecutar, no implementar UI, no revisar los bloques edge vecinos, no inventar contratos/APIs/permisos, no tratar ViewDoc como contrato universal de UI; `G_PRODUCT` ya está satisfecho y la promoción no está autorizada.

## AMBIGUEDADES
1. Filas compuestas frente a campos singulares. Cita: «Cada fila tiene origen, contrato [...], renderer, acción/dueño, error y estado», junto a la fila «Board y sus referencias | Lista, tablero, dependencias | Abrir tareas/contexto/rituales; operaciones de enrutamiento». Obliga a inventar si se agregan varios contratos, renderers, dueños, errores y estados en una sola fila o si se dividen filas; la aceptación no lo define.
2. Error en filas no disponibles. Cita: «error = fallo visible esperado para esa fila». Para filas `propuesto`/`bloqueado` o «sin contrato» no existe un fallo visible actual; obliga a inventar un error esperado o una convención para representar su ausencia.
3. Clasificación única de filas mixtas. Cita: «Distinguir authored/derivado/preferencia local», junto a «Registro de repositorios | Directorio enlazado, relaciones de desks». Una fila puede mezclar configuración authored, relaciones derivadas y preferencia local; obliga a inventar una etiqueta única o una regla de mezcla.

## DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, `vistas.md` y nodo WS09. Cambios previstos: solo editar `borradores/vistas.md`, completar fichas por fila y clasificar origen/contrato/renderer/acción/error/estado. Dependencias: WS07 (decisiones), WS10 (definiciones de estado), WS08 (user-flows). Validaciones futuras: cubrir todas las filas de las tablas, usar la taxonomía de WS10, no inventar contratos y contrastar disponibilidad con la auditoría. Sin ejecución.

## FUTURO
WS10 produce las definiciones de `disponible/propuesto/bloqueado`; WS04 produce `auditoria/ui.md`; WS08 produce los user-flows. Si falta un insumo, `alcance.md` manda detenerse y registrar el hueco, sin crear sustituto. La promoción y el TaskDoc quedan para decisión humana posterior; no son ambigüedad de este nodo.
