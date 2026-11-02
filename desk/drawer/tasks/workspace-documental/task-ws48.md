---
id: WS48
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS12
requires:
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Admitir escrituras de la UI en modo manual exclusivo

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/ (módulo común de admisión de escritura; archivo exacto en el TaskDoc); tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Productor común de la evidencia de modo manual exclusivo (T-P03.1, HO-03; contrato WS12, secciones 5 y 5.9), previo a toda mutación habilitada en la UI y no contenido en WS19.1, para que ack y captura no dependan de WS19.1. Un único punto de admisión que toda ruta de escritura de la UI, existente o nueva, consulta antes de invocar su canal, con una afirmación vigente suministrada fuera de la petición (configuración confiable del responsable del desk, cargada por este nodo y sin valores reales en el repo; su formato, ubicación y vigencia los fija este nodo en su TaskDoc, no WS12, con las condiciones del contrato WS12, sección 5.9) y consultas públicas existentes para la evidencia contraria; no hay registro nuevo del coordinador en Deskops y el prompt de Scion no es señal consultable. Salidas: admitida, con el texto declarado sin evidencia contraria a las <hora de la consulta>, o lectura/handoff con su causa. Cubre la ruta ya en uso POST /api/desk/advance (el botón Avanzar de views/workflow/deskops/deskops-view.js): rechazo en el servidor antes de advance_task cuando falta la afirmación vigente, hay evidencia contraria o la consulta de evidencia falla, y estado y mensaje del botón; se conservan revision, gates y rechazos existentes y no se crea una operación nueva de lifecycle. La ausencia de evidencia contraria no prueba exclusividad, y con otro coordinador escritor la UI queda en lectura o handoff (P03). No crea servicio de identidad, autenticación ni coordinación distribuida, ni lock, ni CAS universal, ni un 409 donde el canal no ofrece precondición. No exige G_HUMAN_READ para desarrollar y probar el mecanismo; la habilitación real de los consumidores sigue requiriendo los gates humanos correspondientes y esto no permite usar escrituras en el producto.

## Aceptación

Pruebas en un store temporal. POST /api/desk/advance sin afirmación vigente, con evidencia contraria o con la consulta de evidencia fallida se rechaza en el servidor antes de invocar advance_task, y el botón Avanzar muestra su estado deshabilitado y el mensaje de la causa; con admisión, la ruta conserva revision, gates y rechazos existentes. Sin afirmación vigente la mutación queda deshabilitada y se ofrece handoff. Con evidencia contraria, o con la herramienta de evidencia ausente o con error, lectura o handoff con su causa y el buffer conservado. Con afirmación y sin evidencia contraria se admite sin afirmar exclusividad comprobada. Evidencia contraria tras escribir bloquea la siguiente escritura. Los consumidores WS19.1, WS19.2, WS21, WS25.1, WS25.2, WS26.1, WS26.2, WS28, WS39 y WS42 dependen de este nodo y lo usan, ninguno lo reimplementa. Acta P01 del delta. Este nodo es plan; no afirma que exista ni que esté implementado o aceptado.

## Dependencias

Tareas: WS12. Gates: G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS48/4ff520f32c0cad6e97634533938dc69007e84c9acbd2405f16d1d29ab28cb1de/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
