# Decisiones registradas

| Id | Decisión | Actor | Fuente | Fecha |
|---|---|---|---|---|
| DU1 | El producto es la UI de deskops, no un explorador del store; el visor KIMUN queda como vista secundaria de inspección. | Dueño | "¿Entiendes que el producto no es en realidad kimun si no que es la UI de deskops?" | 2026-11-04 |
| DU2 | El lenguaje visual es el de las pantallas de Stitch "Software Factory Knowledge Hub"; el design system es el de graph_ui (`DESIGN.md`), ya aplicado en Stitch. | Dueño | "si bien lo que había está técnicamente bien, no entiende el verdadero lenguaje visual que necesito… en el stitch sí se entiende"; elección de unificar hacia graph_ui | 2026-11-04 |
| DU3 | Escribir el plan y ejecutarlo. | Dueño | "si y más importante aún ejecútalo" | 2026-11-04 |
| DU4 | La lógica de qué se muestra vive en deskops (vista de datos con CLI y contrato); graph_ui es un cliente que la sirve por HTTP en loopback. deskops no gana servidor HTTP. | Asistente, conforme al plan de la fábrica del 2026-10-30 (E3: "deskops es la verdad, graph_ui solo muestra") | factory-local-first | 2026-11-04 |
| DU5 | Un elemento sin fuente real no se dibuja. Nada de datos de ejemplo, contadores inventados ni estados simulados. | Asistente, conforme a `DESIGN.md` de graph_ui ("Don't introduce mock, stub, or fabricated data") y al feedback del dueño sobre densidad | DESIGN.md; reader-density | 2026-11-04 |
| DU6 | Revisión en frío con tope: una ronda a nivel de plan y una de preflight por nodo al promover. | Dueño (tope de rondas, "8 rondas igual es excesivo") | cold-review-rounds-cap | 2026-11-04 |
