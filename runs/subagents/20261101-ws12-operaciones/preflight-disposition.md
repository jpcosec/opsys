# Comparación del Supervisor — WS12, aceptada para despacho

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Leí preflight y cold completos. Reproducen objetivo, secciones y límites. Lo que marcan queda fijado aquí; prevalece sobre la TaskDoc donde la precisa.

- **«Última parte» de la autorización:** desde «Tras ese cierre queda autorizada SOLO WS12» hasta el final de `review-source.md`.
- **Commits observados:** deskops en el HEAD del despacho, sldb `77bd6d00`, graph_ui `134a665`, spec2viz `10df4f0`. Si uno se mueve, se declara.
- **Comandos de diagnóstico:** el conjunto sale de `cli/registry.py` de deskops (`mutates`), de las auditorías y de la adenda de `promotion-notes.md` sobre `atoms validate` y `stores check`. Se clasifica por efectos, no por nombre.
- **Criterio de la precondición:** los escritores y operaciones reales, con evidencia. Si la evidencia no basta para elegir, se dice y queda como hueco de WS45, sin inventar.
- **IDs de gates:** `scope_nodes` de cada gate en `dag.yaml`. Leerlos ahí.
- **Ramal E:** los deltas son WS34.1 y WS34.2. La sección fija política, clasificación, actor y momento. No fija umbral numérico.
- **«Prueba real» y «prueba existente»:** prueba en `tests/` del repo dueño, citada por ruta y nombre, sin ejecutar. Si no la hay, «sin prueba» y hueco. Lectura de código se rotula como lectura.
- **G_WRITE_POLICY:** `state: satisfied` en `dag.yaml`, resuelto por WS07. No se registra de nuevo.
- **Staleness, Tester, commits y registros:** Supervisor. `context_review.py status`.
