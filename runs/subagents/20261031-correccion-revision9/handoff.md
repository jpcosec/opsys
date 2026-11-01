# Handoff corrección de la revisión 9 — para revisión root

Fecha: 2026-10-31. Autor: Claude Opus 5.5, pane `w3Y:p1`. Sin push.

**Estado: tarea cerrada por el gate. `build_plan.py --check` 0, `validate_plan.py --check` 0, `context_review.py status` «all reviews current».** Revisión 9, `final_plan_reviewed`, 64 nodos, 16 gates. No activé WS07, WS08–12 ni UI. Espero tu revisión.

Reconozco el punto 4 como falta mía: la línea «revisado por el coordinador» la ordené yo y era falsa.

## Tus cuatro puntos

1. **G_SOURCE:** WS12 dice «G_PAYLOAD_PRECONDITION y, solo en variante editable, G_SOURCE». Sin cambios en P04, gates ni actores.
2. **Timeout:** WS12 asume producir por delta de WS34.1 y WS34.2 la política, el umbral y la clasificación observable. La duración la fija esa sección al preparar esos deltas, no WS34. No bloquea el contrato núcleo. WS34.1 y WS34.2 solo avanzan con esa política verificada en `G_WRITE_CONTRACT`, sin umbral propio. No toqué el gate, que ya evalúa por delta.
3. **WS19.1:** el intento final, con input nuevo porque cambió WS12, describe campos, consumo de precondición, bloqueo de protegidos, buffer, conflicto y validación. Los intentos previos quedan sin crédito.
4. **Provenancia:** `comparison-ledger.md`, con supersesión fechada, qué leí exactamente y 73 filas con actor, hashes y fecha. Las disposiciones viejas no se editaron. Leí contrato (`scope` y `acceptance`), output y disposición de los 73, y volví a leer los 34 que cambiaron. Asumo la aceptación.

## Lo que encontró la comparación, y que tu revisión no listaba

- WS12 no decía quién fija la duración: un revisor la atribuyó a WS34.
- El destino protoátomo de WS25.2 no estaba asumido por WS12: misma falta de productor que el timeout. Corregido.
- WS42: «validar materializaciones» sin regla de hueco. Corregido.
- WS37: dry-run «cambios ninguno» en un nodo que entrega acta. No lo marcaba tu escaneo porque no estaba en tu lista. Repetido.
- WS19, WS25.1, WS26.1 y WS27.2: reformulaban la revisión en vez del encargo. Repetidos.

## Instrucción de reviewer

La última tanda de 33 nodos, más WS12 y WS37, usó el SYSTEM ampliado de `final-instruction.txt`, que pide ejecución hipotética. `context_review.py` no se modificó: ARGV se reemplazó en memoria, y `manifest.json` y `receipt.json` lo registran. **Consecuencia que debes valorar:** el SYSTEM del archivo sigue siendo el original, así que una revisión futura con el runner puede repetir el defecto de reformular la revisión. Corregirlo requiere una tarea específica sobre el helper; no la abrí.

## Commits

`2295acf0` drawer; `3a201e28` activación; `deef3c40` y `4c1b4bd3` fuentes congeladas; `83b8be66` ledger y registro; `e91d0495` correcciones al ledger; closeout y handoff al final de esta tanda, con `git log` como autoridad.

`git diff --name-only 5f05281c` sobre código, `decisiones.md`, auditorías y validadores: 0 archivos.

## Tester

Pi deepseek-flash, solo lectura, `w3Y:pF`: PASS. Tres hallazgos que corregí por atestación en el ledger, sin reescribir archivos:

- WS22: la disposición resolvía algo que el contrato deja abierto. Reclasificado como detalle de promoción abierto.
- WS13.1: cita desplazada. Igual.
- WS12 y WS37 `attempt-2`: `manifest.json` copiado dice `attempt: 1`. Para esos intentos vale `receipt.json`.

El Tester no pudo verificar la afirmación de que comparé los 73 nodos ni recomputar hashes: lo primero es atestación mía, lo segundo es verificable por ti.

## Riesgos residuales

- 39 disposiciones siguen siendo redacción del agente, con la frase falsa conservada. Las leí; dos de ellas exageraban, y el Tester las halló en una muestra de 12. **Pueden quedar otras igual de laxas: mi lectura no las detectó.**
- 73 revisiones con DeepSeek flash: la comprensión es tan buena como ese modelo y mi comparación. Las tres rondas mostraron que una misma entrada produce resultados distintos.
- `promotion-notes.md` conserva detalles reales para las TaskDoc: WS13.1, WS22, WS27.1, WS27.2, WS32.1, WS39, WS45.
- Nada se ejecutó: ni código, ni tests, ni UI.
- `closeout verify` sigue sin anticipar la evidencia que exige `closeout commit`; volvió a fallar aquí.
- deskops está más de 50 commits adelante de `origin`.
