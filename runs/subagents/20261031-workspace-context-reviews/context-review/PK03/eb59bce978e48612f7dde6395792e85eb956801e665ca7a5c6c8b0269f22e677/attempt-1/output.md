## REFORMULACION

- **Propósito:** PK03 agrupa la revisión del lector útil y el descubrimiento temprano, con aceptación humana inicial.
- **Resultado:** agrupación cerrada cuando cada hijo directo tenga `context_review` vigente o bloqueo externo con responsable registrado; no es producto entregado ni ejecución.
- **Repo:** `deskops` como agrupación; los hijos pertenecen a `graph_ui`.
- **Límites:** no ejecuta tareas, no autoriza trabajo ni añade aristas; no depende de edición, Changes ni Scion; no sustituye el acta humana de WS16.

## AMBIGUEDADES

1. **«acta WS16 con mediciones P08»**  
   P08 incluye abrir/buscar, guardar y arranque; WS16 dice «Mide aperturas y búsquedas; guardados no aplican hasta WS30». Obliga a inventar si la aceptación de PK03 exige medir guardado ≤3 s antes de WS30 o solo aperturas, búsquedas y arranque.

2. **«foco/historia/Code/grafo»**  
   PK03 enumera «grafo» en su aceptación, pero sus hijos directos no identifican qué hijo asume esa representación ni su aceptación. Obliga a inventar si queda cubierta por WS13, por una capacidad existente de Mindmap o por otro entregable.

## DRY-RUN

- **Lecturas previstas:** guía, brief, alcance, decisiones, cobertura y bloque PK03; sin ejecutar.
- **Cambios previstos:** ninguno de producto; solo disposición de revisión si el coordinador la registra.
- **Dependencias:** hijos WS13, WS14, WS15, WS16, WS40 y WS41; WS16 depende además de WS08/WS40/WS41 y WS13 de WS11. WS11/WS08 habilitan el conjunto.
- **Validaciones futuras:** `context_review.py status` comprobará hashes y `disposition.md`; WS16 producirá acta humana; la completitud sustantiva no se ejecuta aquí.

## FUTURO

WS11/WS08 producen contrato y flujos; WS40 genera el Taller; WS16 realiza la validación humana; el coordinador registra bloqueos externos. La revisión de cierre la determina el script y la disposición de cada hijo, no este nodo.
