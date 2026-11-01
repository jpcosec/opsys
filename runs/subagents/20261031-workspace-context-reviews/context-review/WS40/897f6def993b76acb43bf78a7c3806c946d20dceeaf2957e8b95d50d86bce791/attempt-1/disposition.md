# Disposición WS40, revisión 9, tras la corrección de procedencia

Supervisor Claude Opus 5.5, pane `w3Y:p1`, 2026-10-31. Comparé `output.md` completo de attempt-1 con title, scope, acceptance, depends_on, requires, output_scope, output_base y children del nodo. No hubo agente preparatorio. No leí el bundle completo del intento.

**Fidelidad.** Fiel: propósito, repo dueño, límites y dependencias coinciden con el contrato. El dry-run describe lecturas, cambios, dependencias, errores y validación.

**Ambigüedades.**

1. «bajo graph_ui:.tmp/workspace-documental-ejemplo/ (o tmp_path en pruebas)»: obliga a inventar si el corpus que consume WS16 debe persistir en una ruta… Clase: `no es ambigüedad`. Ruta fija para el corpus humano y tmp_path solo para pruebas: el scope los separa.
2. «imprime un manifiesto JSON con roots, stores, commits y documentos clave»: no define criterio ni lista de «documentos clave»; el ejecutor debe invent… Clase: `detalle de promoción`. La lista de documentos clave la fija el TaskDoc según lo que consumen WS16/WS30/WS41.
3. «entrada mínima ecosistema/proyecto con enlaces al Board del desk temporal, su FAQ Markdown y documentos de conocimiento»: no indica cuál de los dos d… Clase: `detalle de promoción`. Qué desk recibe la entrada mínima lo fija el TaskDoc; el manifiesto declara roots y entrada.

**Disposición.** Aceptada, sin cambio de contrato.
