REFORMULACION
Encargo del nodo WS19.1: implementar en graph_ui la edición de campos con conflicto visible, reutilizando editores y endpoints del contrato WS12 sin cambiarlo. Resultado: guardado por `changes[]` con `expected`, texto local conservado ante 409 y campos workflow-protegidos no editables; repo graph_ui, scope `frontends/mindmap/views/workspace/fields/` y `tests/`. Límites: depende de WS12, WS47 y WS48; no habilita documentos con contenido no declarado antes de WS47; no crea API ni contrato; gates G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT pendientes; promoción no autorizada.

AMBIGUEDADES
1. «Este parche cubre los ocho hallazgos y esas decisiones»: no se enumeran los ocho hallazgos ni las decisiones A–E; obliga a inventarlos, pues `review-source.md` no está incluido.
2. «Documentos con contenido no declarado no son editables por este canal hasta que WS47 pruebe la guarda de contenido»: no dice cómo los detecta WS19.1 antes de WS47; obliga a inventar la detección (¿deshabilitar, replicar 6.7 en cliente, esperar?).
3. «Delta sobre workspace integrado a1b2b22 de edición»: no describe esa base ni si U02 remoto entra en el alcance; obliga a inventar el punto de partida y el alcance.

DRY-RUN
Un ejecutor futuro leería el contrato §3–§6, `GU/persistence.py`, `sldb_adapter.py`, `serve.py`, la vista de campos y los tests citados. Cambios previstos: editor que envía `expected`; filtro de campos protegidos antes de `/api/save`; llamada a la admisión WS48 antes de escribir; manejo de 409 conservando el buffer. Dependencias: WS12 aprobado, WS47, WS48 y G_PAYLOAD_PRECONDITION (WS45). Validaciones futuras en store temporal: 409 sin pérdida, protegidos rechazados, sin F1 deshabilitado/handoff, contenido no declarado no editable; fallo parcial 500 con `completed`. Nada de esto se ejecuta ahora.

FUTURO
WS12: revisión root y G_WRITE_CONTRACT. WS45: produce G_PAYLOAD_PRECONDITION. WS47: declara pérdidas detectadas/no detectadas. WS48: fija F1 y entrega admisión. P01: acta G_UI_WRITE. Humano: G_HUMAN_READ y autorización de promoción. Root: aceptar la propuesta WS46/47/48.
