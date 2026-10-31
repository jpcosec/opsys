## REFORMULACION
Propósito: cerrar el contrato de operaciones y escritura del workspace documental. Resultado: `contratos/operaciones.md` con whitelist por operación/campo/canal/actor/revisión/Git/efectos, adapter público y estado existente/faltante. Repo dueño: `deskops`. Límites: no diseñar adapters ausentes —registrar hueco y dueño—; no implementar UI, commits ni closeout desde UI; escritura sujeta a P03–P06. `G_WRITE_POLICY` ya está satisfecho; `G_WRITE_CONTRACT`, `G_UI_WRITE` y `G_SLDB_WRITE` se evalúan por delta.

## AMBIGUEDADES
1. «Obtener recibo receptor y prueba solo para delta que se habilita». WS12 es `planning` y tiene `promotion: not_authorized`; no identifica el delta/efecto concreto, el repo receptor ni el actor que emite el recibo, y su `output_scope` solo es un contrato. Obligaría a inventar si WS12 debe ejecutar o probar una mutación, cuál, y dónde, o si el recibo corresponde a nodos dependientes.
2. «estado existente comprobado/faltante». No fija repos, versión/base ni evidencia de “comprobado” —lectura, prueba, acta—. Obligaría a inventar el universo de comprobación y el criterio para declarar una capacidad existente.
3. «workflow-protected fields». No enumera ni remite a inventario de campos; obligaría a inventar qué campos son protegidos y quedan fuera del canal de edición.

## DRY-RUN
Lecturas: `dag.yaml` (WS12 y vecinos), brief, alcance, decisiones, cobertura y guía; contratos previos de WS11/WS08 y capacidades existentes en `deskops`, `sldb` y `graph_ui`. Cambios previstos: redactar únicamente `contratos/operaciones.md`; sin código ni actas en este plan. Dependencias: WS11 y WS08; `G_WRITE_POLICY` satisfecho. Validaciones futuras: revisión de la whitelist y publicación del contrato; recibos por delta en repos receptores. Sin ejecución.

## FUTURO
WS11 produce navegación/identidad; WS08 produce user-flows; WS20 produce `G_SOURCE` y el contrato raw-source; P01 acepta deltas en graph_ui/SLDB; WS07 ya registró P03–P06. Nada de esto es ambigüedad de WS12.
