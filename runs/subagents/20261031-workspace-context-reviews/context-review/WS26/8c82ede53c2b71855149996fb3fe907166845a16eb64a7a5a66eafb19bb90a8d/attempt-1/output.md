## REFORMULACION
**Propósito:** revisar WS26 como encargo de planificación, no como producto ni ejecución.  
**Resultado:** valorar si su propósito, resultado, repo, límites, dependencias y aceptación son comprensibles y comprobables.  
**Repo dueño:** `graph_ui`.  
**Límites:** WS26 es `aggregate`; no se ejecuta. Su aceptación depende de WS26.1 y WS26.2. No reviso los bloques `edge` de vecinos ni ejecuto comandos.

## AMBIGUEDADES
Ninguna.

WS26 define alcance acotado (autoría explícita, evidencia, dependencias, pill binding, enrutamiento Board y capa lista), repo `graph_ui`, hijos responsables y aceptación agregada. La promoción queda limitada a operación ya admitida por WS12 y, si falta, a handoff; WS26.2 lo concreta. Los gates pendientes son intencionales y `per_delta`.

## DRY-RUN
**Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS26, contratos de WS12/WS22/WS26.1/WS26.2 y gates.  
**Cambios previstos:** ninguno; solo informe de revisión.  
**Dependencias:** WS12 (contrato de operaciones/escritura), WS22 (Board navegable), WS26.1 y WS26.2. Las dependencias transitivas de WS12/WS22 ya están cubiertas por el DAG.  
**Validaciones futuras:** aceptación de ambos hijos; G_HUMAN_READ antes de habilitar mutaciones en UI; G_UI_WRITE y G_WRITE_CONTRACT por delta concreto; G_CLOSEOUT ya satisfecho. Desarrollo y pruebas aisladas de API pueden avanzar sin acta humana de lectura.

## FUTURO
WS12 debe producir el contrato técnico por operación/delta. WS22 debe entregar la representación navegable del Board. WS26.1 y WS26.2 producen las salidas agregadas. WS16 produce el acta de G_HUMAN_READ. El receptor P01 emite actas por delta para G_UI_WRITE. Un humano decide la aceptación de cada delta; WS26 no sustituye esas decisiones ni autoriza promoción nueva.
