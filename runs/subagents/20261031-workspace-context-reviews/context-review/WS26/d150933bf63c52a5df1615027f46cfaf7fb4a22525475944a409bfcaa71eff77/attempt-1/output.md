## REFORMULACION

**Propósito:** revisar WS26 como encargo de planificación: un agregado no ejecutable que integra autoría explícita, evidencia, dependencias, contexto/pills, enrutamiento en Board y capa lista.

**Resultado:** dictamen de claridad y comprobabilidad, sin implementar ni promover nada.

**Repo dueño:** `graph_ui`.

**Límites:** no ejecutar; no revisar los bloques `edge` de vecinos; no tratar propuestas Pxx como aprobadas; no inventar contratos ni sustituir dependencias; los gates pendientes son intencionales.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura, nodo WS26 y estados de gates. Sin herramientas ni ejecución.

**Cambios previstos:** ninguno; esta revisión no modifica el DAG, no promueve WS26 y no crea TaskDoc.

**Dependencias:** WS26 depende de WS12, WS22 y sus hijos WS26.1/WS26.2. La dependencia directa de WS12/WS22 es redundante con la de los hijos, pero no contradictoria. Gates requeridos: `G_CLOSEOUT` bloqueado; `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT` pendientes. Su estado no es defecto.

**Validaciones futuras:** WS26 cierra cuando WS26.1 y WS26.2 cumplen su aceptación; WS30 valida UF04/UF05 sobre el flujo completo. El contrato de operaciones corresponde a WS12.

## FUTURO

WS12 debe producir el contrato de operaciones y resolver `G_UI_WRITE`/`G_WRITE_CONTRACT`; WS16 produce `G_HUMAN_READ`; el closeout externo alimenta `G_CLOSEOUT`; WS26.1/WS26.2 ejecutan la autoría y el enrutamiento; WS30 realiza la validación humana. Las decisiones P03–P06 y la promoción quedan para decisión humana o TaskDoc de promoción, no para este nodo.
