## REFORMULACION

**Propósito:** cerrar el contrato de navegación e identidad antes de implementar, dejando clasificados los huecos y los deltas que requieren recepción.

**Resultado:** `contratos/navegacion.md` con identidad/ruta/modelo opcional, origen, foco, enlaces/historia, lectura multidesk read-only, clasificación de huecos y mapa de recepción por delta; enlaces solo a actas externas ya registradas.

**Repo:** `deskops`.

**Límites:** nodo de planificación; no implementa, no muta repos ni escribe actas interrepo. El contrato básico puede cerrar sin recepción de Changes, Scion ni ViewDoc opcional; cada delta queda bloqueado hasta su propio recibo. No autoriza promoción.

## AMBIGUEDADES

1. «cada hueco clasificado instancia/vínculo/consulta/API/renderer y productor dueño antes de code». No se nombra qué repo/actor produce cada categoría de hueco ni qué hacer si las auditorías WS02–04 no asignan dueño. Obligaría al ejecutor a inventar un productor para los huecos sin dueño explícito.

## DRY-RUN

**Lecturas previstas:** guía, brief, alcance, decisiones, `dag.yaml` de WS11 y vecinos citados (WS09, WS08, WS12, WS13, WS17, WS18, WS33, WS40, WS41), y auditorías WS02–04 por dependencia transitiva.

**Cambios previstos:** redactar contrato de navegación; fijar identidad/origen/foco/enlaces; definir resolución repo/store y aliases multidesk; clasificar huecos; construir mapa delta→recepción; enlazar actas solo si ya existen.

**Dependencias:** `G_PRODUCT` satisfecho; salidas de WS09 y WS08; P01, P07 y P09. No requiere actas G_UI_READ/G_SPEC_VIEW para el contrato básico.

**Validaciones futuras:** revisión del contrato; cada hueco con categoría y dueño; APIs citadas con path/símbolo/commit; no afirmar recibos no registrados; cierre sin acta receptora; promoción sigue no autorizada.

## FUTURO

P01/receptor del repo produce las actas por delta; WS18 obtiene `G_SPEC_VIEW` al prepararse; WS12, WS13, WS40 y WS41 consumen el contrato; un humano revisa y decide la promoción.
