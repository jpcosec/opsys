# Disposición WS26.2, revisión 9, tras la corrección de procedencia

Supervisor Claude Opus 5.5, pane `w3Y:p1`, 2026-10-31. Comparé `output.md` completo de attempt-1 con title, scope, acceptance, depends_on, requires, output_scope, output_base y children del nodo. No hubo agente preparatorio. No leí el bundle completo del intento.

**Fidelidad.** Fiel: propósito, repo dueño, límites y dependencias coinciden con el contrato. El dry-run describe lecturas, cambios, dependencias, errores y validación.

**Ambigüedades.**

1. «glob/no-resolución dudosa implica no comprobado y revisión supervisor antes de marcar lista». No se define qué hace dudosa una expansión (glob parcia… Clase: `futuro asignado`. La expansión la documenta WS12 y el ritual; el supervisor es el del repo; el umbral queda «no comprobado», nunca optimista.
2. «Tras enrutar, `deskops show board` muestra la tarea». La aceptación se apoya en un comando externo cuyo productor o contrato no consta en depends_on;… Clase: `no es ambigüedad`. `deskops show board` existe: lo comprobé con `--help`.

**Disposición.** Aceptada, sin cambio de contrato.
