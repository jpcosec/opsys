REFORMULACION  
Propósito: integrar una búsqueda navegable en el workspace. Resultado: UI de búsqueda que usa `sldb find` o su ruta en `sldb serve` según WS03/WS11, abre resultados con identidad y ruta de origen y conserva consulta/foco al volver. Repo dueño: `graph_ui`. Límites: solo API real, sin parser propio, sin cargar todo el grafo por tecla, requiere `G_UI_READ` y WS13; promoción no autorizada.

AMBIGUEDADES  
1. Contradicción entre scope y acceptance. Cita: «Sin resultados/error/degradación diferenciados.» frente a «Sin resultados; error de backend […] y búsqueda degradada […] se ven como tres estados distintos». Obliga a inventar si el ejecutor debe diferenciar esos estados o, por el contrario, no hacerlo.  
2. Criterio de aceptación no comprobable. Cita: «no cargar todo grafo en cada tecla». Obliga a inventar qué cuenta como «todo grafo», cómo se observa y qué umbral o instrumentación valida el cumplimiento.

DRY-RUN  
Lecturas en el input: nodo WS14, `dag.yaml`, guía, brief, alcance, decisiones, cobertura y reconciliación. Cambios previstos: implementación o delta en `frontends/mindmap/source/`, `views/workspace/` y `tests/` de `graph_ui`. Dependencias: WS13; `G_UI_READ`; WS03 y WS11 llegan de forma transitiva mediante WS11/WS13. Validaciones futuras: flujo de teclado buscar-abrir-volver con consulta y foco; tres estados diferenciados; ausencia de carga completa por tecla; evidencia de `G_UI_READ`; validación humana posterior en WS16.

FUTURO  
WS03 produce `auditoria/infraestructura.md`; WS11 produce contrato y `G_UI_READ`; WS13 aporta lector, historia y foco; el TaskDoc de promoción fijará archivos, pills, átomos, evidencias y casos de prueba; WS16 validará con humano. Nada de esto es ambigüedad ni autoriza ejecución.
