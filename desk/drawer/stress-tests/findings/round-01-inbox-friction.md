# Round 01 — Inbox capture friction

**Source:** ST-02

## Slugification pierde información

- `deskops inbox "¿Cómo va?"` → filename `...-como-va`
- `deskops inbox "ñandú > 100º"` → filename `...-and-100`
- `deskops inbox "test con ñ, ¿, símbolos: -> <html> </html>"` → filename `...-test-con-caracteres-s-mbolos-html-html`
- Caracteres UTF-8 se pierden en la conversión a slug. El filename no es representativo del contenido.

## Input largo = filename inservible

- 5000 caracteres de largo producen filename con 68 `a`s consecutivas y un sufijo `-unclear`.
- No hay forma de referenciar esa nota después sin buscar por contenido.

## Sin detección de duplicados

- Mismo mensaje dos veces → dos archivos independientes con distinto timestamp.
- No hay advertencia de duplicado.

## Default kind silencioso

- `deskops inbox "mensaje"` (sin `--kind`) crea nota con `kind: unclear`.
- El usuario no sabe que `--kind suggestion` o `--kind question` existen a menos que lea `--help`.

## --show no visible en --list

- `deskops inbox --list` muestra notas pero no sugiere que `--show <id>` existe para ver detalle.
- El usuario tiene que saber del flag por `--help`.
