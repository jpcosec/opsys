## REFORMULACION
Propósito: ejecutar el gate humano temprano de lectura y descubrimiento para UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura y UF10 arranque. Resultado: acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/acta.md`, tiempos y pruebas técnicas separados, fallos derivados a corrección y `G_HUMAN_READ` resuelto solo con aprobación humana. Repo dueño: `graph_ui`. Límites: no implementa correcciones, no crea corpus propio, no muta el baseline y no sustituye la aprobación por agente; consume WS40 y sigue `validacion-humana.md`.

## AMBIGUEDADES
1. «Fallos abren tarea de corrección en el repo dueño»: no se identifica el repo dueño por tipo de fallo ni quién crea la tarea. Obliga a inventar si la corrección corresponde a `graph_ui`, `deskops` o `sldb/pron`, y si WS16 debe abrirla pese a `promotion: not_authorized`.

## DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, validación humana, user-flows y nodo WS16 en `dag.yaml`; contratos vecinos solo como dependencias. Comprobar disponibilidad de WS14, WS15, WS08, WS40, WS41 y `G_UI_READ`. Obtener manifiesto WS40; si falta, detenerse y registrar hueco, sin corpus sustituto. Ejecutar después el recorrido humano definido, medir 20 aperturas y 10 búsquedas, probar enlace roto, backend ausente y lectura multidesk, y guardar acta versionada. Cambios previstos: acta y resolución del gate; ningún código de producto. Validaciones futuras: revisión humana explícita, tiempos separados y commit atómico del acta en el repo dueño.

## FUTURO
P08 debe designar participante y confirmar umbrales antes de WS16. WS40 produce corpus y manifiesto; WS17 enriquece índices después. El humano aprueba o rechaza el recorrido. Si hay fallo, el repo dueño crea la tarea de corrección. `G_HUMAN_READ` solo pasa con acta y decisión humana; WS30 cubrirá mutaciones y guardados.
