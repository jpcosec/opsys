# Comparación del Supervisor — WS11, aceptada para despacho

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Leí preflight y cold completos. Reproducen objetivo, secciones y límites. Lo que marcan queda fijado aquí; prevalece sobre la TaskDoc donde la precisa.

- **Corrección de la TaskDoc:** dice «trece nodos»; son 10 dependientes directos: WS12, WS13, WS13.1, WS13.2, WS13.3, WS17, WS18, WS33, WS40, WS41. Lista de `dag.yaml`.
- Aliases y roots: no inventar valores. Fijar el mecanismo con lo real: manifiesto WS40 para el corpus; registry para el desk real, si la evidencia lo sostiene. Lo que falte es hueco.
- Rutas seguras: el criterio sale del código existente, citado (por ejemplo los límites de `_inspect_file_reference`). Lo no cubierto es hueco.
- Mapa de deltas: IDs = nodos con `owner_repo: graph_ui` que declaran `G_UI_READ`, más los de escritura que el contrato alcance solo como remisión a WS12. Nombres de gate, los de `dag.yaml`. Leerlos ahí.
- Compromiso = aceptación o scope de un nodo del DAG, o fila de `user-flows.md` o `vistas.md` que lo exija.
- Cambio de alcance: el Executor no lo decide. Registra hueco con productor, o «requiere cambio de alcance» para root.
- `G_SPEC_VIEW`: gate de `dag.yaml`; leer su definición.
- `frontends/workspace/`: se puede citar solo como no adoptado, nunca como base.
- Tester, checks, commits y closeout: Supervisor.
