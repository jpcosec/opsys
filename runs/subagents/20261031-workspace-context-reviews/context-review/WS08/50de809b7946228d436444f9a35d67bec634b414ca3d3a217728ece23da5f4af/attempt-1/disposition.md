# Disposición WS08, ronda 4

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. error_reviewer: El singular de «nodo y gate humano» es formato de la fila por UF; cobertura.md ya lista varios nodos/gates por flujo. Cita: context-review-guide.md, «textos exactos de pantalla, nombres de archivo y casos de prueba detallados que el TaskDoc de promoción fijará».
2. error_reviewer: La aceptación exige «Cada UF» y cobertura.md cubre UF01–UF10; «manual» no añade un flujo: el manual es índice/capítulos de WS10/WS31 sobre esos mismos recorridos. Cita: cobertura.md, filas UF01–UF10; context-review-guide.md, «No cuentan: ... detalles que el nodo delega a su promoción».
3. error_reviewer: UF06 no falta: la aceptación dice «Cada UF tiene entrada/salida...» y cobertura.md incluye «UF06 delegar/intervenir»; el scope enumera temas, no la lista cerrada de UFs. Cita: cobertura.md, fila UF06; dag.yaml#node:WS08, acceptance.
4. error_reviewer: El propio scope ya asigna el modo degradado a UF07: «modo degradado (UF07, fallo de backend/dependencia)»; no hay que decidir entre variante por flujo o UF separada. Cita: dag.yaml#node:WS08, scope.
