# Disposición WS36, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. UI que invoca solo el adaptador WS34, registra decisiones con WS33.2 y muestra actor y evidencia, error visible si faltan API/permisos, sin autoaprobación, repo graph_ui, depende de WS34 y WS35: coincide.

**Ambigüedades.**

1. WS33.2 no figura en depends_on (solo en review_context_nodes). Clase: `no es ambigüedad`. WS36 depende de WS34 y WS35; WS34 y WS35 dependen del agregado WS33 y la guía dice que un aggregate «termina cuando terminan sus hijos»; el edge de WS33.2 del input trae parent_id: WS33. Conviene que el TaskDoc nombre WS33.2 explícito (ver promotion-notes.md).
