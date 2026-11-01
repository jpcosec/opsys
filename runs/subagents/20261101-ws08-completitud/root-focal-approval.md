# Comprobación focal root del parche WS08

Fecha: 2026-11-01. Mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`. Aprueba renovar revisiones sobre el parche congelado en `023a05e3`, por bytes. No aprueba el cierre de fase ni las revisiones futuras, y no es aprobación humana.

- `user-flows.md`: `0a1e754ca010b31e6344ec278b3e24d4d9d7503549ba5f2daceb63035958ed47`
- `cobertura.md`: `1104a1f134364cb16d9113768b70de6304252227935d3ec3ccb93abf6d64a4a9`

Root declara: leyó diff completo, matriz de las diez UF y Tester focal; los SHA256 coinciden con `git show 023a05e3`; `parche-diff.txt` coincide con el diff real; las diez líneas Gate humano son idénticas; `dag.yaml`, helper, decisiones, guía, `manual.md` y validadores idénticos a `f92ed754`; build --check 0; 73 `input changed`.

Instrucciones: tanda de 73 con DeepSeek Flash, thinking low, v2, sin recortar ni normalizar fuentes. Comparar cada reformulación y dry-run con contrato completo y sentido de aristas y gates. No rescatar una contradicción real con interpretación experta ni aceptar por número de intentos; una paráfrasis equivalente se acepta leída en contexto, con motivo concreto. Sin ediciones cosméticas de fuente; un defecto material va primero a root con diff y alcance. WS10 conserva su aprobación; sus revisiones se renuevan sin rehacer `manual.md`. No cerrar fase ni activar WS09/WS11/WS12/UI/Scion/push antes del checkpoint.
