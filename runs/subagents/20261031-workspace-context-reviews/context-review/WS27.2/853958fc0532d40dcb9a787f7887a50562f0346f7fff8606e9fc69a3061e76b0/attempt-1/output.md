## REFORMULACION
Propósito: definir un nodo de implementación que muestre, junto a una TaskDoc, la evidencia declarada, encontrada y verificada, abriendo su soporte cuando sea posible. Resultado: vista de evidencia en `frontends/mindmap/views/workspace/evidence/` con pruebas. Repo dueño: `graph_ui`. Límites: no crear modelo de comentarios; rutas de lectura según contrato WS11; depende de WS13 y WS12 y del gate pendiente G_UI_READ.

## AMBIGUEDADES
1. «declarada sin artefacto, artefacto no declarado y verificación fallida se muestran como estados distintos»: no se define cómo emparejar cada evidencia declarada con un artefacto encontrado. Obligaría a inventar la regla de identidad (ruta normalizada, hash, id u otra).
2. «verificada = resultado de `deskops closeout verify`»: no se especifica si el veredicto es por evidencia o por TaskDoc completa, ni cómo se asigna a cada evidencia. Obligaría a inventar agregación y mapeo.
3. «Evidencia junto a la TaskDoc»: no se indica cómo se selecciona la TaskDoc mostrada ni de qué contexto procede. Obligaría a inventar la fuente de selección.

## DRY-RUN
Lecturas: nodo WS27.2, aristas WS12/WS13/WS27, guía, brief, alcance, decisiones y cobertura. Cambios previstos: nueva vista de evidencia bajo el `output_scope` y tests; ningún cambio en nodos vecinos. Dependencias: WS13 y WS12; G_UI_READ pendiente, resuelto por WS11; rutas de lectura fijadas por contrato WS11. Validaciones futuras: pruebas de estados distintos, ausencia visible, apertura de Markdown dentro del workspace y declaración de no soportado fuera; aceptación del delta por graph_ui; preflight task-only en promoción. Sin ejecutar.

## FUTURO
WS11 produce la aceptación y las rutas de lectura; WS12 registra la capability exacta de `closeout verify` y los campos de TaskDoc; WS07/humano resuelven P01/P04 y designan responsables; el TaskDoc de promoción fija archivos, pills y textos; WS27.1 aporta el diff complementario.
