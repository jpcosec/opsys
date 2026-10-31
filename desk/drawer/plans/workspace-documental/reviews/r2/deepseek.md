# R2 — Revisión de seguimiento (deepseek)

Comparación con mi dictamen R1 y con los archivos actuales. No usé dictámenes de pares ni `reviews/r1/`.

**Veredicto: REQUIERE CORRECCIONES.**

El plan ya es autosuficiente en intención, separa autoridad documental/workflow y modela gates externos y humanos. Quedan una contradicción de gate y varios desajustes entre flujos prometidos, nodos y aceptación.

## Bloqueantes

1. **`G_WRITE` es a la vez prerrequisito y productor de WS12; su evidencia mezcla decisión humana y prueba técnica.**
   - `dag.yaml` `gates.G_WRITE.resolver: WS07/WS12`; `tasks.WS12.requires` incluye `G_WRITE`; `build_plan.py` fija `producers['G_WRITE']='WS07'`.
   - Como está escrito, WS12 consume y produce el gate. La evidencia incluye `before-image`, que WS07 (acta humana P03–P06) no puede demostrar y que probablemente exige WS20, el cual depende de WS12.
   - Corrección: añadir `producer` único y `resolvers` como lista en el YAML; separar `G_WRITE_POLICY` (WS07, acta P03–P06) de la prueba técnica (`G_SOURCE` en WS20, concurrencia en WS12); quitar `before-image` de la evidencia de WS07. Validar que ningún productor sea consumidor.

2. **El diagrama no se genera solo del YAML: los productores de gates están hardcodeados y el chequeo de ciclos no prueba el resolver declarado.**
   - `build_plan.py` §`producers`; `README.md` (“dag.yaml es la única fuente”); `validation.txt` (“no cycles”).
   - Consecuencia: cambiar `resolver` en el YAML no cambia el diagrama, y el ciclo WS12↔G_WRITE queda oculto porque la proyección ignora `WS12`.
   - Corrección: leer `producer` del YAML, generar aristas desde él, fallar si un gate interno no tiene exactamente un productor, y añadir prueba de consistencia YAML↔proyección.

3. **La matriz de cobertura promete gates/implementaciones que los nodos no cubren.**
   - **UF10 (arranque/proyecto sin desk):** `cobertura.md` lo asigna a WS15/WS16, pero `task-ws15.md`, `task-ws16.md` y `task-ws17.md` no mencionan orientación sin desk, `init` CLI ni refresco; `alcance.md` §Arranque sí lo promete. Añadir ese alcance/aceptación a WS15 y UF10 a WS16, o crear nodo explícito.
   - **UF09 (modelos):** `cobertura.md` y `validacion-humana.md` prometen “prueba humana específica WS39”, pero `task-ws39.md` solo requiere `G_UI`/`G_WRITE`; no hay gate humano ni acta. Añadir `G_HUMAN_MODEL` producido por WS39, o retirar la promesa y marcar el capítulo como propuesto.
   - **UF08 (otro desk):** `user-flows.md` y `cobertura.md` prometen “envío autorizado” y gate WS30, pero `decisiones.md` P07 define multidesk inicialmente lectura y “sin mutación cruzada”, y `task-ws30.md` no incluye envío. Decidir si el mensaje a inbox es una excepción explícita a P07, o dejar UF08 read-only y retirar el envío.
   - **UF03 (conocimiento):** promete “dividir o reunir” y “materializar”; `task-ws24.md` cubre navegación/clasificación, no esas operaciones. Añadirlas a WS24/WS25 con operaciones públicas, o reducirlas explícitamente en UF03 y manual.

## Correcciones sustantivas (no estructurales)

4. **Dos rutas de “ejemplo” incompatibles.** `validacion-humana.md` fija `.tmp/workspace-documental-ejemplo/`; `task-ws17.md` escribe `ejemplo/README.md`, `ejemplo/desk/README.md`, `ejemplo/mapas/`. Consecuencia: los índices authored de WS17 pueden no ser el corpus que validan WS16/WS30. Fijar una sola ruta canónica y usarla en WS16, WS17, WS30 y manual; declarar WS17 como dependencia del gate que valida índices.

5. **El manual no cubre los flujos que el plan sí incluye.** `borradores/manual.md:23` dice “UF01–UF08”; `user-flows.md` llega a UF10. Corregir a UF01–UF10 y añadir capítulos/etiquetas de modelos (UF09) y arranque (UF10), o declararlos fuera de alcance en `manual.md` y `WS10`.

6. **Evidencia/actor de gates incompletos.** `G_EXEC` no tiene acta ni ruta de evidencia (a diferencia de `G_HUMAN_*`); `G_UI` exige “confirmación del responsable graph_ui” sin artefacto externo verificable. `G_SCION` lo resuelve WS05, pero `task-ws05.md` solo promete “señalar campos no expuestos”, no una consulta real que exige la evidencia. Corrección: acta para G_EXEC, nota/commit en graph_ui para G_UI, y autorizar explícitamente un probe read-only en WS05 o mover `G_SCION` a WS33.

7. **Decisión de producto ausente sobre entradas/índices reales.** `vision.md:32` deja abierto dónde viven; `decisiones.md` P01–P08 no lo incluye; `task-ws17.md` limita las entradas al ejemplo y prohíbe escribir otros proyectos. Si el encargo “ecosistema navegable” incluye entradas en repos reales, falta P09 o una decisión explícita de que solo el ejemplo está en alcance.

## Sugerencias

8. `README.md` §Entregas dice “WS13–16 … antes de índices nuevos”, pero WS17 solo depende de WS11 y puede ejecutarse antes de WS16. Ajustar la prosa o la arista.
9. `output_scope` mezcla raíces en graph_ui (`frontends/mindmap/...` y `shell/...`) y en spec2viz (`sldb/views/`). Concretar en promoción está previsto; conviene fijar la raíz ahora para evitar evidencia en el repo equivocado.

## Gates futuros bien modelados (no defectos)

`G_CLOSEOUT` (blocked, externo, tarea activa con hash) y `G_EXEC`/`G_HUMAN_*` (pendientes, con evidencia esperada) están correctamente modelados como futuro. No exijo su aprobación; solo corrijo evidencia/actor y la circularidad de `G_WRITE`.

## Hallazgos R1 resueltos

- Referencias externas corregidas: rutas reales de graph_ui y `...-modelos-del-desk.md`, con hash y estado observado.
- Chat invisible: `brief.md` con extractos, glosario y límites; WS01 lo valida.
- Decisiones: P01–P08 con actor, fecha/resultado requeridos y `PENDING_OWNER`; propuestas no son aprobaciones.
- Gates externos/humanos: nodos explícitos, sin prerrequisitos en texto libre; `validation.txt` los trata como no satisfechos.
- A1 monolítico: dividido en WS02–WS05; A4/A5 ya no dependen solo de borradores.
- Kimun: referencia explícita, sin migración ni dependencia silenciosa.
- Validación humana: participante, ejemplo, protocolo y presupuestos definidos.
- Superficies omitidas: Code, Schema, issues no modelados, FAQ, crossroads, modo degradado y carpetas legacy auditadas; mover/renombrar y adjuntos quedan fuera.
- Duplicación: `overlap_with`/`integration_mode` y WS06/G_UI obligan a reconciliar con las tareas draft de graph_ui.
- Destinos: `output_scope` por nodo y aviso de concretar archivos antes de promoción (parcialmente resuelto; ver 4 y 9).
