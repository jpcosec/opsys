# Disposición WS26.1, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Autoría desde candidato del drawer con evidencia declarada, dependencias y pills, sin editar status, repo graph_ui, depende de WS12 y WS22: coincide.

**Ambigüedades.**

1. «candidato queda autorado»: ¿crea tarea activa o enrutada?. Clase: `no es ambigüedad`. el scope separa el enrutamiento: en WS26.2 «Enrutar = añadir la tarea a la lista tasks del BoardDoc»; WS26.1 solo autora; «promotion: not_authorized» es metadato del nodo, no regla de la UI.
2. «Si una operación Git no tiene contrato o dueño… handoff» sin operación Git en el scope. Clase: `no es ambigüedad`. es una cláusula de respaldo condicional («queda en handoff explícito y se declara no disponible»); no obliga a commitear (consistente con P05, guardar no hace commit).
