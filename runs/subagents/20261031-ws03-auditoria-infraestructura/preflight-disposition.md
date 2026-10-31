# Comparación del coordinador — WS03, aceptada para despacho

Revisiones: preflight y cold v1–v4, cada una en proceso Pi nuevo, sin herramientas y con stdin DEVNULL (recibos `*-receipt.json`). El insumo final es la TaskDoc vigente; `preflight.md` guarda la reformulación final, copia de `preflight-v4.md`.

Las cuatro rondas reproducen el objetivo, el entregable único, el repo y los límites: solo lectura, sin Scion, sin contratos nuevos, sin commits del Executor. Ningún revisor confundió la tarea con implementación ni propuso ejecutar fuera del alcance. v1–v3 detectaron lagunas reales (columnas, universo, hash, roles, atribución) y se corrigieron en la TaskDoc con `deskops edit task`. Los hallazgos de v4 son detalle o quedan resueltos aquí; estas resoluciones obligan al Executor y al Tester.

## Resoluciones sobre v4
- Repo leído = se abrió al menos un archivo suyo o se corrió una consulta sobre él. Las líneas de `git status --short` se cuentan tal cual.
- `--help` y comandos de lectura de cada CLI están permitidos; se corren con las herramientas ya instaladas, sin instalar nada.
- ViewDoc: `brief.md` lo llama «contrato existente de spec2viz». Manda el código: si no aparece se registra ausente y la discrepancia con el brief se reporta como hallazgo, sin editar el brief. Una aparición en tests, docs o comentarios se registra con su tipo y no cuenta como implementación.
- Estado ausente: la ubicación es «—» y la evidencia es el comando usado. Un mecanismo ausente en los tres repos va en una fila; si difiere por repo, una por repo.
- Documento = lo que cada repo trata como documento según su código. Fuera de git: «sin git», con SHA-256 si se cita.
- La activación está en activation.md; `execution_authorized=false` describe el cierre de planificación y no bloquea esta auditoría.
