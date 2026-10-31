## REFORMULACION

**Propósito:** definir la vista de evidencia junto a una TaskDoc, mostrando estados declarada, encontrada y verificada sin inferir verificación.

**Resultado:** UI en `graph_ui` que muestra esos estados, abre soportes Markdown del workspace y declara no soportado el resto. Incluye gates/summary según el reporte real.

**Repo:** `graph_ui`; salida prevista en `frontends/mindmap/views/workspace/evidence/`, rutas de lectura del contrato WS11 y `tests/`.

**Límites:** sin modelo de comentarios nuevo; sin prueba independiente del artefacto; verificada es solo el resultado de `deskops closeout verify`; sin inferencia por extensión; reporte ausente o comando fallido se muestra como no verificable con error; no autoriza promoción ni implementación fuera del delta; depende de WS13 y WS12, y requiere G_UI_READ por delta.

## AMBIGUEDADES

Ninguna.

La correspondencia por tipo de evidencia y la salida pública de `closeout verify` tienen productor nombrado (WS12); las rutas de lectura, WS11. La ausencia de contrato se resuelve con las reglas comunes de `alcance.md`. Los estados exigidos son distinguibles y comprobables, y el comportamiento fuera de Markdown está delimitado.

## DRY-RUN

**Lecturas previstas:** guía, brief, alcance, decisiones, `dag.yaml` del nodo y vecinos; TaskDoc de promoción cuando exista.

**Cambios previstos:** componente de evidencia, resolución de referencias/archivos de TaskDoc, apertura en lector y pruebas de estados. Sin cambios en contratos ni en modelos Deskops.

**Dependencias:** WS13 entrega lector/historia/foco; WS12 entrega correspondencia por tipo, artefactos soporte y salida de `closeout verify`. G_UI_READ está pendiente y es intencional: exige acta por delta, no aceptación conjunta.

**Validaciones futuras:** declarada sin artefacto, artefacto no declarado, verificación fallida, evidencia ausente y reporte/comando fallido deben verse distintos; apertura de Markdown interno; ruta declarada y “no soportado” fuera del workspace; recepción G_UI_READ del delta.

## FUTURO

WS12 debe publicar el contrato de evidencia y la salida de verificación; WS13 debe completar el lector. El receptor P01 emite el acta G_UI_READ del delta concreto. La promoción queda supeditada a TaskDoc, archivos, pruebas y preflight, hoy no autorizados. La aceptación humana del delta no se presume.
