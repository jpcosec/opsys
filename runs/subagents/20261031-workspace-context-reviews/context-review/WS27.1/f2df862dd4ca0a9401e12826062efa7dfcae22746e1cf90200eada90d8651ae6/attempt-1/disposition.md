# Disposición WS27.1, tanda sobre 023a05e3

Supervisor Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Leí `output.md` completo de attempt-1 junto al contrato del nodo: title, scope, acceptance, depends_on, requires, output_scope y children. Sin agente preparatorio. No leí el bundle completo. Comprensión del encargo, no aprobación de producto.

**Fidelidad.** Fiel: propósito, repo dueño, límites y dependencias coinciden con el contrato. El dry-run describe lecturas, cambios, dependencias, errores y validación.

**Ambigüedades.**

1. «sin commits se declara que no hay historial referenciado y se usa diff working tree→HEAD». No distingue references vacías, referencias no resolubles… Clase: `detalle de promoción`. Casos de referencias: TaskDoc, dentro de la aceptación.
2. «Diff Git e historial read-only» / «Repo/rutas se resuelven por contrato WS11». No nombra el canal o API que ejecuta git log/diff ni quién lo produce;… Clase: `futuro asignado`. WS27.1 depende de WS12, cuya whitelist fija el canal; su dry-run se detiene si no lo cubre.

**Disposición.** Aceptada como comprensión del encargo, sin cambio de contrato.
