## REFORMULACION

**Propósito:** convertir WS27.2 en un encargo ejecutable: mostrar junto a la TaskDoc la evidencia declarada, encontrada y verificada, con sus estados diferenciados y apertura de soporte.

**Resultado:** UI de evidencia en `frontends/mindmap/views/workspace/evidence/`, sin modelo de comentarios nuevo; tests incluidos.

**Repo:** graph_ui (`output_base: graph_ui:repository_root/`).

**Límites:** depende de WS13 (lector) y WS12 (contrato); requiere G_UI_READ por delta. No inferir tipo por extensión en renderer; verificada = resultado de `deskops closeout verify`, no prueba independiente; artefacto fuera del workspace → ruta y “no soportado”; promoción no autorizada.

## AMBIGUEDADES

1. «gates/summary se muestran según reporte real». No se define qué son “gates” ni “summary”, ni de qué reporte salen; la aceptación solo exige declarada/encontrada/verificada. Obliga a inventar contenido y forma, y deja esa parte del scope sin aceptación comprobable.

2. «resultado del gate de la TaskDoc/tipo» frente a «verificada = resultado de `deskops closeout verify`». No queda fijada la granularidad: ¿un estado por TaskDoc, por tipo de evidencia o por evidencia individual? Obliga a inventar cómo mapear una salida única del comando a varias filas.

3. «una evidencia ausente se ve como ausente» frente a «declarada sin artefacto […] estados distintos». “Ausente” puede ser el vacío sin evidencia o la declarada cuyo archivo no resuelve. Obliga a inventar si son uno o dos estados.

4. «Reporte ausente/fallo de comando es no verificable con error» frente a «verificación fallida». No se aclara si “no verificable” es un estado propio o se colapsa con “fallida”. Obliga a inventar cuántos estados no verificados mostrar.

## DRY-RUN

**Lecturas:** nodo WS27.2 y aristas WS13/WS12; contratos WS11/WS12; `task-ws27-2.md`; modelos TaskDoc y `closeout_evidence`; salida de `deskops closeout verify`.

**Cambios previstos:** componentes de evidencia y estados, apertura vía lector, tests de estados y soportes.

**Dependencias:** WS13 (lector/rutas), WS12 (contrato), acta G_UI_READ del delta.

**Validaciones futuras:** evidencia ausente, declarada sin artefacto, artefacto no declarado, verificación fallida, comando/reporte ausente, apertura Markdown y caso no soportado.

## FUTURO

WS12 debe publicar la correspondencia por tipo de evidencia y la salida pública de `closeout verify`; si falta, el nodo se detiene y registra el hueco según alcance.md. P01 emite el acta G_UI_READ del delta. El TaskDoc de promoción fija archivos, textos y escenarios. WS13 entrega lector y rutas de lectura.
