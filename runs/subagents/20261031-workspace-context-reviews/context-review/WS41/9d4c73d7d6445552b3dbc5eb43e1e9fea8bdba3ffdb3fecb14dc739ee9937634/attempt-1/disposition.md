# Disposición WS41, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Lectura segura entre dos stores de WS40 con aliases/roots autorizados, errores visibles (alias no autorizado, path escapado, store ausente), sin mutaciones cruzadas ni cambiar SLDB_STORE global, repo graph_ui, depende de WS13, WS11 y WS40: coincide.

**Ambigüedades.**

1. cómo comprobar «sin mutaciones cruzadas». Clase: `detalle de promoción`. caso de prueba (estado git o hash del store antes/después, ausencia de peticiones de escritura) dentro de una aceptación comprobable; lo fija el TaskDoc.
