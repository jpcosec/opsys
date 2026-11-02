## Datos del supervisor (no verificados por mí)

- `tester-facts.log`: HEAD deskops `820b4d57`; graph_ui `134a665`; sldb `77bd6d00`; sha256 de `navegacion.md` `b3c763…`; cuatro checks con exit 0. No ejecuté nada.

## Lectura propia

| Objeto | Fuente | Evidencia real archivo:línea | Resultado |
|---|---|---|---|
| Identidad canónica `Model:name` | Propia | `UIs/graph_ui/frontends/mindmap/workspace_routes.py:118` | PASS |
| Resolución por `Model:name`, `Model/name`, nombre solo | Propia | `workspace_routes.py:251-269` | PASS |
| Nombre ambiguo → 400 | Propia | `workspace_routes.py:264-267`, `:299-300` | PASS |
| Guardia textual de identificador | Propia | `workspace_routes.py:134-135` (`'..' in ident`, prefijo `/`/`\`) | PASS |
| `path` en catálogo, nodo y contexto | Propia | `workspace_routes.py:125`, `:237`, `:209` | PASS |
| Fallback degradado y rutas fijas | Propia | `workspace_routes.py:271-352`; candidatos `:315-321`; lectura `:326` | PASS |
| Hash de campos y de archivo | Propia | `workspace_routes.py:173-198`, `read_bytes` `:196`; `document_serialization.py:24-32` | PASS |
| Nodos y aristas graph | Propia | `workspace_routes.py:387-393`, `:395-413`; `document_edge.py` sin campo `field` | PASS |
| Estados de Code | Propia | `workspace_routes.py:481-575` | PASS |
| Rutas seguras (contención, `.git`, gitignore, dir, tamaño, binario, encoding, URL) | Propia | `workspace_routes.py:501-518`, `:521-524`, `:460-479`, `:531-532`, `:536-537`, `:540-541`, `:543-549`, `:484-485` | PASS |
| `document_edges` reconstruye índice | Propia | `workspace_routes.py:356-359`; `document_edges.py:30`; `rebuild_edges.py:30-40` | PASS |
| `recover_links` sin rama de alias | Propia | `sldb/.../links/resolver.py:32-37` | PASS |
| `_store` de `views_routes` acepta store del cliente y escribe | Propia | `views_routes.py:29-33`, `:56-66` | PASS |
| `identity.py` sin contención | Propia | `deskops/identity.py:256-262` | PASS |
| graph_ui no consume `[[`/`recover_links` en workspace | Propia | grep en `frontends/mindmap`: solo `serve.py:10,241` y usos ajenos en notación/`contract.py` | PASS |
| No hay `focus` en el workspace | Propia | grep en `workspace_routes.py` y `views/workspace/` sin coincidencias; solo `selectedId` en `workspace-view.js:56` | PASS |
| Specs sin fila en `ui.md` pero vista existente | Propia | grep `Specs` en `auditoria/ui.md` sin coincidencias; `notation-view.js:356`; `registry.js:16` | PASS |
| 10 dependientes directos de WS11 | Propia | `dag.yaml` `depends_on` con WS11 en 728, 802, 846, 897, 938, 1175, 1218, 2282, 2677, 2718; WS15.1 depende de WS13 (1056-1058) | PASS |
| 18 nodos de `G_UI_READ` | Propia | `dag.yaml:173-191` | PASS |
| Productores citados en H-01..H-25 existen | Propia | ids en `dag.yaml`: 841, 892, 933, 1052, 1093, 1488, 1526, 1565, 974, 1887, 2011, 723, 1170, 2672, 2712 | PASS |
| Tabla C1-C4 | Propia | `workspace-view.js:219-226`, `:262`, `:419`, `:518`, `:537`; `workspace_routes.py:441-451` | PASS con salvedad: C4 es correspondencia de datos entrada→tarjeta, no foco seleccionable |
| §2.2 «ninguna ruta de graph_ui lee el archivo propio» | Propia | Contradicho: `workspace_routes.py:196` hace `read_bytes()` del archivo propio; `:326` hace `read_text()` en el fallback | FAIL |
| §4 «el único `read_text` del archivo del documento está dentro de la construcción del IR» | Propia | También leen el archivo `sldb/.../cli/serve/sections_routes.py:46` (IR/secciones) y `sldb/.../api/documents/document_serialization.py:20` (provenance) | FAIL |
| ¿Algún párrafo decide cambio de alcance? | Propia | 6.2 y 8.4 remiten a root; 9 detiene WS18 conforme a la TaskDoc | PASS |
| ¿Inventa alias, root o valor? | Propia | 3.2 no fija valores; H-10/H-11 quedan como hueco | PASS |

## No pude verificar

- Los commits `134a665`, `77bd6d00` y `c19c6c0d`: sin shell/git. El hecho del supervisor dice HEAD deskops `820b4d57`, distinto del `c19c6c0d` que declara el contrato.
- Comportamiento en runtime: reconstrucción de índices, `[[alias:ref]]`, CDN y `surface`.
- Que no exista un acta de recepción fuera de `UIs/graph_ui/runs/subagents/` (solo comprobé que no existe `workspace-documental-acceptance/`).
- Los checks y hashes del `tester-facts.log`: son dato del supervisor, no lectura mía.

RESULTADO: FAIL
