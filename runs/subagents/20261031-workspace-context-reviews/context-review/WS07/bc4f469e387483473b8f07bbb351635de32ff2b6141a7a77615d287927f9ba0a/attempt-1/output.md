REFORMULACION
Propósito: que el humano dueño del producto confirme o corrija P01–P09 y `baseline_proposal`, dejando registro explícito de decisiones y designaciones. Resultado: `decisiones.md` actualizado con estado, actor, fecha, evidencia, alternativas y nodos afectados; `parameters.source_mode` sincronizado; `baseline_proposal` corregido si procede. Repo dueño: `deskops`. Límites: no inventar aprobación; no editar nodos del DAG; no configurar/ejecutar Scion ni conceder G_EXEC; no autorizar ejecución; G_PRODUCT y G_WRITE_POLICY solo pasan por registro humano verificable; no tocar Board ajeno.

AMBIGUEDADES
1. «El humano dueño del producto confirma o corrige P01–P09 de decisiones.md y `baseline_proposal` de dag.yaml» y «decisiones.md; `baseline_proposal` y parameters.source_mode en dag.yaml». No se define qué es `baseline_proposal`, dónde está ni qué campos tiene. Obligaría a inventar su esquema, su contenido y si confirmarlo equivale a aprobar el plan completo o solo una parte.
2. «| P08 | Uso humano y alcance | Proyecto Taller temporal, participante humano y presupuestos propuestos en validacion-humana.md.» Ese archivo no se suministra ni figura como dependencia de WS07. Obligaría a inventar los presupuestos, el participante y qué se está aprobando exactamente en P08, o a dar por suficiente una referencia que el ejecutor no puede verificar.

DRY-RUN
Lecturas previstas: guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `dag.yaml` (parámetros, nodo WS07 y gates); los bloques edge solo como contrato vecino, sin revisarlos. Cambios previstos: estados/actor/fecha/evidencia/alternativas/nodos afectados en `decisiones.md`; valor `source_mode` editable o read_only; `baseline_proposal` si se define. No se editarán nodos, Board ni Scion. Dependencias: salida de WS06 (`reconciliacion.md`), decisión y designaciones humanas, elección P04, contenido de P08 y de `validacion-humana.md`. Validaciones futuras: evidencia de G_PRODUCT/G_WRITE_POLICY; P01 con responsables graph_ui/sldb/spec2viz y operador Scion; `source_mode` sincronizado; ausencia de aprobación inferida.

FUTURO
El humano confirma o corrige P01–P09 y designa responsables; WS11/12 aceptan por repo receptor; WS44 ejecuta su probe con el acceso registrado; WS08/09/10/44 consumen G_PRODUCT; la promoción fija archivos, pills y evidencia.
