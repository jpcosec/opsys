# Comprobación focal root sobre la fuente de la tanda 3

Fecha: 2026-11-01. Texto recibido de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, antes de la tanda.

Aprobación focal sobre estos bytes. No es aprobación del plan ni de outputs futuros, ni aprobación humana.

- `decisiones.md`: `f2d4b58f41587ff91d511e801a21a11795b3ad54ec59b91edcc2c3e4a12bd72d`
- `context-review-guide.md`: `dec1766a708b1fdfea8af1233c8f2fbe5aa03ce5d7c07e431082bf9d00975d0e`

Root declara: leyó el diff completo de ambos y las cláusulas P07, P09 y T-P03.1; preguntas y respuestas 0–2 intactas; `dag.yaml`, helper, build y validate idénticos a `fc5e64a8`.

Condición: Tester de fuente PASS sin cambiar esas dos fuentes. Tester v3: PASS, `tester-v3-result-summary.md`. Los bytes coinciden con estos hashes, comprobado con `sha256sum` antes del commit.

Para WS12: antes de habilitar modo exclusivo aplica T-P03.1 como requisito de su policy, no como supuesto de que exista detección. La fuente histórica del actor inicial sigue sin localizar.
