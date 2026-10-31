## REFORMULACION
- **Propósito:** publicar un manual documental básico cuyas instrucciones estén respaldadas por evidencia de validación/publicación, no por capacidades supuestas.
- **Resultado:** `docs/workspace-user-manual.md`, capturas en `docs/assets/workspace-user-manual/` y átomos vinculados en `desk/atoms/`.
- **Repo:** `deskops`.
- **Límites:** solo navegación, edición, captura, trabajo manual y revisión demostradas; Scion queda como capítulo propuesto hasta WS38; no atomizar Pxx pendientes; personalización/impacto no bloquean el manual básico.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
- **Lecturas previstas:** `dag.yaml#node:WS31`; `context-review-guide.md`; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`; `borradores/manual.md`; actas de WS30 y WS43; contratos de WS11/WS12 en `contratos/`; Pxx aceptadas; manual CLI existente.
- **Cambios previstos:** redactar/actualizar el manual y sus capturas; crear un átomo por Pxx aceptada y por contrato aplicable; enlazar átomos al documento.
- **Dependencias:** WS30 (acta y `G_HUMAN_MANUAL`), WS10 (índice/convención), WS43 (acta de publicación), contratos transitivos de WS11/WS12. `G_HUMAN_MANUAL` debe estar resuelto.
- **Validaciones futuras:** cada instrucción referencia acta WS30 o WS43; etiquetas disponible/propuesto/bloqueado; links y `atom->doc` verificables; ninguna Pxx pendiente atomizada; Scion marcado propuesto; capítulos de modelos/impacto marcados propuestos salvo comprobación de `G_HUMAN_MODEL`/WS29. No se ejecuta nada.

## FUTURO
- WS30 produce el acta humana y resuelve `G_HUMAN_MANUAL`.
- WS43 produce el acta de publicación y el commit de la versión publicada.
- WS11/WS12 producen los contratos que WS31 debe referenciar.
- WS38 añade después los capítulos verificados de delegación.
- WS39/WS29 aportan, si existen, evidencia para modelos/impacto; si no, se mantiene etiqueta propuesta.
- La promoción fijará archivos exactos, pills, átomos y evidencia; no corresponde a este nodo.
