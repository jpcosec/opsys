## REFORMULACION

**Propósito:** nodo agregado que cierra la revisión de cambios y evidencia del workspace, agrupando WS27.1 (diff Git) y WS27.2 (evidencia declarada/encontrada/verificada).

**Resultado:** no produce artefacto propio; se cumple cuando ambos hijos cumplen su aceptación. Sus dependientes siguen dependiendo de WS27.

**Repo dueño:** graph_ui (`output_base: graph_ui:repository_root/`).

**Límites:** aggregate no ejecutable; no duplica implementación ni infiere cierre por commit; depende de WS13, WS12 y sus hijos; G_UI_READ es por delta y sigue pendiente.

## AMBIGUEDADES

Ninguna. El nodo es un agregado no ejecutable y su aceptación remite a la de sus hijos; el gate pendiente es intencional; los detalles de archivos, pruebas y textos quedan delegados al TaskDoc de promoción; y la falta de contrato o API tiene regla común de parada. Nada obliga al ejecutor de WS27 a inventar resultado, aceptación, repo, actor o límite.

## DRY-RUN

**Lecturas:** `dag.yaml#node:WS27`, hijos WS27.1/WS27.2, guía de revisión, brief, alcance, decisiones y cobertura. Los bloques edge se usan solo como contexto de dependencias, no se revisan.

**Cambios previstos:** ninguno; el agregado no se ejecuta ni genera entregable propio.

**Dependencias:** WS13 (lector), WS12 (contrato de operaciones), WS27.1 y WS27.2; G_UI_READ pendiente con evaluación `per_delta`.

**Validaciones futuras:** aceptación de ambos hijos, recibo de lectura por delta en graph_ui y preflight de promoción. No se ejecuta nada ahora.

## FUTURO

WS27.1 implementa diff/historial read-only; WS27.2 implementa los estados de evidencia y apertura de soporte; WS12 fija la correspondencia de evidencia y el canal de `deskops closeout verify`; WS13 aporta lectura, foco e historia; el receptor P01 emite el acta G_UI_READ del delta; la promoción fija TaskDoc, archivos y pruebas; WS28 integra verificación y handoff de cierre; WS35 añade la asociación a intento; WS29 cubre integridad del store. La aceptación final es decisión humana.
