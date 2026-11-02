# Corrección de WS12, siete ajustes aplicados y decisiones pendientes

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-02. Nada ejecutado en runtime. No es aprobación de nadie. Contrato en borrador. Tarea activa.

**Paro aquí, como pediste: quedan ambigüedades materiales. No lancé las tres revisiones frescas ni renové nada.**

- `contratos/operaciones.md` sha256 `5ea0f7b6e82eb402524ca9acf2cbc09c82a46b2a5d4ede2bd858b3ab81852c02`
- `dag.yaml` sha256 `e4d8b772d33950125a7cf5f896ef7512e659452a5858d3e1e57ac2593654856f`
- `patch-2-contrato.diff` sha256 `69c1d037c2f1944f0c180d8a5b489f60fc6d0b58e07141dee51f6f5418f49394`, `patch-2-dag.diff` sha256 `33adc144de475620583c416d1ed0ec44b661067bdae45a05d20081cfbf2c4c71`, desde `2da226ed`
- Tabla de los siete puntos: `result-summary.md`, sección «Segunda pasada».

## Estado de los siete

Aplicados. Tester independiente de los siete sobre `3b4a6c35`: FAIL con tres gemelas reales, corregidas; el resto en PASS, `renovacion-4/`. Focal de esas gemelas sobre bytes finales: PASS. Cobertura incremental: ningún Tester único recorre los siete sobre bytes finales. El punto 6 no afecta al intake: nunca dijo «no valida», sino que el error va en la posición de `path`; no lo modifiqué.

Coteje en fuente: `drawer.py:117-140`, `operations.py:284-300,1235-1245,1297-1328`, `deskops-view.js:27-30,51`.

Invalidación: 35 «input changed» y 3 pendientes (`stale-medido-2.log`); mismos conteos que antes. Sin ciclos, por script. `validate --check` en `freeze-2-validation.log`.

## Decisiones que necesito

**1. Canal para preparar un candidato no rastreado.** `promote` crea el candidato sin rastrearlo (`drawer.py:117-140`) y `/save update` exige documento rastreado (`save_plan.py:49-50`). Tu punto 2 eligió `/save update`, de modo que ese canal no alcanza el caso normal. Opciones: (a) `edit task` (W02): alcanza el drawer y ya tiene guarda de contenido, sin `expected`; (b) rastrear primero con S06 y usar S02: amplía la whitelist y arriesga colisión de id con `add task` (7.3); (c) declarar no disponible los no rastreados.
**Recomiendo (a) para no rastreados**, como canal sin precondición de 5.7 (ii-b), con la aceptación de «guardado obsoleto» limitada a candidatos rastreados. Consecuencia: en ese caso WS47 y G_PAYLOAD_PRECONDITION no aportan.

**2. `closeout_evidence` en el candidato.** Protegido en edición (W03, NOAC); UF04 la pide en la preparación y es lo único que la persiste ahí, sin validar vocabulario. **Recomiendo una excepción acotada a `desk/drawer/tasks/`, con vocabulario validado por el adaptador**, y seguir protegido en tarea activa. La alternativa es declararla solo al crear la tarea activa, en WS26.2, lo que aparta a WS26.1 de UF04.

**3. Pills en el candidato.** `bind` no alcanza el drawer. Queda la lista entera con existencia comprobada por el adaptador. **Recomiendo aceptarlo**: ya está redactado.

**4. Agregado WS26.** WS19 declara G_PAYLOAD_PRECONDITION y WS26 no, ahora que WS26.1 lo requiere. **Recomiendo añadirlo** por simetría; WS26 ya está entre los invalidados.

**5. Residuo de WS47, sin decisión tuya salvo que discrepes.** El criterio es el de `_write_doc`; no verifiqué que sus tres comprobaciones definan toda «pérdida». El contrato obliga a WS47 a declarar el residuo antes de su aceptación.

No identifico compromiso humano afectado ni productor ausente. Los gaps son de interfaz pública.

Con tu respuesta aplico lo decidido, lo cubro con Tester y sigo con las tres revisiones frescas y la renovación medida, sin otra parada salvo novedad material.
