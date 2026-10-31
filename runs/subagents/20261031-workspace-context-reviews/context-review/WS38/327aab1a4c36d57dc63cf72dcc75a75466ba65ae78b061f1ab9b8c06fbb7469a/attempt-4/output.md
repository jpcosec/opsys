## REFORMULACION

**Propósito:** añadir al manual la operación de delegación y la revisión trazable demostradas en WS37, sin ampliar capacidades.
**Resultado:** capítulos publicados en `docs/workspace-user-manual.md` y átomos vinculados en `desk/atoms/`.
**Repo dueño:** `deskops`.
**Límites:** solo lo que conste en el acta de WS37 y en operaciones reales; deben documentarse los fallos allí registrados y advertir que operar requiere `G_EXEC`. No autoriza ejecución ni promoción; el nodo es candidato.

## AMBIGUEDADES

Ninguna. El alcance, la fuente de verdad (acta de WS37) y la aceptación son comprobables. Los átomos y archivos exactos quedan para la promoción, y la ausencia de acta o de contrato se resuelve por las reglas comunes de `alcance.md`, no inventando contenido.

## DRY-RUN

- **Lecturas previstas:** guía de revisión; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`; `borradores/manual.md`; nodo WS38, vecinos WS37/WS31 y gates `G_HUMAN_DELEGATE`/`G_EXEC` en `dag.yaml`.
- **Cambios previstos:** capítulo de delegación en `docs/workspace-user-manual.md`; átomos vinculados en `desk/atoms/`.
- **Dependencias:** acta de WS37 en `graph_ui:runs/subagents/workspace-documental-acceptance/delegacion/acta.md`; manual básico publicado por WS31; `G_HUMAN_DELEGATE` satisfecho por WS37.
- **Validaciones futuras:** cada paso remite al acta y a operaciones reales; fallos registrados documentados; mención explícita de `G_EXEC`; etiquetas, enlaces y relación átomo→documento verificados.

## FUTURO

- WS37 produce el acta y resuelve `G_HUMAN_DELEGATE`; una persona aprueba la delegación.
- WS31 publica el manual básico que WS38 extiende.
- La promoción fija archivos, átomos, pills y evidencia exactos.
- Un humano autoriza o rechaza la promoción; este revisor no ejecuta ni aprueba.
