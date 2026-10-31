## REFORMULACION
Propósito: convertir `borradores/vistas.md` en un catálogo preciso de fuentes, representaciones y renderizadores del workspace. Resultado: cada fila de las tablas y cada ficha con origen, contrato (o «sin contrato»), renderer, acción/dueño, error y estado, clasificando authored/derivado/preferencia local. Repo dueño: `deskops`, con salida limitada a `desk/drawer/plans/workspace-documental/borradores/vistas.md`. Límites: no implementar UI, no inventar actores/APIs disponibles, no tratar ViewDoc como contrato universal, no prometer consultas guardadas sin prueba de WS03. Depende de WS07/WS10/WS08; G_PRODUCT está satisfecho.

## AMBIGUEDADES
1. Cita: «Estado = disponible/propuesto/bloqueado según WS10; disponibilidad actual viene de auditoria/ui.md (WS04)». WS10 exige para «disponible» «versión/commit implementado + pruebas relevantes + acta humana del recorrido y pasos verificados». Aplicado a una fila de renderización, el ejecutor debe inventar si ese acta humana es exigible o si basta la auditoría WS04, y cuál prevalece si discrepan.

## DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, `vistas.md`, entradas de WS09 y vecinos en `dag.yaml`; por dependencia, `borradores/user-flows.md` (WS08), `borradores/manual.md` (WS10), auditorías WS02–WS04 y `auditoria/ui.md`.
Cambios previstos: reescribir cada fila de las tablas de `vistas.md` con origen, contrato, renderer, acción/dueño, error y estado; completar la ficha por fila; clasificar componentes authored/derivado/local; marcar «no definido» con productor WS11/12 o futura implementación cuando falte evidencia.
Dependencias: decisiones P01–P09 (WS07), criterios de estado de WS10, UFs de WS08, disponibilidad de WS04, contratos/capacidades de WS02–WS03.
Validaciones futuras, sin ejecutar: ninguna fila o ficha incompleta; ningún actor/API inventado; estados solo desde fuentes citadas; errores actuales solo si están auditados; filas compuestas separadas solo con evidencia/estado independiente.

## FUTURO
WS11 produce el contrato de navegación e identidad y WS12 las operaciones por delta; ambos pueden rellenar campos marcados «no definido». WS18/G_SPEC_VIEW es opcional y no bloquea. WS40 aporta el corpus para pruebas. WS16/WS30 son gates humanos de aceptación. La promoción de WS09 no está autorizada y requiere decisión humana posterior.
