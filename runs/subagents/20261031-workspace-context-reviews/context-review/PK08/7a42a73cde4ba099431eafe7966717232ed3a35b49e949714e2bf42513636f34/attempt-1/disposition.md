# Disposición PK08, ronda 6

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. error_reviewer: El input ya nombra el comprobador: «lo comprueba `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops»; el objeto hasheado es detalle de esa herramienta. Cita: context-review-guide.md, «textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará».
2. error_reviewer: El criterio ya está escrito en la propia frase: «por causa externa (ajena al encargo del propio hijo)»; afinar más el límite es caso de borde. Cita: context-review-guide.md, «No evalúas si el producto es bueno ni ejecutas nada».
3. error_reviewer: La vigencia ya se exige en la definición: «Revisión vigente: `context_review` del hijo ... cuyo hash ... coincide con los actuales y que tiene disposition.md», y el bloqueo explícito es un `context_review.status=blocked` registrado en esa disposition. El «o» alterna el estado de la revisión vigente, no exime de tenerla. Cita: dag.yaml#node:PK08, acceptance.
