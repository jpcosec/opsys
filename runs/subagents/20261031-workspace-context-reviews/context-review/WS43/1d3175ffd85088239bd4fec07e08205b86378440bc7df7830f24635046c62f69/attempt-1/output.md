## REFORMULACION
**Propósito:** publicar en el deskops real la navegación documental validada en Taller (entradas/índices authored), sin tocar repos hermanos.
**Resultado:** `desk/README.md`; mapa de ecosistema/índices según P09 y WS11; átomos de acuerdos durables; acta y commit.
**Repo:** `deskops` (`output_base: deskops:repository_root/`).
**Límites:** no modificar repos hermanos ni imponer modelos; no publicar solo el ejemplo; cada proyecto adicional exige tarea de repo; preservar registry como inventario derivable; registrar conocimiento durable en átomos antes de docs.

## AMBIGUEDADES
1. **Dependencia no declarada.** «mapa de ecosistema/índices según P09 y WS11» cita WS11, pero `depends_on` solo incluye WS17 y WS30. Obliga a inventar si WS11 debe estar terminado, dónde están sus artefactos y qué hacer si faltan.
2. **Contrato y modelo indeterminados.** «P09 y contrato fijan ubicación/modelo opcional» no identifica qué contrato ni qué «modelo»; P09 sigue pendiente. Obliga a inventar formato, ubicación y contrato aplicable.
3. **Commit sin actor ni canal.** «acta … y commit» no define quién commitea, en qué rama ni con qué autoridad; P05 propone que guardar no commitea y el closeout es externo. Obliga a inventar la operación de commit.
4. **Repos conocidos no enumerados.** «Enlazar repos conocidos por identidad/origen y su entrada existente» no fija el conjunto ni qué constituye «proyecto adicional». Obliga a inventar el inventario a enlazar.

## DRY-RUN
- **Lecturas:** `dag.yaml` (WS43/WS17/WS30 y gates), `decisiones.md` (P09/P05), brief/alcance, cobertura UF01/UF03, artefactos WS17, acta WS30, inventario WS11, registry.
- **Cambios previstos:** `desk/README.md`; mapa/índices authored; átomos; `runs/subagents/workspace-documental-acceptance/publicacion/acta.md`; commit.
- **Dependencias:** WS17 y WS30 (G_HUMAN_MANUAL); G_PRODUCT (WS07); G_WRITE_CONTRACT (WS12); WS11 no declarada.
- **Validaciones futuras:** persona designada recorre Markdown/UI; links/roots verificables; registry derivable sin duplicar; ningún repo hermano modificado; acta y commit; cold preflight.

## FUTURO
WS07 resuelve P01/P09 y designa actor; WS30 produce G_HUMAN_MANUAL; WS12 produce G_WRITE_CONTRACT; WS11 entrega inventario/mapa; WS31 consume WS43; el humano acepta publicación y commit. La promoción exige paths, modelo/contrato, pills/átomos, evidencia y preflight.
