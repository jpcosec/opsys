## REFORMULACION

Encargo: corregir en el repo deskops dos defectos ante desks con el ciclo de vida anterior a CC31 (semillas managed de `desk/lifecycle/` con `attributes: {}`). (d1) `deskops doctor` debe reportar cada semilla managed desactualizada —una por archivo, qué difiere y el fix `deskops desk update --apply`— reutilizando `seed_desk(root, apply=False, restore_managed=True)`, sin comparación propia. (d2) `deskops advance` debe fallar antes de escribir, con mensaje que nombra la arista (archivo y relation_type) y su efecto `sets` ausente o divergente, sin `ValidationError` de pydantic, dejando la tarea intacta en disco. Resultado: ambos arreglados con causa raíz escrita, tests de reproducción verdes, doc en `docs/` (manual de operador) y CHANGELOG. Límites: fuera el validador de CC37, la migración del kit Chatbot_Infra y la gramática del CLI; los goldens de ayuda idénticos y los de salida solo cambian para los mensajes nuevos.

## AMBIGUEDADES

1. «severidad alert o error a decidir y justificar en el informe»: no da criterio; obliga a inventar por qué una semilla desactualizada rompe (error) o solo mueve (alert) el desk.
2. «cuyo efecto no lleva al estado que el validador exige» frente a «difiere de la semilla del paquete»: no queda claro si d2 compara contra la semilla managed o re-deriva la expectativa del validador; obliga a inventar la fuente de verdad.
3. «deskops advance falla antes de escribir»: no dice en qué capa (`lifecycle.advance` o `services/tasks.py`) ni si la lectura de semillas se hace por avance; obliga a inventar el punto de control y su coste.
4. «los de salida también, salvo los mensajes nuevos de d1 y d2, que llevan golden propio»: no fija formato exacto del mensaje; obliga a inventar su redacción golden.

## DRY-RUN

Lecturas: `deskops/lifecycle.py` (`advance`, `seed_changes`), `deskops/workspace.py` (`seed_desk`, `DeskScaffoldResult.rewritten_paths`), `deskops/data/desk_declaration.yaml`, `deskops/doctor_findings.py`, `cli/commands/doctor.py`, `models/task_lifecycle.py` (solo lectura), tests y docs. Cambios previstos: hallazgo d1 en doctor (por archivo reescrito, severidad justificada, fix `REGISTER`); pre-chequeo en `advance` que inspecciona la arista holding y aborta con mensaje que nombra archivo y relation_type; tests de reproducción y de doctor; manual de operador y CHANGELOG. Dependencias: `scaffold_store` devolviendo `rewritten`, semillas en `deskops/data/lifecycle/`, `apply_effects`. Validaciones futuras: tests de a uno con `TMPDIR=/dev/shm` y guarda pgrep; goldens de ayuda idénticos y golden propio de los mensajes nuevos; tras `desk update --apply`, doctor limpio y advance draft→active.

## FUTURO

El coordinador corre los 4 pasos del workflow en clon limpio. El dueño del kit Chatbot_Infra migra su desk con `desk update --apply`. El recibo `reproduction` debe existir como evidencia. El validador CC37 y la gramática del CLI quedan sin tocar por decisión ajena a este nodo.
