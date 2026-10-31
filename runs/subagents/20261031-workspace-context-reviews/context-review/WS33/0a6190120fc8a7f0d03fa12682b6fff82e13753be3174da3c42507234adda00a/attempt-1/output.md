REFORMULACION
WS33 es un agregado no ejecutable del repo `deskops`. Agrupa WS33.1 —vincular mensajes y resultados a un intento existente, con deduplicación y procedencia, sin tocar tablas Scion— y WS33.2 —registrar una decisión humana explícita (aprobar/pedir corrección) con actor, intento y tarea, mediante el contrato WS12—. Resultado: backend documental, independiente del editor UI. Límites: no ejecuta, no define UI, no sustituye tablas Scion; promoción no autorizada. Depende de WS32, WS11 y sus hijos; requiere `G_SCION`. La aceptación es agregada: se cierra con la aceptación de sus hijos.

AMBIGUEDADES
1. La dependencia WS11 no se refleja en alcance, salidas ni aceptación. Cita: «depends_on: - WS32 - WS11 - WS33.1 - WS33.2» y «se cumple cuando todos sus hijos cumplen su aceptación». Aunque `integration_mode` dice «matriz WS06 llega de forma transitiva por WS11/WS12», no fija qué salida de WS11 consume WS33 ni cómo se comprueba. Obliga a inventar si WS11 condiciona el cierre del agregado o si la arista sobra; según la guía, un agregado termina con sus hijos.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación y nodo/aristas de WS33. Cambios previstos: ninguno propio; el agregado no genera archivos ni ejecuta código. Dependencias: WS32, WS11, WS33.1, WS33.2 y `G_SCION`. Validaciones futuras: aceptación de ambos hijos y evidencia de `G_SCION`; no se ejecutan pruebas ni comandos.

FUTURO
WS44, con operador designado en WS07, produce la evidencia de `G_SCION`. WS33.1 y WS33.2 producen sus salidas; WS35 las consume. El TaskDoc de promoción fijará archivos, pills y evidencia; la promoción sigue requiriendo autorización humana.
