## REFORMULACION

WS33 es un nodo agregado de planificación: agrupa la vinculación de mensajes, resultados y decisiones humanas asociadas a intentos. Su resultado no es ejecutable de forma aislada; se cumple cuando WS33.1 y WS33.2 cumplen su aceptación. El repo dueño es `deskops`. Límites: backend documental, independiente del editor UI; no autoriza promoción ni implementación; no define por sí mismo API Scion, dispatch/reply ni escritura fuera del contrato aplicable.

## AMBIGUEDADES

ninguna

No hay frase que obligue al ejecutor de WS33 a inventar un resultado, aceptación, repo, actor o dependencia: el nodo declara su carácter agregado, sus hijos, su repo y su aceptación por agregación.

## DRY-RUN

- Lecturas: nodo WS33 y guía de revisión; no se lee el TaskDoc ni fuentes externas.
- Cambios previstos: ninguno; un `aggregate` no se ejecuta ni produce archivos propios.
- Dependencias: WS32, WS11, WS33.1, WS33.2; gates `G_SCION` y `G_WRITE_CONTRACT`.
- Validaciones futuras: aceptación de WS33.1 y WS33.2, recibos de gates por delta y preflight de promoción antes de cualquier autorización.

## FUTURO

WS33.1 y WS33.2 producen las salidas concretas del agregado. WS12 produce el contrato técnico de operaciones y WS44 la evidencia de Scion; un humano autoriza la promoción y el preflight de la tarea. WS34/WS35 consumen el resultado cuando sus propias dependencias y gates estén satisfechos. Nada de esto se ejecuta aquí.
