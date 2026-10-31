REFORMULACION
- **Propósito**: definir el encargo de una vista de solo lectura en el workspace para mostrar ejecución y trazabilidad.
- **Resultado**: UI en `graph_ui` que presenta la cadena tarea→intento→mensaje/resultado/decisión, enlaza cada elemento a su fuente y abre evidencia en el lector WS13; `completed` no equivale a aprobado/cerrado.
- **Repo**: `graph_ui`; salida acotada a `frontends/mindmap/views/workspace/execution/; tests/`.
- **Límites**: lectura, sin dispatch/reply ni aprobación; promoción `not_authorized`. Depende de WS33 y WS27; requiere G_SCION y G_UI_READ.

AMBIGUEDADES
1. «Cada mensaje, resultado y decisión se muestra bajo su intento y tarea» frente a WS33.1: «un mensaje con varios intentos o sin intento resoluble no se vincula y registra la procedencia como hueco». Obliga a inventar qué hace WS35 con mensajes no vinculados: ocultarlos, listarlos aparte o representarlos como hueco de procedencia, y cómo encajan en «cada mensaje».

DRY-RUN
- **Lecturas**: guía de revisión; nodo WS35; contratos de contexto WS33/WS33.1/WS27; gates; `brief.md`, `alcance.md`, `decisiones.md` y `cobertura.md`.
- **Cambios previstos**: implementar vista de lectura y pruebas dentro del `output_scope`; jerarquía tarea/intento/mensaje/resultado/decisión, enlaces a fuente, apertura de evidencia en WS13 y protección semántica de `completed`.
- **Dependencias**: WS27 para diff/evidencia; WS33 para referencias/decisiones vía WS33.1/WS33.2; WS13 transitivamente para lector; G_SCION producido por WS44; G_UI_READ por delta para WS35.
- **Validaciones futuras**: pruebas de jerarquía, enlaces, apertura de evidencia y no traducción de `completed`; prueba del tratamiento acordado para mensajes no vinculados; acta de recepción G_UI_READ del receptor P01.

FUTURO
WS33.1/WS33.2 producirán referencias, decisiones y huecos de procedencia; WS27.2, evidencia; WS13, el lector; WS44, contrato público de Scion. El receptor humano P01 decide la recepción G_UI_READ por delta. La promoción fijará archivos, pruebas y pills en TaskDoc.
