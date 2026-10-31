REFORMULACION
- **Propósito:** planificar una búsqueda navegable dentro del workspace documental.
- **Resultado:** delta o integración en ticket existente de `graph_ui` que permita buscar con API real, abrir un resultado y volver conservando consulta y foco.
- **Repo:** `graph_ui`, con salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.
- **Límites:** texto/campos/semántica solo según API real; sin parser propio; sin cargar todo el grafo en cada tecla; promoción no autorizada, solo preflight de tarea.

AMBIGUEDADES
1. «resultados enlazan identidad y contexto». No define qué identidad ni qué contexto deben mostrarse/enlazarse, y la aceptación no lo comprueba. Obliga a inventar campos, enlace y criterio de verificación.
2. «Búsqueda vacía/error/degradación diferenciados» frente a «Sin resultados; error de backend […] y búsqueda degradada […] se ven como tres estados distintos». «Vacía» puede significar consulta vacía o ausencia de resultados. Obliga a decidir si hay un cuarto estado y cómo probarlo.

DRY-RUN
- **Lecturas:** input completo; guía, brief, alcance, decisiones, cobertura y reconciliación como contexto; contratos vecinos solo para dependencias, sin revisarlos.
- **Cambios previstos:** integrar búsqueda en `graph_ui` usando `sldb find` o su ruta en `sldb serve`, según WS03/WS11; estados diferenciados; conservar consulta y foco; sin parser ni carga total del grafo por tecla.
- **Dependencias:** WS13, G_UI_READ, auditoría de WS03, contrato de WS11 y matriz WS06 transitiva.
- **Validaciones futuras:** recorrido por teclado, distinción de estados, ausencia de carga total por tecla, pruebas en `tests/`, preflight de promoción y validación humana posterior en WS16.

FUTURO
WS03 produce la auditoría de infraestructura; WS11 fija el contrato y resuelve G_UI_READ; WS06 aporta la matriz de forma transitiva; el TaskDoc de promoción concreta archivos, escenarios y textos; una autorización humana habilita promoción; WS16 realiza la validación humana.
