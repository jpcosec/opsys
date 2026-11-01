# Disposición WS39, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Integrar inspección/edición de modelos existentes desde el panel Context de WS13, UF09 en store temporal, acta humana con participante P08 y G_HUMAN_MODEL antes de marcar disponible, repo graph_ui, depende de WS12 y WS13: coincide.

**Ambigüedades.**

1. hallazgo propio: el panel Context vive en `node/workspace-view.js`, que no está en `output_scope` (`shell/dialogs.js; views/models/; tests/; runs/…`); el revisor declaró «Ninguna». Clase: `detalle de promoción`. el scope delega «ruta/selector exacto se fija en TaskDoc»; es la tensión más cercana a un defecto del lote: el TaskDoc debe añadir ese archivo al alcance o declarar el enganche por `shell/dialogs.js` (ver promotion-notes.md).
