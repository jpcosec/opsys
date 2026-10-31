# Disposición WS33.1, ronda 2

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. corregido con ajuste del revisor: WS33.1.scope -> Clave de deduplicación: Hub + proyecto + id de mensaje. Los resultados se identifican por intento y por el identificador que exponga la fuente, a comprobar en W
2. corregido: WS33.1.scope -> Solo se vinculan mensajes y resultados con referencia a un id de intento existente; un mensaje con varios intentos o sin intento resoluble no se vincula y regis
3. corregido: WS33.1.acceptance -> Con contrato público real, una importación repetida (mismo Hub/proyecto y conversación, con checkpoint) no duplica mensajes ni resultados ni atribuye una conver
4. corregido: WS33.1.depends_on (WS11 llega de forma transitiva por WS32 → WS12 → WS11 y el scope no consume navegación ni identidad documental; la arista directa no aporta requisito y confunde al ejecutor. Mantiene la regla de alcance.md sobre dependencias transitivas.)
