## REFORMULACION

**Propósito:** fijar una base factual verificable —capacidades existentes, ausentes y huecos, con repo dueño— y una matriz de deltas por repo para no duplicar código. **Resultado:** auditorías de Deskops, infraestructura, UI y Scion, más `reconciliacion.md` actualizada con reutilización/ticket/delta y evidencia actual. PK01 es agrupación sin ejecución propia; su completitud depende de WS01–WS06. **Repo dueño:** deskops. **Límites:** solo lectura, sin probes vivos, sin aceptar producto, sin modificar Board/tareas ajenas, sin implementar ni autorizar tareas o aristas.

## AMBIGUEDADES

1. «WS05 inventario Scion es independiente y alimenta E». No precisa respecto a qué es independiente. Si lo es de WS01, contradice que WS05 dependa de WS01; si solo de WS06, ya se deduce. Obliga a inventar si WS05 consume brief/glosario y si su auditoría debe alinearse al vocabulario.
2. «WS06 integra sus evidencias por delta/repo». El posesivo «sus» no tiene antecedente fijo: ¿WS02–WS04, o todos los hijos incluido WS05? Obliga a decidir si la matriz debe absorber también `auditoria/scion.md`, aunque WS05 «alimenta E».
3. «cómo se probaría resultado integrado». No se define criterio ni validador de integración; WS06 solo propone correspondencia. Obliga a inventar si la prueba es cobertura de filas, re-verificación de evidencia o aceptación humana.

## DRY-RUN

Orden hipotético: WS01 —brief ya cubierto; se verifica hash/alcance y enlace a `decisiones.md`— entrega `brief.md` como entrada común. En paralelo, WS02, WS03, WS04 y WS05 leen brief; WS02 produce `auditoria/deskops.md`, WS03 `auditoria/infraestructura.md`, WS04 `auditoria/ui.md` y WS05 `auditoria/scion.md`. Después WS06 consume WS02–WS04 y escribe la matriz en `reconciliacion.md`; WS05 no entra en WS06 y pasa al ramal E. Validación integrada: cada fila de auditoría aparece o se excluye explícitamente en la matriz, cada nodo graph_ui tiene mapeo, cada delta tiene repo/ticket/responsable P01 y evidencia citada; se revisa el paquete completo contra acceptance. Sin ejecutar.

## FUTURO

WS06 produce la matriz; P01 acepta por delta en WS11/12; WS44 decide G_SCION con probe; WS07 verifica el registro de decisiones; la promoción fija el TaskDoc. No es ambigüedad.
