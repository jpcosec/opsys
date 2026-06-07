# Round 03 — Init, bootstrap, scaffold

**Source:** ST-init

## init

- Scaffolding completo: `.sldb/core/`, `.sldb/runtime/`, `desk/tasks/`, `desk/contexts/`, `desk/rituals/`, `desk/atoms/`, `desk/drawer/`, `desk/inbox/`, etc.
- Templates personalizados con el basename del target directory
- **Idempotente**: segunda corrida detecta "already exists" sin errores
- `init --help` no tiene descripción — solo usage line
- `init` sin path opera sobre CWD silenciosamente — el usuario puede no darse cuenta

## bootstrap

- `bootstrap --help` solo usage line, sin descripción
- `bootstrap` dice "Global deskops model registry is ready" pero no muestra qué hizo
- La diferencia entre `bootstrap` e `init` no es clara desde la ayuda

## desk install

- Existe como subcomando, acepta path posicional
- No se probó a fondo (requiere otro repo)

## graph build en scaffold fresh

- Produce KG snapshot con 1 nodo (`config_file:tag-namespaces.yaml`) y 0 edges
- Correcto para un scaffold vacío

## list atoms en scaffold fresh

- **Silencioso**: no imprime nada (no hay átomos todavía). No dice "no atoms found".

## Error handling

- Path inexistente → exit 1, mensaje claro
- Path es archivo → exit 1, mensaje claro
- Sin path → exit 0, opera en CWD (sorprendente)
