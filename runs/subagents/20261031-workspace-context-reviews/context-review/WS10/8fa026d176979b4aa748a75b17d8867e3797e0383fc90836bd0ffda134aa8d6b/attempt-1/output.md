REFORMULACION
WS10 es un nodo de planificación en `deskops` que debe precisar el índice y la convención de capítulos de `borradores/manual.md`: capítulos conceptuales con propósito/entradas/salidas, ejemplo fijo Taller (`graph_ui:.tmp/workspace-documental-ejemplo/`, productor WS40) y etiquetas de disponibilidad, reutilizando el manual CLI y contrastando con auditorías WS02–04 y decisiones. Resultado: solo ese borrador actualizado. Límites: no redacta el manual completo, no inventa pasos ni capturas, no implementa UI, no aborda Scion; promoción no autorizada.

AMBIGUEDADES
1. «propuesto intención sin esa evidencia; bloqueado dependencia/contrato identificado pendiente». Una capacidad sin evidencia por un contrato o dependencia pendiente cumple ambas definiciones; el nodo no fija precedencia ni el paso de “bloqueado” a “propuesto”. Obligaría a inventar la regla de etiquetado y el estado del capítulo.

DRY-RUN
Lecturas: nodo WS10 en `dag.yaml`; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `borradores/manual.md`; `auditoria/deskops.md` (WS02) y auditorías WS03/04 vía WS06/WS07; `docs/operator-manual.md`; evidencia de G_PRODUCT. Cambios previstos: solo `deskops:desk/drawer/plans/workspace-documental/borradores/manual.md`: fijar índice de capítulos con propósito/entradas/salidas, definir etiquetas disponible/propuesto/bloqueado, dejar Taller como corpus futuro de WS40 y enlazar el manual CLI. Dependencias: WS02 y WS07; WS40 aún no produce el ejemplo; no hay acta humana. Gates: G_PRODUCT satisfecho; no se exige G_HUMAN_MANUAL. Errores esperados: falta de auditoría o corpus → marcar no comprobado/futuro, sin inventar pasos; contrato ausente → detenerse y registrar hueco. Validación futura: revisor comprueba que solo cambió `manual.md`, que las definiciones y el contraste con auditorías están citados y que no hay capturas ni pasos ficticios.

FUTURO
WS09 consume el estado de WS10 para el catálogo de renderizaciones; WS31 incorpora índice y etiquetas al manual publicado; WS40 produce el corpus Taller; WS30/WS43 producen actas y publicación; un humano acepta el manual. La promoción de WS10 requiere TaskDoc/preflight no autorizados.
