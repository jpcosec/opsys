# Causa de los 216 fallos técnicos (2026-10-31)

Los intentos con returncode -9 no llegaron al modelo. El runner lanzaba `pi --print` con stdin heredado de un socket abierto, y Pi espera ese stdin antes de empezar: 0 eventos con `--mode json`, timeout sin salida ni stderr.
Comprobación: el mismo comando con stdin desde /dev/null respondió en 1,7 s.
No fue caída de DeepSeek, cuota ni contenido del plan; la hipótesis inicial de falla intermitente era errónea.
Corrección: `stdin=subprocess.DEVNULL` en context_review.py. Esos intentos se conservan como fallos del runner. No son evidencia de review ni cuentan para el tope de 3 intentos por input; los recibos nuevos llevan `stdin: devnull`.
