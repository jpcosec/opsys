## REFORMULACION

**Propósito:** revisar WS27 como encargo de planificación agregado que integra la revisión de cambios y evidencia junto a la TaskDoc.

**Resultado:** nodo no ejecutable; se cumple cuando WS27.1 (diff Git/historial read-only) y WS27.2 (evidencia declarada/encontrada/verificada) cumplen su aceptación. Los dependientes siguen apuntando a WS27.

**Repo dueño:** `graph_ui`, con `output_base: graph_ui:repository_root/`.

**Límites:** solo lectura, sin escribir ni revertir; el diff se acota a repo y tarea; no muestra hallazgos de integridad del store (WS29); evidencia sin modelo de comentarios nuevo; abrir soporte solo si es Markdown dentro del workspace; el resto se declara no soportado. Promoción no autorizada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** guía de revisión, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, fragmentos de `dag.yaml` para WS27, WS27.1, WS27.2 y gate `G_UI_READ`. No se leen ni revisan los bloques edge de vecinos.

**Cambios previstos:** ninguno. Esta revisión no modifica archivos, no promueve el nodo ni ejecuta código.

**Dependencias:** WS13 y WS12 como prerrequisitos; WS27.1 y WS27.2 como hijos que determinan el cierre del agregado. `G_UI_READ` está pendiente y su resolutor es WS11.

**Validaciones futuras:** comprobar que WS27.1 muestra diff/historial real y read-only por repo alcanzado por `TaskDoc.files`; comprobar que WS27.2 distingue declarada, encontrada y verificada, y abre solo soporte Markdown del workspace. El agregado solo podrá considerarse cumplido cuando ambos hijos lo estén. La aceptación de lectura deberá constar en el acta de WS11.

## FUTURO

- WS27.1 y WS27.2 implementan y validan sus aceptaciones; no se ejecutan aquí.
- WS11 produce la aceptación de `G_UI_READ`, con responsable de `graph_ui` designado explícitamente.
- Un humano decide la promoción; el TaskDoc fijará archivos y pruebas.
- WS28 y WS35 consumen WS27 como dependencia, sin que esta revisión los evalúe.
