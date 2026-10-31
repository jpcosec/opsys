REFORMULACION  
Propósito: agrupar la publicación básica del workspace documental: manual versionado y entradas/mapa del desk real, solo sobre recorridos ya demostrados. Resultado sustantivo: un paquete integrado por `docs/workspace-user-manual.md` con capturas, límites y referencias a actas/versiones; `desk/README.md` y mapa/índices authored según P09/WS11; átomos de decisiones y contratos con provenance atom→doc; actas de validación y publicación. Repo dueño: `deskops`; WS30 valida en `graph_ui`. Límites: PK06 no ejecuta ni autoriza tareas, no añade aristas, no promete Scion/modelos/Changes, mantiene como propuesto lo no demostrado y no sustituye gates humanos ni permisos. La publicación real no puede ser solo el ejemplo.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Lecturas hipotéticas: `dag.yaml`, WS31/WS43, sus dependencias WS10/WS17/WS30, brief/alcance/decisiones/manual/cobertura y contratos WS11/WS12. Orden: WS17 produce plantillas `ejemplo/nav/`; WS30 produce acta humana con paths/hashes; WS10 precisa índice. Con eso, el hijo WS43 publica el desk real: `desk/README.md`, mapa/índices, átomos y acta de publicación. Después, el hijo WS31 consume WS10, WS30 y WS43 y publica el manual versionado, assets y átomos vinculados. Dependencias/gates: `G_HUMAN_MANUAL` para WS31/WS43; `G_PRODUCT` y `G_WRITE_CONTRACT` para WS43; WS30 aporta validación humana. Validaciones futuras: links/roots verificables, referencias a acta/versión, atom→doc con fuente, etiquetas disponible/propuesto/bloqueado, mapa real distinto del ejemplo y ausencia de escritura en repos hermanos. Prueba integrada: el participante P08 recorre Markdown/UI real; se trazan actas WS30/WS43; Tester independiente verifica WS31. No ejecutar.

FUTURO  
WS17 entrega entradas/índices; WS30 decide y registra la validación humana; WS43 produce publicación real, acta y commit; WS31 produce manual y átomos. Humanos satisfacen `G_HUMAN_MANUAL`, `G_PRODUCT` y `G_WRITE_CONTRACT` y aceptan deltas. WS38 y WS29 aportan Scion/Changes solo si se demuestran.
