# Writing instructional text in templates

ID: pill-template-instructional-text

## What

Los templates SLDB (`__template__`) pueden incluir texto fijo alrededor de los marcadores `⸢rev•⸥`. Ese texto aparece en todos los documentos del tipo y es una oportunidad para guiar a quien escribe.

## Why

Sin texto instructivo, un documento nuevo renderizado muestra campos vacíos sin contexto. El autor tiene que saber de antemano qué va en cada campo, o ir a buscar la documentación del modelo.

Con texto instructivo, el template es autosuficiente: al abrir un documento nuevo ya se entiende qué llenar.

## When

Siempre que se define o modifica un `__template__`. Aplica a todos los modelos.

## Where

En el `__template__` de cada modelo, como texto alrededor de `⸢rev•field⸥` / `⸢rev,list•field⸥`.

## How

Reglas:

1. **Una línea por campo como máximo**. Si necesitas más, el campo está mal diseñado.
2. **Estilo: cursiva `_..._`**. Se lee como instrucción, no como contenido del documento.
3. **Verbos en imperativo**: "Describe...", "Lista...", "Indica...".
4. **Si el campo tiene valores fijos, menciónalos**: `# draft | active | blocked`.
5. **Ubicación**: justo antes del marcador, en la línea anterior.
6. **No reemplaces el marcador**: el texto instructivo va antes, el marcador sigue en su línea.

```markdown
## Goal

_Describe el resultado concreto que debe producir esta tarea._

⸢rev•goal⸥
```

No hagas:

```markdown
## Goal

⸢rev•goal⸥ _Describe el resultado concreto..._
```

## How Not

- No uses texto instructivo para documentar el modelo. Para eso están los `Field(description=...)`.
- No repitas información obvia. "ID del documento" para un campo `id` no agrega valor.
- No uses párrafos largos. Una frase corta por campo.
- No pongas instrucciones en frontmatter (comentarios YAML no se soportan). Ponlas en el body.

## Tags

- system:deskops
- topic:templates
- topic:documentation
