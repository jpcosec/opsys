## REFORMULACION

**Propósito:** validar con una persona real el recorrido temprano de lectura y descubrimiento (UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura, UF10 arranque) sobre el corpus de WS40.
**Resultado:** acta humana y registro de fallos/tiempos en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/`.
**Repo dueño:** graph_ui (`output_base: graph_ui:repository_root/`).
**Límites:** no crea corpus propio, no implementa correcciones, no muta entre desks, no sustituye la aprobación humana, no mide guardados.

## AMBIGUEDADES

1. «supervisor del repo receptor atribuye el fallo por evidencia» — no se define quién es ese supervisor ni cómo se designa o identifica en el plan. Obligaría a inventar el actor al que WS16 debe dirigir el fallo.
2. «si aún no se aísla causa, registra incidente/diagnóstico en repo/superficie» — no se fija qué repo o superficie aloja ese registro ni el criterio para elegirlo cuando la causa es desconocida. Obligaría a inventar la ubicación y el destinatario del incidente.

## DRY-RUN

- **Lecturas previstas:** manifiesto JSON de WS40; `validacion-humana.md`; `cobertura.md`; `borradores/user-flows.md`; contratos/entradas producidos por WS11/WS14/WS15/WS41.
- **Cambios previstos:** escribir el acta en el `output_scope` indicado; registrar fallos, ayudas solicitadas, timestamps y resultados técnicos; mantener el gate pendiente ante fallo medido.
- **Dependencias:** WS14 (búsqueda), WS15 (errores/degradado y orientación sin desk), WS08 (guiones), WS40 (corpus y manifiesto), WS41 (lectura multidesk).
- **Validaciones futuras:** 20 aperturas, 10 búsquedas, arranque ≤10 s, p95 ≤2 s, sin guardados; commit atómico del acta en graph_ui; verificación de que el recorrido se completa sin rutas memorizadas ni instrucciones verbales.
- No se ejecuta nada.

## FUTURO

El humano participante realiza el recorrido y decide; el supervisor del repo receptor atribuye el fallo y abre tarea de corrección; el repo dueño versiona el acta y el recibo de G_HUMAN_READ; ese gate habilita mutaciones de baseline en UI, no desarrollo/pruebas aisladas de API; WS30 cubre guardados y UF02/UF03 edición/UF04/UF05.
