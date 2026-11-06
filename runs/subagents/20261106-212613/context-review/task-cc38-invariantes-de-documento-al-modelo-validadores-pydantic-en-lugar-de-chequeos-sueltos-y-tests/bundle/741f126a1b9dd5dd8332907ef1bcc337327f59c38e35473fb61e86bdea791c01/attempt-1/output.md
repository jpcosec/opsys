## REFORMULACION
Propósito: aplicar DK6 moviendo cada invariante de un solo documento a un validador pydantic en `deskops/models/`, borrando el chequeo suelto, e inventariando las reglas entre documentos para CC32/CC33. Resultado: inventario en el TaskDoc, validadores con tests, rechazo probado en `sldb fields update`/`docs update`, doctor sin hallazgos nuevos, goldens idénticos y CHANGELOG. Repo: deskops, worktree desde `origin/main` con CC30 integrado o desde `wt/cc30` si se autoriza. Límites: no implementa reglas entre documentos, no toca el ciclo de TaskDoc (CC37), no escribe en sldb, no cambia gramática, formato del desk ni goldens.

## AMBIGUEDADES
1. «Un chequeo mixto se parte: lo de un documento va al modelo y el resto al inventario de CC32/CC33» frente a «el chequeo viejo se borra en el mismo paso». No dice si la mitad entre documentos permanece en el código —y con qué nombre— hasta CC32/CC33 o se elimina; obligaría a inventar su ubicación y el alcance del grep.
2. «Sin cambio de gramática ni de texto de error: goldens idénticos» frente a p9 «Ningún golden lo fija». Si un chequeo sin texto CLI está fijado por un test (p. ej. `match="Unknown atom tag namespace"`), no se aclara si p9 autoriza cambiar ese texto; obligaría a elegir entre preservar test o mensaje nuevo.
3. «un test que construye el modelo con el payload malo y espera ValidationError» frente a tests existentes con `pytest.raises(ValueError)`. No define si hay que migrar esas aserciones a `pydantic.ValidationError`; obligaría a inventar el criterio.
4. Done When: «sldb fields update … es rechazado» frente a Validation: «sldb fields update y sldb docs update rechazan…». No aclara si `docs update` es bloqueante; obligaría a inventar el gate.

## DRY-RUN
Lecturas: TaskDoc, ritual, los archivos de p2 (`domain_tree.py`, `atom_tags.py`, `services/atoms.py`, `doctor.py`, `doc_access.py`, `closure.py`), modelos, grep de tests y el informe de CC30 vía `git show`. Cambios previstos: añadir validadores a los modelos afectados, borrar funciones y llamadas, hacer que servicios/doctor extraigan el mensaje sin reescribir el chequeo, mover/añadir tests y CHANGELOG; ningún golden. Dependencias: CC30 integrado, pydantic y que sldb aplique los validadores en ambas vías. Validaciones futuras: pytest archivo a archivo, goldens, cuatro casos sldb en copia bajo `/dev/shm`, `doctor`/`stores check` en los 6 desks antes y después, y greps de aceptación.

## FUTURO
CC32/CC33 implementan las RuleDoc inventariadas; CC37 cubre el ciclo de TaskDoc. Si sldb no aplica un validador, se registra hipótesis y decide el coordinador. Un documento existente inválido o la base del worktree requieren decisión del dueño/coordinador. La suite completa la corre el supervisor.
