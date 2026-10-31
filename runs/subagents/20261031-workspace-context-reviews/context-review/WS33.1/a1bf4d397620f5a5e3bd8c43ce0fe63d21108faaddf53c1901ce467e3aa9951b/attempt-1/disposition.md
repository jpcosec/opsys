# Disposición WS33.1, ronda 8

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. error_reviewer: Caso de borde de importación no cubierto por el scope; la falta de un dato se resuelve con la regla de hueco. alcance.md: «Si al llegar a un nodo falta un contrato, API, dato o permiso que debía producir una dependencia: detenerse, registrar el hueco con repo dueño y no crear sustituto».
2. error_reviewer: La duda se resuelve con la cadena real: WS33.1 → WS32 → WS12 → WS11; WS12 declara WS11 en `depends_on`. alcance.md: «Una dependencia transitiva cuenta como prerrequisito aunque no figure en `depends_on` directo».
