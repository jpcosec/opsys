# Disposición WS45, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Verificar o completar en sldb la precondición de payload que WS12 fije (before-image `expected`/HTTP 409, token publicado, comparación pública), inventario con path/símbolo/commit, pruebas por operación y escritor, independiente de source_mode, depende de WS12: coincide. Resultado omite el recibo G_SLDB_WRITE, que sí figura en el dry-run.

**Ambigüedades.**

1. «código solo si al ejecutar falta capacidad, con tarea propia en sldb» (¿es WS45 esa tarea?). Clase: `detalle de promoción`. la frase y el output_scope (`src/sldb/...` solo si falta capacidad) acotan el código; a diferencia de WS20 («se convierte en esa tarea propia»), WS45 no lo declara. Cierra con el TaskDoc, sin riesgo de que el ejecutor invente código (ver promotion-notes.md).
2. «operación y escritor que el contrato WS12 alcance» (enumeración). Clase: `futuro asignado`. productor WS12: «WS12 define la representación de la precondición, las operaciones y los escritores alcanzados» y la representación la elige WS12 (ya no es hueco compartido); si falta, regla común de alcance.md.
