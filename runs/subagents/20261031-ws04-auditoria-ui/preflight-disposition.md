# Comparación del coordinador — WS04, aceptada para despacho

Revisiones: preflight y cold v1–v4, cada una en proceso Pi nuevo, sin herramientas y con stdin DEVNULL (recibos `*-receipt.json`). El insumo final es la TaskDoc vigente; `preflight.md` guarda la reformulación final, copia de `preflight-v4.md`.

Las cuatro rondas reproducen el objetivo, el entregable único, el repo y los límites: solo lectura, sin Scion, sin contratos nuevos, sin commits del Executor. Ningún revisor confundió la tarea con implementación ni propuso ejecutar fuera del alcance. v1–v3 detectaron lagunas reales (columnas, universo, hash, roles, atribución) y se corrigieron en la TaskDoc con `deskops edit task`. Los hallazgos de v4 son detalle o quedan resueltos aquí; estas resoluciones obligan al Executor y al Tester.

## Resoluciones sobre v4
- Valores de mapeo. base reutilizada: capacidad ya en código, con path y commit. delta: ticket o fila de reconciliacion.md que la describe, aún sin cumplir. ticket: tarea o entrada de Board de graph_ui. ausencia explícita: nada de lo anterior. Se permiten combinaciones, por ejemplo base parcial + ticket.
- Mencionar el ID del nodo basta como vínculo, y se cita. Sin ID, debe describir su alcance.
- Sesión: la definición operativa de la TaskDoc rige la tabla de sesiones; Board y git status son fuentes de trabajo en curso, listadas aparte sin atribuirlas a una sesión.
- Tarea externa = todos los archivos de desk/tasks de graph_ui, y además entradas de Board sin archivo, con path y hash «sin archivo».
- SPEC: coincidencia = el plan lo cubre; discrepancia = lo cubre distinto; ausencia = una parte de la sección sin contraparte en el plan. Temas del plan que SPEC no menciona van en una nota final.
- Encargo aportado: va en ui.md. La delegación de activation.md es el único registrado; no contiene requisitos de mapeo adicionales.
