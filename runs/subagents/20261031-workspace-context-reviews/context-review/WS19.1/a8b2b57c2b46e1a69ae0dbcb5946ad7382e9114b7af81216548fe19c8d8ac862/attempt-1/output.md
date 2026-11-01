## REFORMULACION

Propósito: que el workspace integrado de graph_ui permita editar campos reutilizando editores y API existentes, con precondición de escritura y conflicto visible. Resultado: guardar/recargar confirma dato real; escritura obsoleta se rechaza sin perder el texto local; campos protegidos por workflow no editables por este canal; endpoints del contrato WS12 consumidos sin modificar contrato. Repo dueño: graph_ui (`frontends/mindmap/views/workspace/fields/`, `tests/`). Límites: delta sobre base a1b2b22; mutación solo en desk con modo manual exclusivo; otros modos read-only; sin raw-source, sin CAS nuevo, sin cambios de contrato, sin alta/baja de relaciones (alcance del agregado WS19).

## AMBIGUEDADES

1. «Mutación restringida a desk en modo manual exclusivo (P03); otros modos read-only hasta contrato». El input no define qué es un «modo», cuáles existen ni cómo el ejecutor detecta que hay otro coordinador escribiendo. Obligaría a inventar un mecanismo de detección y un catálogo de modos que P03/WS12 no enumeran; «hasta contrato» mitiga, pero la aceptación ya exige distinguir modos para probar la restricción.

## DRY-RUN

Lecturas previstas: nodo WS19.1, contrato WS12 (representación de precondición, whitelist y campos protegidos), `reconciliacion.md` (base a1b2b22, ticket de edición draft en serie), `alcance.md` (reglas de contrato ausente), guía y brief. Cambios previstos: nuevos archivos bajo `views/workspace/fields/`, consumo de endpoints WS12 sin tocar contrato, tests de guardado/conflicto/protección. Dependencias: WS12 (contrato), WS45 vía G_PAYLOAD_PRECONDITION, G_HUMAN_READ (solo habilita uso de mutaciones en UI), G_UI_WRITE y G_WRITE_CONTRACT por delta, ticket `editing` en serie sin duplicar. Validaciones futuras: guardar/recargar dato real, rechazo de escritura obsoleta conservando texto local, campos protegidos no editables, pruebas aisladas de API antes del acta humana. Nada se ejecuta.

## FUTURO

WS12 debe publicar representación de precondición, whitelist por campo/operación y campos protegidos; WS45 aportará evidencia de G_PAYLOAD_PRECONDITION en sldb; el receptor P01 emitirá acta G_UI_WRITE por delta; WS16 emitirá G_HUMAN_READ; el TaskDoc de promoción fijará archivos y textos; WS19.2 cubrirá relaciones.
