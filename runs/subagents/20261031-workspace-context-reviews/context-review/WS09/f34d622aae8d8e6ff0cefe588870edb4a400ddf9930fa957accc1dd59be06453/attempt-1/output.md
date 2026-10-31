REFORMULACION
WS09 es un encargo de planificación en deskops: precisar el catálogo de `borradores/vistas.md` inventariando soportes y representaciones, dejando por fila origen, contrato o «sin contrato», renderer, acción/dueño, error y estado, y distinguiendo authored, derivado y preferencia local. No implementa UI ni modifica repos ajenos; ViewDoc es grafo, no contrato universal de UI; no resuelve decisiones Pxx ni autoriza promoción.

AMBIGUEDADES
1. «Inventariar fuente, queries, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas existentes» frente a «Aplica a cada fila de las tablas de vistas.md». Obliga a decidir si el alcance se limita a las filas ya escritas o si deben añadirse filas para «vistas existentes» y categorías no listadas; sin criterio de cierre, el ejecutor inventa el conjunto inventariado.
2. «completa la ficha por fila», cuya ficha incluye «aceptación mediante user-flow», mientras la aceptación solo exige «origen, contrato..., renderer, acción/dueño, error y estado». Obliga a inventar la aceptación/user-flow de filas sin UF asociada o a decidir si ese campo queda vacío; no está definido qué campos son exigibles.

DRY-RUN
Lecturas previstas: `dag.yaml` (WS09 y edges), `vistas.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `auditoria/ui.md` vía WS04/WS10, definiciones de WS10 y user-flows de WS08. Cambios previstos: solo `borradores/vistas.md`, completando tablas y fichas; sin tocar código ni otros repos. Dependencias: WS07 (G_PRODUCT), WS10 (definiciones de estado), WS08 (UF); G_PRODUCT sigue pendiente. Validaciones futuras: comprobar campos por fila, coherencia de estados con WS10 y auditoría, y que no se prometa UI no soportada; promoción no autorizada.

FUTURO
WS07 registra decisiones y G_PRODUCT; WS10 fija disponible/propuesto/bloqueado; WS08 aporta user-flows; WS04 produce `auditoria/ui.md`; WS11 consume el catálogo; WS18/WS22/WS23 implementan vistas; el humano decide promoción y `source_mode`. Nada de esto se resuelve en WS09.
