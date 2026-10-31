# R3 — Revisión de seguimiento (deepseek)

**Veredicto: APTO COMO PLAN.**

Validación ejecutada: `validate_plan.py` PASS; `build_plan.py --check` PASS (43 candidatas, 15 gates, sin ciclos; referencias externas con hash sin cambios). `validate_plan.py` reescribe `validation.txt`; el contenido generado coincide con el entregado.

## Bloqueantes

Ninguno. No encuentro una tarea que, con sus dependencias y gates satisfechos, no pueda promoverse o ejecutarse. Los pendientes son gates futuros con productor, actor o evidencia declarados; no los trato como aprobaciones faltantes.

## Sugerencias no bloqueantes

1. **`README.md` §Entregas contradice el DAG.** Dice que “WS29 (Changes) y WS42 (Schema) son extensiones … no prerrequisitos del lector o manual básico”. WS42 es operaciones de conocimiento y `WS30` depende de `WS42`; Schema es WS39. Corregir la frase en la plantilla de `build_plan.py` (o derivarla de `dag.yaml`): cambiar “WS42 (Schema)” por “WS39 (Schema)” y no afirmar que WS42 no precede al manual.
2. **`cobertura.md` UF01 asigna “WS30 para índices”, pero `WS30` no menciona UF01 ni WS17 en alcance/aceptación.** Añadir explícitamente “UF01 con entradas authored WS17” a la aceptación de WS30, o mover ese gate a WS43, que sí publica la navegación real.
3. **WS16 y el corpus de entrada.** `WS16` depende de WS40/WS41, no de WS17; WS40 solo materializa plantillas WS17 “opcionalmente”. El gate humano temprano de UF01 puede terminar validando búsqueda sin una entrada ecosistema/desk. Hacer que WS40 genere una entrada mínima, o declarar que WS16 valida UF01 por búsqueda y que WS30/WS43 lo validan por entrada.
4. **Alcance de `G_UI_READ` para WS40.** WS11 produce el gate como aceptación del “delta lector”/ViewDoc; WS40 es generador de fixtures y WS41 lectura multidesk. Aclarar que el acta de WS11 cubre esos deltas o añadir un alcance aceptado específico; de otro modo WS40 puede quedar esperando una aceptación que no lo menciona.
5. **Evidencia en repo dueño.** WS16/30/37/39 son de `graph_ui`, pero sus `output_scope` usan `evidencia/...` relativo al paquete del plan. Fijar si la evidencia se archiva en el repo dueño o bajo una excepción explícita de evidencia de plan, para que el cierre sea auditable.

## Hallazgos R2 resueltos

- `G_WRITE` dividido en `G_WRITE_POLICY` (WS07) y `G_WRITE_CONTRACT` (WS12); productores en `dag.yaml`, sin ciclo WS12↔gate.
- Productores de gates leídos del YAML; proyecciones y chequeo de ciclos coherentes.
- Aceptación por repo receptor en WS11/12; WS06 solo propone correspondencias.
- WS40 corpus único, WS41 lectura multidesk, WS42 operaciones de conocimiento, WS43 publicación real; UF03/UF08/UF10 alineados y sin promesa de envío interdesk.
- Toda mutación baseline exige `G_HUMAN_READ`; WS20/21 resueltos con `source_mode` pending/editable/read_only y G_SOURCE solo en editable.
- P09 añadido para ubicación de entradas reales; ejemplo reproducible bajo WS40 y plantillas WS17 separadas.
- Manual actualizado a UF01–UF10; UF09 con `G_HUMAN_MODEL` producido por WS39.
