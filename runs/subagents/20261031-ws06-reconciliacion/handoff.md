# Handoff WS06 — para revisión root

Fecha: 2026-10-31. Autor: Claude, pane `w3Y:p1`. Sin push.

**Estado: WS06 cerrada por el gate. No activé WS07, WS08–12, código UI ni el ajuste canónico.** Espero tu revisión.

**Atención: `validate_plan.py --check` falla hoy y es el efecto declarado, no un descuido.** Editar `reconciliacion.md` invalidó 25 revisiones baratas. Regularizarlo exige escribir en `dag.yaml`, fuera del scope de WS06, y queda capturado en el ajuste canónico.

## Commits

| Commit | Qué |
|---|---|
| `567b20ce` | Activación de WS06 y `approval.md` con tu dictamen |
| `b027a2f2` | Disposición de preflight y cold |
| `71f1f6f4` | Matriz en `reconciliacion.md` y evidencia |
| `ff28c68c` | Closeout: «declaró commit, document; encontré commit, document» |
| `6d41f301` | Ajuste canónico capturado en drawer, sin ejecutar |

Entregable: `desk/drawer/plans/workspace-documental/reconciliacion.md`, sha256 `7a85a5816747e681c5a2e270c3edff1e912d5f04f89bea3cd541d6be2e5d6bce`, sección «Matriz de correspondencia WS06». El texto previo quedó intacto, comprobado byte a byte contra `git show`. Evidencia en esta carpeta.

## Matriz

68 filas únicas, por capacidad y no por nodo:

| Repo dueño | Filas |
|---|---|
| graph_ui | 37 |
| sldb | 10 |
| spec2viz | 3 |
| deskops | 18 |

| Clasificación | Filas |
|---|---|
| ya cubierto | 33 |
| nuevo delta | 32 |
| extender ticket | 2 |
| no adoptado | 1 |

Cobertura: 63 de 63 nodos, 21 con «sin delta» y motivo. Tu valor «reusable» es «ya cubierto» aquí; es capacidad observable con sus límites, no aceptación ampliada.

Aplicación de tus condiciones:

- Tickets de edición y Changes se extienden en serie: C-14 y C-28. C-28 declara que doctor y drift amplían lo que nombra el ticket.
- `frontends/workspace`: «no adoptado», valor que agregué solo para esa fila.
- ViewDoc: C-37 evaluador y rutas en graph_ui, solo local; C-48 modelo en spec2viz; C-49 notación; C-50 solo portabilidad o independencia del host. Sin evaluador de cero.
- `expected`: C-40 ya cubierto con límites; C-41 CAS como nuevo delta, en sldb.
- Scion: C-64 conserva WS32/33 sin WS05, apunta al candidato del drawer; C-65 a C-68 quedan para el ramal E. El operador Scion aparece solo ahí y en C-36.
- Filas de deskops: «no designado en P01», porque P01 cubre graph_ui, sldb y spec2viz. No lo inventé; es un hueco que el solicitante puede cerrar.
- Ninguna fila acepta un delta. Recibos externos del receptor P01; WS11 y WS12 son fuente de contrato. La TaskDoc lo aclara; `dag.yaml` aún conserva el texto viejo (ajuste 4).

## Ajuste canónico, sin ejecutar

Candidato `desk/drawer/tasks/task-ajuste-canonico-tras-ws06.md`, detalle en `canonical-adjustments.md`:

1. **CAS:** `brief.md:40` y WS19.1 dan por hecho un hash CAS que no existe. El vacío es el CAS de guardado de payload por campos, y C-41 no tiene nodo productor en el DAG. Afecta WS19, WS19.1, WS19.2, WS20, WS21, WS12 y WS42.
2. **Captura directa a drawer:** WS25.2 necesita un productor en deskops, porque hoy solo existe `promote` desde inbox. Afecta WS25, WS25.2 y WS12.
3. **ViewDoc:** `brief.md:24` y WS18. `output_scope` de WS18 apunta a `sldb/views/` con dueño spec2viz. Afecta WS18, WS24, WS09 y WS11.
4. **Texto de recibos** en WS06. Afecta WS06, WS11 y WS12.
5. **Re-review de 25 nodos** y su registro en `dag.yaml`: PK01, WS04, WS06, WS13, WS13.1–13.3, WS14, WS15, WS15.1–15.2, WS19, WS19.1–19.2, WS21, WS22, WS23, WS24, WS29, WS32, WS32.1–32.2, WS33, WS33.1–33.2.

Orden que propongo: primero 1–4, que cambian inputs, y al final 5, para no repetir re-reviews. Los cuatro primeros cambian contratos, por lo que deberían pasar por tu revisión antes de activarse.

## Verificación

- Preflight y cold en procesos Pi nuevos, resueltos por disposición, que agregó «no adoptado» y las reglas de cobertura.
- Executor nuevo Claude Sonnet.
- Tester Pi read-only `w3Y:pD`: PASS con hallazgos sobre C-50, C-64, C-28 y ajuste 1, corregidos. Tester nuevo del delta: PASS.
- Mi recuento: 68 filas, 33/32/2/1, 63/63, prefijo intacto. `build_plan.py --check` exit 0. `context_review.py status`: 25 «input changed», exactamente los declarados. Diff protegido sobre código, `dag.yaml`, `brief.md` y auditorías: 0 archivos.

## Límites

- El Tester muestreó, no cubrió las 68 filas: 12 ya cubierto, 10 nuevo delta, las 3 entonces extender ticket, 5 dudosas y 10 sin delta. Quedó NO VERIFICADO código de C-33. Los commits vienen de las auditorías y no se comprobaron con `git show` por fila.
- Filas deskops citan el HEAD auditado `215bf624`, porque WS02 no cita commit por fila.
- Las filas «ya cubierto» son lectura de código y auditorías, nada se ejecutó.
- Nodos y orden de la atomización son propuesta, sin tareas creadas.
- deskops está 40 commits adelante de `origin`, incluidos los de otras sesiones.
