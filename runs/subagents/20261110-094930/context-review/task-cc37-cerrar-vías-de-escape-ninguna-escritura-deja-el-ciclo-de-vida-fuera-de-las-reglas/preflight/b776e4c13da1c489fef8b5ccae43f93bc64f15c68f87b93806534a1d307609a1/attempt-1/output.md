REFORMULACION
Propósito: implementar CC37 para que ninguna escritura deje una TaskDoc con ciclo de vida incoherente. Resultado: validador pydantic en `deskops/models/` que lee la tabla de RelationDoc del paquete; sldb lo aplica en fields update, docs update, /save y transacción; `desk update --apply` reporta sin escribir tareas inconsistentes; inventario de vías; pruebas; CHANGELOG. Repo: deskops, con los paths indicados (`deskops/models/`, `deskops/data/rules/`, `deskops/services/`, `deskops/lifecycle.py`, `deskops/workspace.py`, `deskops/cli/commands/desk.py`, `tests/`, `CHANGELOG.md`). Límites: no tocar sldb, no añadir campo «solo por transición», ni reglas de cierre, selectores, closeout resolved-by o forma del desk.

AMBIGUEDADES
1. «pasa las reglas tras desk update --apply (o el desk update reporta las inconsistentes sin escribirlas)» frente a «si alguna tarea real de los 6 desks no pasa el validador, el worker para y avisa». Obliga a inventar si reportar basta para cerrar o si toda tarea real debe pasar.
2. «Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`» frente a un `files` que no incluye `docs/`. Obliga a inventar si se crea documentación fuera del alcance declarado.
3. «Si /save no es probable sin levantar un servidor, el worker usa la función de sldb que /save llama y lo explica». «No es probable» no está definido; obliga a inventar cuándo vale la prueba indirecta.

DRY-RUN
Lecturas: TaskDoc, `models/task.py`, RelationDoc de `data/lifecycle/`, `lifecycle.py`, `closure.py`, `specs/compiler.py`, `services/tasks.py`, `workspace.py`, `desk.py`, `payload_save_steps.py` de sldb y tests citados. Cambios previstos: `model_validator` con constantes de entrada/cierre; filtro en workspace que reporta «inconsistent ... not written»; pruebas por caso y por vía sldb; CHANGELOG; posible constante de cierre. Dependencias: CC31, CC38, ramas CC35b y resolved-by, copias de los 6 desks. Validaciones futuras: pytest de a8 desde `/dev/shm`; rechazo por fields/docs/save; grep de a5; desk update sobre copias; goldens; doctor/view board.

FUTURO
El coordinador copia el inventario al TaskDoc, decide sobre tareas inconsistentes y ejecuta la suite completa; otras ramas aportan resolved-by y selectores.
