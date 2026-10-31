# Disposición WS32.1, ronda 2

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. corregido con ajuste del revisor: WS32.1.scope -> dispatch intent (intención registrada) y confirmed (Scion aceptó) como hechos separados del RunDoc; ambos se registran en el registro por intento que WS32.2 vue
2. corregido: WS32.1.acceptance -> cambios de RunDoc por el flujo SLDB de modelos (registro y edición de documento trackeado con CLI sldb), no edición ad hoc.
3. corregido: WS32.1.acceptance -> Dos intentos del mismo agente y un dispatch fallido (rechazo o timeout de la API) conservan identidades distintas, evidenciadas por ids de intento propios;
