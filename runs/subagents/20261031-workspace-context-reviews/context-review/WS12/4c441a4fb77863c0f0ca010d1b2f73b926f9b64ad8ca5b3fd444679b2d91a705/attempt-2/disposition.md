# Disposición WS12, revisión 9, tras la corrección de procedencia

Supervisor Claude Opus 5.5, pane `w3Y:p1`, 2026-10-31. Comparé `output.md` completo de attempt-2 con title, scope, acceptance, depends_on, requires, output_scope, output_base y children del nodo. No hubo agente preparatorio. No leí el bundle completo del intento.

**Fidelidad.** Intento 2, tras rechazar el 1 porque su FUTURO atribuía a WS34.1/34.2 fijar el timeout, contra el «no WS34» del contrato. El intento 2 dice que WS34.x consumen la política. Fiel.

**Ambigüedades.**

1. «La duración no se elige ahora: esa sección del contrato WS12 la fija al preparar esos deltas, no WS34, y su ausencia no impide cerrar el contrato núc… Clase: `futuro asignado`. El contrato fija productor (sección de WS12) y momento (al preparar WS34.1/34.2). El núcleo cierra sin ella y WS34.x se detienen si falta.
2. «Solo si falta conducta de workflow se registra un productor Deskops explícito antes de WS25.2». No dice si ese productor es nodo del DAG, tarea o sec… Clase: `detalle de promoción`. La forma del productor Deskops, si hiciera falta, se decide al registrarlo; cambiar el DAG exige revisión del plan.

**Disposición.** Aceptada, sin cambio de contrato.
