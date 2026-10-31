## REFORMULACION
Propósito: añadir edición de campos con revisión esperada y conflicto visible. Resultado: guardar/recargar confirma dato real; una escritura obsoleta conserva el texto local y muestra conflicto; campos workflow-protected no editables por este canal. Repo: `graph_ui`, delta sobre workspace integrado `a1b2b22`, salida en `frontends/mindmap/views/workspace/fields/` y `tests/`. Límites: consumir endpoints del contrato WS12 sin cambiarlo; no duplicar `editing`; promoción no autorizada; mutaciones UI sujetas a `G_HUMAN_READ`, y a `G_UI_WRITE`/`G_WRITE_CONTRACT` por delta; pruebas API aisladas pueden avanzar.

## AMBIGUEDADES
1. «Mutación restringida a desk en modo manual exclusivo (P03); otros modos read-only hasta contrato». Obligaría a inventar qué es operativamente «modo manual exclusivo» —quién lo activa y cómo se detecta— y qué contrato/actor habilita los «otros modos». P03 solo fija lectura/handoff cuando hay otro coordinador escritor; no define ese modo ni nombra productor del contrato restante.

## DRY-RUN
Lecturas consideradas: nodo WS19.1, guía, brief, alcance, decisiones, cobertura y reconciliación suministrados; sin abrir otras fuentes. Cambios previstos: implementar edición de campos en la ruta indicada y sus tests; consumir endpoints WS12; no modificar contrato ni campos protegidos. Dependencias: WS12, gates `G_HUMAN_READ`/`G_UI_WRITE`/`G_WRITE_CONTRACT`, padre WS19, base `a1b2b22`, matriz WS06 transitiva. Validaciones futuras: guardar/recargar; CAS/409 con texto local conservado; conflicto visible; bloqueo de campos protegidos; restricción de modo; pruebas API aisladas; UI solo tras `G_HUMAN_READ`; recibos per_delta. Sin ejecutar.

## FUTURO
WS12 produce contrato/whitelist/endpoints y `G_WRITE_CONTRACT`. WS16 produce `G_HUMAN_READ`. El receptor P01 emite `G_UI_WRITE` por delta concreto. El TaskDoc de promoción fija archivos, pills, átomos y evidencia. WS19 cierra cuando cumplen WS19.1 y WS19.2; WS06 integra sin duplicar. La aceptación humana del delta no autoriza implementación, API ni Scion.
