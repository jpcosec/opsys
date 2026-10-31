## REFORMULACION

**Propósito:** revisar WS23 como encargo de planificación para representar RitualDoc/StepDoc/lifecycle como procedimiento navegable. **Resultado:** vista de procedimiento con pasos y fuentes navegables, transiciones solo representadas y apertura de documentos/soporte; leer no marca pasos ni escribe estado. **Repo:** `graph_ui`; salida en `frontends/mindmap/views/workspace/procedure/; tests/`. **Límites:** candidato no autorizado; depende de WS13 y WS09; requiere G_UI_READ pendiente por delta; pruebas con corpus WS40 o store temporal real; no ejecuta transiciones.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** `task-ws23.md`, inventario/contrato de WS09, contrato de lector/historia/foco de WS13, fuente real de estado de pasos en deskops, corpus WS40 o store temporal, código existente en el ámbito de salida y tests.

**Cambios previstos:** incorporar representación de procedimiento, navegación de pasos/fuentes, transiciones en modo no accionable y estados derivados de deskops; pruebas del ámbito. Sin escrituras de estado ni acciones lifecycle.

**Dependencias:** WS09 debe aportar inventario/contrato de renderización; WS13, lectura integrada; G_UI_READ, recibo por delta. Si falta contrato o API, detenerse y registrar el hueco conforme a alcance.

**Validaciones futuras:** abrir un procedimiento y sus documentos/soporte; verificar que leer no auto-marca pasos; comprobar que todo estado mostrado procede de deskops; ejecutar pruebas sobre WS40 o store temporal; confirmar que las transiciones no son accionables.

## FUTURO

El TaskDoc de promoción fijará archivos exactos, escenarios, textos, pills y evidencia, y exigirá preflight task-only. El responsable humano y WS11 emitirán el recibo G_UI_READ correspondiente a WS23. WS40 aportará el corpus si se elige esa vía; WS09 y WS13 entregarán sus insumos. WS30 realizará la validación humana del flujo.
