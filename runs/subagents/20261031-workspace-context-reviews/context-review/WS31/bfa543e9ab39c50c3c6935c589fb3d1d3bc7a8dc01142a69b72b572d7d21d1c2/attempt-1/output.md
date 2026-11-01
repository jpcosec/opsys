## REFORMULACION

El nodo encarga publicar en deskops un manual documental básico ya probado: convertir el índice y convención de WS10 en `docs/workspace-user-manual.md`, con assets y átomos vinculados, cubriendo navegación, edición, captura, trabajo manual y revisión demostradas. El resultado es un manual publicado y trazable a actas/contratos, con Scion solo como capítulo propuesto. Límites: no promete permisos ni aceptación técnica inexistente, no bloquea por personalización/impacto, no implementa UI ni modifica otros repos; la promoción sigue no autorizada.

## AMBIGUEDADES

1. «un átomo por cada decisión Pxx humana o técnica ya registrada y vigente en decisiones.md y por cada contrato en contratos/» frente a WS43: «los acuerdos durables aplicados al mapa [...] quedan en átomos enlazados desde él. [...] Reutilizar átomo equivalente antes de crear». Obligaría a inventar si WS31 crea átomos nuevos, reutiliza los de WS43 o solo los enlaza; riesgo de duplicados u omisión.

2. «Cada instrucción remite al acta de WS30 o al acta de publicación de WS43 de la versión publicada». No queda claro si «versión publicada» designa el commit del desk publicado, una versión del manual o el propio acta de WS43. Obligaría a inventar el identificador que debe citarse en cada instrucción.

3. «incorporar el índice de borradores/manual.md, capturas y limitaciones» frente a la aceptación, que solo exige «etiquetas, links y atom->doc verificados». Obligaría a decidir si las capturas son obligatorias, de qué build proceden y cómo se validan, pese a existir `docs/assets/workspace-user-manual/`.

## DRY-RUN

Leería `task-ws31.md` tras promoción, `borradores/manual.md`, actas de WS30 y WS43 con sus commits, `decisiones.md`, `contratos/navegacion.md`, `contratos/operaciones.md`, manual CLI y átomos existentes.

Cambios previstos: redactar/actualizar `docs/workspace-user-manual.md`, depositar capturas en `docs/assets/workspace-user-manual/` y crear o enlazar átomos en `desk/atoms/`.

Consumiría `G_HUMAN_MANUAL`, el acta de WS30 y la publicación/acta de WS43; los contratos de WS11/WS12 llegan transitivamente. Errores esperados: acta o contrato ausente, link irresoluble, etiqueta sin acta/commit o átomo duplicado; ante ello, detenerse y registrar el hueco con repo dueño, sin sustituirlo. Validación: el executor comprueba links, etiquetas y atom→doc; un Tester independiente revisa antes del cierre. El nodo no produce gate.

## FUTURO

WS38 añadirá capítulos verificados de delegación y reutilizará o actualizará átomos de WS31. WS39/WS29 pueden aportar evidencia para capítulos opcionales; sin ella quedan propuestos. WS30 y WS43 producen actas y gates. La aceptación de deltas y cualquier cambio de alcance corresponden a un humano.
