# SLDB template markers

ID: pill-sldb-template-markers

## What

SLDB usa marcadores dentro del `__template__` de un modelo para definir dónde va cada campo en el markdown. Hay tres tipos:

### `⸢rev•fieldname⸥`

Valor **scalar**. Se reemplaza por el valor del campo al renderizar, y se extrae del mismo lugar al leer. Usado en frontmatter y body:

```yaml
id: ⸢rev•id⸥
status: ⸢rev•status⸥
```

```markdown
## Goal

⸢rev•goal⸥
```

### `⸢rev,list•fieldname⸥`

Valor **lista**. SLDB lo renderiza como items `- item` y al extraer, parsea cada `- ` como un elemento de la lista. El template debe tener el prefijo `- `:

```markdown
## Validation

- ⸢rev,list•validation⸥
```

### `⸢render•fieldname⸥`

Campo **compuesto**. SLDB no lo extrae del documento — lo construye desde `__compositions__` al renderizar. La composición define un modelo fuente, un campo con referencias, y un template:

```python
__compositions__ = {
    "fieldname": {
        "source_field": "refs",
        "model": "model.path:ModelClass",
        "template": "- {field1} [{field2}]",
    }
}
```

## Texto fijo alrededor de marcadores

SLDB soporta texto fijo alrededor de los marcadores. Ese texto:

- **No se modifica** al renderizar (se replica tal cual)
- **Sirve de anclaje** al extraer (SLDB ubica el marcador por el texto que lo rodea)
- **Guía al autor** cuando se renderiza un documento nuevo

```markdown
## Goal

_Describe el resultado concreto._

⸢rev•goal⸥
```

El texto en cursiva es fijo del template, no del documento.

## Where

Los templates se definen en `__template__` como strings multilínea en cada modelo Pydantic bajo `deskops/models/*.py`.

## How

`TemplateExtractor` parsea el template y registra recipes (marcador → posición/contexto). `DataExtractor` usa esos recipes para leer el documento real. `SLDBRenderer` usa los mismos recipes para escribir.

## Tags

- system:sldb
- topic:templates
