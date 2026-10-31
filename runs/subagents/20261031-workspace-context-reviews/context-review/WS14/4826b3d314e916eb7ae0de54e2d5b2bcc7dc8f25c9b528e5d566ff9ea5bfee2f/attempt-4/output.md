REFORMULACION
- **Propósito**: integrar en el workspace una búsqueda navegable sobre el API real de `sldb`, sin parser propio.
- **Resultado**: búsqueda con resultados que enlazan identidad y contexto; con teclado, buscar/abrir/volver conserva consulta y foco; estados vacío, error y degradación diferenciados; sin cargar todo el grafo en cada tecla.
- **Repo**: `graph_ui`, con salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.
- **Límites**: texto/campos/semántica solo según API real; depende de WS13 y `G_UI_READ`; no parser propio; promoción no autorizada; integración como delta o ticket existente, sin duplicar.

AMBIGUEDADES
1. «según auditoria/infraestructura.md y contrato WS11»: no se identifica qué nodo o actor produce `auditoria/infraestructura.md` ni se aporta su contenido. El ejecutor tendría que inventar si ese documento existe, quién lo emite y qué criterio de infraestructura aplica, o asumir sin base que WS11 lo cubre.
2. «Sin resultados, error de backend y búsqueda degradada se ven como tres estados distintos»: no se define qué sigue funcionando en «búsqueda degradada» ni qué la diferencia funcionalmente del error de backend. Con «no parser propio», el ejecutor tendría que inventar un fallback o el criterio de distinción entre ambos estados.

DRY-RUN
- **Lecturas previstas**: nodo WS14, guía, brief, alcance, decisiones, cobertura, reconciliación, contrato WS11 y `auditoria/infraestructura.md` cuando existan, y el TaskDoc de promoción.
- **Cambios previstos**: integrar búsqueda en `views/workspace/` o fuente de `graph_ui` y añadir pruebas; sin tocar otros repos.
- **Dependencias**: WS13 y sus hijos, más WS11 de forma transitiva; `G_UI_READ` con resolver WS11.
- **Validaciones futuras**: gate `G_UI_READ`, recorrido de teclado, tres estados diferenciados y ausencia de carga completa por tecla; validación humana en WS16. Sin ejecutar nada.

FUTURO
WS11 produce el contrato y `G_UI_READ`; WS13 entrega el lector, historia y foco; WS16 valida con humano; WS07/P01 designa al responsable de `graph_ui`; la promoción fija archivos y pruebas en el TaskDoc. Nada de ello es ambigüedad del encargo.
