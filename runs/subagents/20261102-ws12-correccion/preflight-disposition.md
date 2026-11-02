# Comparación del Supervisor — corrección de WS12, aceptada para despacho

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-02. Leí preflight completo. Reproduce objetivo y límites. Lo que marca queda fijado aquí; prevalece sobre la TaskDoc donde la precisa.

- **Derivados:** las salidas de `build_plan.py` y `render_diagram.py`. Los corre el Supervisor.
- **Medición de invalidación:** lista de `context_review.py status` tras el parche. La corre el Supervisor.
- **Decisión B:** criterio de encaje: leer el nodo WS45. Si la guarda de contenido no cabe en su entregable y aceptación de precondición sin cambiar su sentido, se propone nodo atómico. Decidir y justificar por escrito. No ampliar WS45 en silencio.
- **Decisión C:** se propone un nodo propio de admisión manual, previo a toda mutación habilitada y no dentro de WS19.1, con dueño y dependencias justificados.
- **Decisión D:** «probar» es aceptación futura del productor. Aquí no se ejecuta nada.
- **Intake SLDB:** `deskops message send --to sldb --kind unclear`, lo envía el Supervisor. Solo el gap comprobado por lectura, rotulado así.
- **Matriz:** si un hallazgo no tiene productor, «no aplica» o «gap del consumidor», con motivo.
- **Rutas ajenas:** no se tocan. `dag.yaml` se edita solo para la propuesta, sin tocar `context_review`.
