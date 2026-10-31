REFORMULACION
Propósito: nodo agregado WS33 que reúne «Referencias Hub/proyecto/conversación/mensaje/intento y decisión humana explícita (WS33.2); dedup y procedencia». Resultado: agregado no ejecutable; se cumple cuando WS33.1 y WS33.2 cumplen su aceptación. Repo: deskops. Límites: backend documental, independiente del editor UI; no toca tablas Scion; depende de WS32/WS11 y de sus hijos; G_SCION y G_WRITE_CONTRACT pendientes son intencionales.

AMBIGUEDADES
Ninguna. La aceptación remite expresamente a las aceptaciones de WS33.1/WS33.2 y el alcance, repo y límites están delimitados. No hay frase que obligue al ejecutor de WS33 a inventar un resultado propio.

DRY-RUN
Lecturas: nodo WS33, hijos WS33.1/WS33.2, gates y guía. Cambios previstos: ninguno; un agregado no se ejecuta ni produce artefactos propios. Dependencias: WS32, WS11 y los hijos; requires G_SCION/G_WRITE_CONTRACT. Validaciones futuras: aceptación de WS33.1 —importación repetida sin duplicar mensajes/resultados y huecos de procedencia— y de WS33.2 —decisión con actor, intento, tarea y resultado aprobar/pedir corrección—; al cumplirse ambas, WS33 queda cumplido para sus dependientes.

FUTURO
WS44 debe producir la evidencia de G_SCION; WS12, el contrato G_WRITE_CONTRACT por delta; WS32/WS32.1/WS32.2, la identidad de intento. La designación del operador Scion y la recepción técnica corresponden a actores humanos. WS33.1/WS33.2 ejecutan y aportan sus salidas; WS34/WS35 consumen WS33 cuando sus propios gates lo permitan.
