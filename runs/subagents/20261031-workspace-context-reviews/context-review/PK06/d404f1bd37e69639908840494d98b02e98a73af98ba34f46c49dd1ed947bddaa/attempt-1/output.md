## REFORMULACION
PK06 es un paquete de publicación, sin ejecución propia. Su propósito es convertir recorridos ya demostrados en documentación publicada y verificable: un manual básico versionado y las entradas/índices del desk real. El resultado esperado es `docs/workspace-user-manual.md` con instrucciones enlazadas a actas/versiones y límites, `desk/README.md` y mapa authored probados, y átomos que registren acuerdos durables y procedencia. Repo dueño: `deskops`. Límites: no implementa UI, no autoriza tareas ni añade aristas, no publica Scion/modelos/Changes no demostrados —quedan propuestos—, no modifica repos hermanos y no sustituye actas humanas ni contratos ausentes.

## AMBIGUEDADES
Ninguna. Las salidas de WS43 y WS31, sus dependencias externas (WS17, WS30, WS10) y los gates están definidos; los pendientes son gates intencionales o productos de otros nodos, no invenciones exigidas a PK06.

## DRY-RUN
Hipotéticamente, WS17 entrega plantillas `ejemplo/nav/` con paths/hashes y WS30 entrega acta humana con entradas/índices validados. Con ambos, se ejecutaría primero WS43: consume contrato `contratos/navegacion.md` de WS11, plantillas WS17 y acta WS30; aplica al deskops real las entradas validadas, escribe `desk/README.md`, mapa de ecosistema/índices, átomos enlazados y `runs/subagents/workspace-documental-acceptance/publicacion/acta.md`, registrando correspondencia paths/hashes y verificando roots/links contra el contrato. Después WS31: consume índice de WS10, acta WS30 y acta/publicación WS43; redacta `docs/workspace-user-manual.md`, assets y átomos, con cada instrucción remitida a acta/versión, etiquetas coherentes, capítulos no demostrados marcados propuestos y links/atom→doc verificados.

Integración: el acta WS43 debe permitir trazar las entradas WS17 validadas por WS30 hasta el mapa publicado; WS31 debe enlazar esa publicación y el acta manual, sin presentar como demostrado lo que siga propuesto. Validación esperada: ejecutor comprueba links resolubles, etiquetas y fuente declarada; tester independiente revisa antes del cierre. Si falta contrato, acta o correspondencia, se detiene y registra el hueco con repo dueño; un fallo del guion humano bloquea el gate.

## FUTURO
WS17, WS30 y WS10 producen sus artefactos; WS11/WS12 aportan contratos; el humano recorre y acepta mediante `G_HUMAN_MANUAL`; WS38 y WS29 deciden cuándo dejar de marcar Scion/modelos como propuestos.
