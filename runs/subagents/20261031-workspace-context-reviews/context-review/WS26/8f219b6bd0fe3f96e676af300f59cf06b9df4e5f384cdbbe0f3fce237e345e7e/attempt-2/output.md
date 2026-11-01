## REFORMULACION

**Propósito:** integrar en graph_ui la autoría explícita desde un candidato del drawer —evidencia declarada, dependencias y contexto/pills— y el enrutamiento explícito en Board con representación de capa lista, sin confundir ruta de Board con ejecución.

**Resultado:** agregado no ejecutable; su salida es la suma de WS26.1 y WS26.2 (`output_scope: Agregado: salidas de WS26.1, WS26.2`).

**Repo dueño:** `graph_ui`.

**Límites:** no implementa promoción nueva; solo invoca una operación completa ya admitida por WS12 y, si falta, deja handoff y estado pendiente. No edita `status` para avanzar. Las mutaciones en UI quedan sujetas a G_HUMAN_READ; el desarrollo y las pruebas aisladas de API pueden avanzar con contratos/gates técnicos. Depende de WS12 y WS22, además de sus hijos; requiere G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

**Aceptación:** se cumple cuando ambos hijos cumplen la suya; los dependientes siguen colgando de WS26.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

WS26 no se ejecuta. Un ejecutor futuro promovería y ejecutaría sus hijos:

- **WS26.1** leería el candidato del drawer, el TaskDoc real, la representación Board de WS22 y el contrato WS12; escribiría la vista de autoría, endpoints autorizados y tests. Transferiría el candidato autorado con evidencia, dependencias y pills visibles tras recargar; ante una operación Git sin contrato/dueño dejaría handoff explícito. Se validaría con UF04 sobre TaskDoc real.
- **WS26.2** consumiría la autoría de WS26.1, el Board de WS22 y las operaciones de WS12; escribiría la vista de enrutamiento y tests; invocaría la operación pública para añadir la tarea al Board y mostraría la capa lista separada de ejecución y de tareas con dependencias pendientes o archivos solapados. Si falta la operación completa de promoción, prepararía handoff. Rutas con glob/no resolución quedarían como no comprobadas y con revisión de supervisor. Se validaría con `deskops show board` y distinción visual.
- **Conjunto:** ambas aceptaciones más WS30 como validación humana posterior. G_UI_WRITE y G_WRITE_CONTRACT se verifican por delta con recibos; G_HUMAN_READ antes de habilitar mutaciones UI; G_CLOSEOUT ya está satisfecho. Si falta un contrato, se registra el hueco con repo dueño y no se crea sustituto.

## FUTURO

WS12 produce el contrato de operaciones; WS22, la representación Board; WS16, el acta G_HUMAN_READ; el receptor P01 concede G_UI_WRITE por delta; WS30 valida autoría/revisión manual; el TaskDoc de promoción fija archivos, pills y evidencia.
