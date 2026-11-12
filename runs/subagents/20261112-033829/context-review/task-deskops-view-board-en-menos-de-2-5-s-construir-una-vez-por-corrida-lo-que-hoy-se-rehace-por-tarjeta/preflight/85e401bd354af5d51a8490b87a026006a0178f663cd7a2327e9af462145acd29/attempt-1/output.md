REFORMULACION
Propósito: optimizar `deskops view board` para que, con el store construido y en un proceso nuevo, tarde ≤2,5 s (mediana de 3) en el layout del benchmark de H11, sin cambiar su salida. Resultado: construir una vez por corrida lo que hoy se rehace por tarjeta —grafo del desk, contexto de closeout y snapshot de lectura—, reduciendo aperturas del store; incluye tests, docs y CHANGELOG. Repo/superficie: deskops (`view.py`, `services/tasks.py`, `closeout_gates.py`, `lifecycle.py`, `graph/desk_graph.py`, `operations.py`, `tests/`, `docs/operator-manual.md`, `CHANGELOG.md`). Límites: no tocar sldb, no cambiar lo que muestra el board ni el contrato de la vista; `view task` solo si comparte código. No es agregado ni paquete: es una TaskDoc sin hijos (`atoms: []`); un worker futuro la ejecutaría.

AMBIGUEDADES
1. “la tarea H11 de sldb está integrada en sldb main” y “corre contra ese sldb”: no define cómo comprobar la integración ni qué commit/versión exacta usar. Obligaría a inventar el criterio de verificación.
2. “layout del benchmark de H11” / “su layout”: remite a un entorno y a `runs/.../repro.log` externos, sin comando ni datos. Obligaría a suponer ruta, fixtures y comando de benchmark.
3. “2,5 s o menos” junto con “Las mediciones van con caché frío y caliente”: no aclara si el umbral debe cumplirse en frío, en caliente o en ambos. Obligaría a fijar una condición de aceptación no escrita.
4. “la salida … es byte a byte la de antes” y “view task”: el alcance excluye `view task` salvo código compartido, pero la validación exige comparar su salida. Obligaría a decidir si ese requisito aplica siempre.
5. “las llamadas … se reducen a las necesarias”: no fija objetivo numérico ni qué llamadas son necesarias. Obligaría a inventar un umbral.

DRY-RUN
Un ejecutor leería el TaskDoc, el informe/repro de H11 y el estado de sldb; mediría y perfilaría `view board`; modificaría `view.py` y servicios para compartir grafo, closeout y snapshot por corrida; reduciría aperturas del store; compararía salidas; añadiría tests y docs. Dependencias: H11 integrado en sldb, layout de benchmark y entorno `/dev/shm`. Validaría benchmark frío/caliente, identidad de salida, perfil de llamadas, suite por archivo, `ci-knowledge-check`, `graph missing` y los 4 pasos de CI. Sin ejecutar.

FUTURO
El worker produce código, mediciones, perfil, tests, docs y CHANGELOG. El coordinador ejecuta los 4 pasos de CI y decide la aceptación; si no se alcanza la meta, el worker entrega la explicación medida y la parte atribuible a sldb.
