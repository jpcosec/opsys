### PK08 [1]
1. «cuyo hash de input y de contrato coinciden con los actuales». El input no define qué artefacto constituye el «contrato» del hijo ni cómo se calcula o conserva su hash. Obligaría a inventar el objeto hasheado y el procedimiento de comparación, salvo que se presuma que `context_review.py status` lo define por completo; el input no lo afirma.

### WS05 [2]
1. «marca qué capabilities requieren WS32 y WS33». WS33 no aparece definido en el input suministrado. Para clasificar sus capabilities el ejecutor tendría que inventar el alcance o las necesidades de WS33.
2. «API pública de Scion (endpoints/SDK documentados o exportados; no tablas ni funciones internas)». No se fija qué prevalece si documentación y exports discrepan, ni el límite exacto entre símbolo exportado y función interna. Obligaría a inventar un criterio de “público” para decidir qué campos son interfaz.
