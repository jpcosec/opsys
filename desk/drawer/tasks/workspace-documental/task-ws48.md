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

Productor común de la evidencia de modo manual exclusivo (T-P03.1, HO-03; contrato WS12, secciones 5 y 5.9), previo a toda mutación habilitada en la UI y no contenido en WS19.1, para que ack y captura no dependan de WS19.1. Un único punto de admisión que toda ruta de escritura consulta antes de invocar su canal, con una afirmación vigente suministrada fuera de la petición (configuración confiable del operador, sin valores reales en el repo) y la consulta de la evidencia contraria disponible. Salidas, admitida con el texto declarado sin evidencia contraria a una hora, o lectura/handoff con su causa. La ausencia de evidencia contraria no prueba exclusividad, y con otro coordinador escritor la UI queda en lectura o handoff (P03). No crea servicio de identidad, autenticación ni coordinación distribuida, ni lock, ni CAS universal, ni un 409 donde el canal no ofrece precondición.

## Aceptación

Pruebas en un store temporal. Sin afirmación vigente la mutación queda deshabilitada y se ofrece handoff. Con evidencia contraria, o con la herramienta de evidencia ausente o con error, lectura o handoff con su causa y el buffer conservado. Con afirmación y sin evidencia contraria se admite sin afirmar exclusividad comprobada. Evidencia contraria tras escribir bloquea la siguiente escritura. Los consumidores WS19.1, WS19.2, WS21, WS25.1, WS25.2, WS26.1, WS26.2, WS28, WS39 y WS42 dependen de este nodo y lo usan, ninguno lo reimplementa. Acta P01 del delta. Este nodo es plan; no afirma que exista ni que esté implementado o aceptado.

## Dependencias

Tareas: WS12. Gates: G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; no ejecutar. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
