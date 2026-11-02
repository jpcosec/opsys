# Handoff WS11

Contrato: `desk/drawer/plans/workspace-documental/contratos/navegacion.md`, sha256 `ca537c71d585a86032a1bf3817705f00af4904139e50534f0f5b70416b3597df`. Sigue en estado «borrador» por §0; cambiarlo es de root.

Decisiones de alcance abiertas para root:
1. WS13.1 promete foco Code/texto/graph; soportado solo C1-C4. Huecos H-03b, H-05b «candidato». Retirarlo exige cambio de alcance.
2. WS41, enlaces de texto entre desks: componer `parse_links` + `doc_status` en graph_ui, o ampliar a sldb. Sintaxis no fijada (H-16).
3. WS18 detenida: falta selección mínima de ViewDoc.
4. Aliases del desk real sin nodo productor (H-11).

Hallazgo sobre vistas.md: la vista Specs existe (`views/specs/notation/notation-view.js:356`) y `ui.md` no tiene fila. Matiza F18a. No edité vistas.md.
Sin productor en el DAG: H-14 en store propio, H-16.
No se tocó ningún repo hermano. WS12 y UI no activados.
