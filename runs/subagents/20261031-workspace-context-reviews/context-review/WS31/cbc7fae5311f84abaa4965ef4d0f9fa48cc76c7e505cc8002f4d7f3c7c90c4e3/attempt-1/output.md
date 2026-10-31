## REFORMULACION

**Propósito:** publicar el manual documental básico probado, integrando navegación, edición, captura, trabajo manual y revisión ya demostrados. **Resultado:** `docs/workspace-user-manual.md`, sus capturas en `docs/assets/workspace-user-manual/` y átomos vinculados en `desk/atoms/`. **Repo dueño:** `deskops`. **Límites:** depende de WS30, WS10 y WS43; requiere `G_HUMAN_MANUAL`; Scion solo como capítulo propuesto hasta WS38; personalización e impacto no bloquean el manual básico; no se atomizan Pxx pendientes; no se ejecuta nada.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** guía de revisión, `dag.yaml#node:WS31` y vecinos; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/manual.md`; contratos de WS11/WS12; actas de WS30/WS43; átomos existentes y manual actual en `deskops`.

**Cambios previstos:** redactar/actualizar el manual, incorporar capturas reales y crear/vincular átomos por Pxx aceptadas y contratos aplicables.

**Dependencias:** WS30 aporta acta y satisface `G_HUMAN_MANUAL`; WS10 aporta índice y convención; WS43 aporta publicación real y acta; WS11/WS12 aportan contratos. Si falta un contrato o acta, aplica la regla común: detenerse y registrar el hueco.

**Validaciones futuras:** cada instrucción remite a acta de WS30 o WS43; etiquetas disponible/propuesto/bloqueado; links y `atom->doc` verificables; un átomo por Pxx aceptada y por contrato; ninguna Pxx pendiente atomizada; Scion marcado propuesto; capítulos de personalización/impacto marcados propuestos o respaldados por `G_HUMAN_MODEL`/WS29.

## FUTURO

WS30 produce el acta humana y resuelve `G_HUMAN_MANUAL`. WS43 publica el mapa del desk real y su acta. WS11/WS12 producen los contratos. WS38 añadirá los capítulos verificados de delegación. WS39 y WS29 determinan si personalización e impacto pueden dejar de ser propuestos. El humano resuelve las Pxx. La promoción fijará archivos, pills y evidencia en el TaskDoc.
