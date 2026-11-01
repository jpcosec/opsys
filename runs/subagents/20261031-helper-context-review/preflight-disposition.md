# Comparación del coordinador — helper context_review, aceptada para despacho

Leí preflight y cold completos. Reproducen los cuatro requisitos, el límite de no tocar FILE:instruccion ni validadores, y las pruebas sin proveedor. Sus ambigüedades son de API menor y quedan fijadas aquí; obligan a Executor y Tester.

- INSTRUCTION_VERSION: cadena `v2-ejecucion-hipotetica`. Los intentos históricos sin el campo son versión original.
- Clasificador: `receipt_state(receipt: dict) -> tuple[str, list[str]]`, estado `complete`, `incomplete` o `technical_failure`, y campos faltantes. Campos requeridos: los que escribe hoy el runner: argv, cwd, stdin, pi_version, start, end, pid, returncode, input_sha256, output_sha256, technical_failure. Un recibo con technical_failure verdadero es `technical_failure`.
- Evidencia registrada: primer elemento de `context_review.evidence`, directorio de intento; su `receipt.json`. Sin ese archivo también es incompleto.
- Numeración: la de attempt_dir, siguiente libre desde 1.
- argv efectivo: la lista pasada a Popen, tal cual.
- `--reason` sin `--new-attempt`, `--new-attempt` sin ids o sin razón, o combinado con `--stale`: parser.error, sin crear nada.
- Contar WS12 y WS37 como únicos incompletos es una validación del Supervisor; si aparece otro, se reporta sin tocar datos.
