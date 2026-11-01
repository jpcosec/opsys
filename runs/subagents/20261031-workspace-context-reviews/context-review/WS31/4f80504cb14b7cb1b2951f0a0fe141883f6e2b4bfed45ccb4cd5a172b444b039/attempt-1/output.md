## REFORMULACION
Propósito: publicar un manual documental básico de navegación, edición, captura, trabajo manual y revisión ya demostrados. Resultado: `docs/workspace-user-manual.md`, capturas en `docs/assets/workspace-user-manual/` y átomos vinculados, incorporando el índice de `borradores/manual.md`, limitaciones y capítulos propuestos donde falte evidencia. Repo dueño: `deskops`. Límites: no implementa producto, no ejecuta, no crea contratos ni permisos; promoción `not_authorized`; Scion solo como capítulo propuesto hasta WS38; personalización/impacto quedan propuestos sin WS29/G_HUMAN_MODEL.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, borrador de manual y nodo WS31; al ejecutar, actas de WS30/WS43, contratos inventariados por WS11/WS12, `decisiones.md`, documentación existente y, si se menciona impacto, pruebas/recibo/commit de WS29. Cambios previstos: crear/actualizar manual, assets y átomos dentro del `output_scope`; nada fuera de `deskops`. Dependencias: WS30, WS10, WS43 y `G_HUMAN_MANUAL`; contratos de navegación/operaciones vía productores inventariados. Validaciones futuras: cada instrucción referencia acta WS30 o acta de publicación WS43; links resolubles; etiquetas coherentes; cada Pxx vigente y contrato inventariado tiene átomo con fuente `atom→doc`; Tester independiente comprueba antes del cierre. Sin ejecución.

## FUTURO
WS30 produce el acta humana y satisface `G_HUMAN_MANUAL`; WS43 produce el acta de publicación real y su commit; WS11/WS12 inventarían los contratos aplicables; WS29 aporta pruebas reales si se documenta impacto; G_HUMAN_MODEL decide el capítulo de modelos; WS38 completará después el capítulo Scion. El TaskDoc de promoción fijará archivos exactos, capturas y escenarios de prueba dentro de la aceptación. La aceptación humana y la autorización de promoción corresponden al solicitante, no a este revisor.
