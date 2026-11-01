# Disposición WS26.2, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Enrutar añadiendo la tarea al BoardDoc por operación pública, capa lista separada de ejecución/dependencias/solape, no implementar promoción nueva, repo graph_ui, depende de WS12, WS22 y WS26.1: coincide.

**Ambigüedades.**

1. «glob/no-resolución dudosa implica no comprobado y revisión supervisor antes de marcar lista». Clase: `no es ambigüedad`. la conducta del nodo está definida: mostrar «no comprobado» y no marcar lista («no heurística optimista»); la revisión del supervisor es un paso externo al nodo.
2. «ritual vigente» sin ruta. Clase: `futuro asignado`. productor WS12: «rutas normalizadas/expansión de files que documente contrato WS12 y ritual vigente»; si falta, regla común de alcance.md (detenerse y registrar el hueco).
