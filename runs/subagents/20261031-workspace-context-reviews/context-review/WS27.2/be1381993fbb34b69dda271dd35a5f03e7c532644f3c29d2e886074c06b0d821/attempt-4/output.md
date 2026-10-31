## REFORMULACION
Propósito: implementar en `graph_ui` una vista de evidencia junto a la TaskDoc que muestre los estados declarada, encontrada y verificada, y permita abrir su soporte. Resultado: código en `frontends/mindmap/views/workspace/evidence/` más `tests/`, con rutas de lectura fijadas por el contrato WS11. Repo dueño: `graph_ui`. Límites: sin modelo de comentarios nuevo; depende de WS13 y WS12; `requires: G_UI_READ` está pendiente (resolver WS11); `promotion: not_authorized`. No se ejecuta nada.

## AMBIGUEDADES
1. «encontrada = artefactos hallados»: no define qué fuente ni qué criterio produce un “hallazgo” (¿rutas declaradas en la TaskDoc?, ¿búsqueda en el repo?, ¿artefactos de test?). Obliga al ejecutor a inventar el mecanismo y el universo de búsqueda.
2. «una evidencia ausente se ve como ausente»: solo cubre el caso ausente; no define qué mostrar cuando declarada, encontrada y verificada discrepan (declarada sin artefacto, encontrada no declarada, verificación fallida). Obliga a inventar la semántica de estados y su combinación.
3. «Abrir soporte = abrir el artefacto en el lector»: no aclara qué lector ni qué hacer con artefactos no Markdown o fuera del workspace; `alcance.md` limita adjuntos binarios, pero el nodo no restringe “artefacto”. Obliga a inventar el manejo de esos casos.

## DRY-RUN
Lecturas previstas: `dag.yaml`, guía, brief, alcance, decisiones, cobertura; TaskDoc referenciada `desk/drawer/tasks/workspace-documental/task-ws27-2.md` (no incluida); contratos de WS11/WS12 (aún no producidos); lector de WS13.
Cambios previstos: módulo de evidencia en el `output_scope` y pruebas; ninguna escritura fuera de él.
Dependencias: WS12 (capacidad/contrato de lectura y closeout), WS13 (lector e historia/foco), `G_UI_READ` pendiente.
Validaciones futuras: pruebas de los tres estados, evidencia ausente visible, apertura de soporte; acta del gate; sin ejecución ahora.

## FUTURO
WS11 resolverá `G_UI_READ` con acta e identidad; WS12 registrará la capability y la forma del resultado de verificación; la promoción fijará archivos, escenarios y textos dentro de la aceptación; el solicitante designará responsables según P01. Si falta contrato o ruta, el ejecutor se detiene y registra el hueco conforme a `alcance.md`.
