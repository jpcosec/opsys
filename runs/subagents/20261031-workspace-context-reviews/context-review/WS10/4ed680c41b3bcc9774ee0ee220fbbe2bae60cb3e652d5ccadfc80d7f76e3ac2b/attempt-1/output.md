REFORMULACION  
Propósito: revisar WS10 como encargo de planificación del manual documental. Resultado: `borradores/manual.md` con índice y convención editorial precisados, ejemplo fijo y etiquetas de disponibilidad. Repo dueño: `deskops`. Límites: no implementar UI, no escribir pasos ni capturas ficticios, no ampliar alcance; usar auditoría WS02–WS04; promoción no autorizada.

AMBIGUEDADES  
1. «ejemplo fijo» (dag.yaml#node:WS10) y «con el mismo proyecto de ejemplo» (borradores/manual.md). No se identifica el proyecto, su ruta ni si se admite un marcador hasta WS40. Obligaría a inventar la identidad/contenido del ejemplo o a decidir por cuenta propia que el ejemplo queda indefinido.

DRY-RUN  
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, `borradores/manual.md`, nodo WS10, auditorías WS02/WS03/WS04 —transitivas por WS06/WS07— y manual CLI `docs/operator-manual.md`. Cambios previstos: solo `borradores/manual.md`; ordenar índice, fijar convención por capítulo, precisar el ejemplo y definir `disponible/propuesto/bloqueado` con evidencia verificable. Dependencias: WS02 y WS07; G_PRODUCT satisfecho; WS03/WS04 transitivas. Validaciones futuras: cada etiqueta debe tener criterio y fuente; no debe haber pasos/capturas ficticios; el manual CLI debe quedar enlazado; preflight de promoción posterior. Si falta el ejemplo, registrar el hueco y no sustituirlo. No ejecutar.

FUTURO  
WS40 producirá el corpus/ejemplo e instrucciones; WS09 consumirá las etiquetas de WS10 para `vistas.md`; WS31 publicará el manual probado; WS43 publicará entradas reales; WS30/WS43 aportarán actas y validación humana. La promoción de WS10 requiere TaskDoc y preflight, aún no autorizados.
