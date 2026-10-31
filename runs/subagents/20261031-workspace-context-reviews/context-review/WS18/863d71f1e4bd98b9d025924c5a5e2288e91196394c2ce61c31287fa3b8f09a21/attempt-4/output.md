## REFORMULACION

**Propósito:** declarar en spec2viz proyecciones de grafo reutilizables (ViewDoc/NotationDoc) para selecciones y notación ya soportadas, sin crear páginas UI declarativas ficticias. **Resultado:** vista portable evaluada sobre store real, con documentación de qué selecciona, y tareas receptoras promovidas por el dueño de spec2viz. **Repo dueño:** spec2viz (`sldb/views/`, `tests/`). **Límites:** no modificar el repo de spec2viz desde este plan; depende de WS09 (catálogo de renderizaciones) y WS11 (contrato de navegación/identidad); requiere G_SPEC_VIEW, aún pendiente.

## AMBIGUEDADES

1. «output_scope: sldb/views/ (nombres confirmados por contrato)» — no se identifica qué contrato ni quién confirma esos nombres. Obliga a inventar la ruta/archivo exacto o a asumir que el contrato es `contratos/navegacion.md` de WS11, que no los enumera.
2. «Vista portable evaluada sobre store real» — no fija resultado observable ni criterio de paso/fallo de esa evaluación. Obliga a inventar qué significa «evaluada» (¿render?, ¿selección correcta?, ¿ambas?). El TaskDoc puede fijar escenarios, pero solo dentro de una aceptación que aquí queda indefinida.

## DRY-RUN

**Lecturas:** guía, brief, alcance, decisiones, cobertura, nodo WS18 y contratos vecinos WS09/WS11/G_SPEC_VIEW. **Cambios previstos:** ninguno ejecutado aquí; a futuro, artefactos ViewDoc/NotationDoc en `sldb/views/` y `tests/`, más TaskDoc de promoción receptor. **Dependencias:** WS09 (inventario de vistas soportadas), WS11 (delta ViewDoc y productor de G_SPEC_VIEW), designación del responsable spec2viz por WS07, decisiones P01/P02/P07. **Validaciones futuras:** evidencia de G_SPEC_VIEW con acta receptora, prueba sobre store real/WS40, confirmación de no solapamiento y promoción por el dueño.

## FUTURO

WS11 produce la aceptación del delta y satisface G_SPEC_VIEW; WS07 designa al responsable de spec2viz; el solicitante humano resuelve P01/P02/P07; el dueño receptor promueve la tarea en spec2viz y fija archivos, escenarios y textos en el TaskDoc.
