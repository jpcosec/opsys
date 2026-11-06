## REFORMULACION

**Propósito:** corregir la regresión de GC03 que deja `review` sin clasificar en la gramática de primer nivel del CLI, haciendo fallar `tests/test_cli_grammar.py::test_top_level_nouns_are_classified_exactly_once`.

**Resultado:** `review` clasificado exactamente una vez en `TOP_LEVEL_GRAMMAR['operational']` dentro de `tests/test_cli_grammar.py`, con una aserción de `mutates` coherente con `deskops/cli/registry.py` (sin modificarlo), más una línea en `CHANGELOG.md` bajo Unreleased/Fixed.

**Repo:** deskops (workspace `desk`). Archivos tocados: `tests/test_cli_grammar.py`, `CHANGELOG.md`.

**Límites:** fuera de alcance `deskops/cli/registry.py`, parser, ayuda, goldens, `docs/` y cualquier otro sustantivo. No se corrige el registro aunque contradiga el comportamiento real: solo se anota como hallazgo.

## AMBIGUEDADES

1. "con el valor que hoy declara deskops/cli/registry.py, sin cambiarlo" vs. "Si el registro declara un valor que contradice lo que el comando hace... se anota en la Validation". No queda claro si un test debe fijar el valor del registro aunque sea falso; obligaría a inventar la política de aserción ante contradicción.
2. "Si command_for_path(('review',)) existe" — condicional sin dato; obligaría a inventar cuál rama aplica antes de leer el registro.
3. "fijar mutates de ('review','status') (no muta) y ('review','preflight') (muta)" — afirma valores concretos sin citar el registro; obligaría a inventar si son del registro o expectativa del autor.

## DRY-RUN

**Lecturas:** `deskops/cli/registry.py` (CommandSpec de `review` y `mutates`), `tests/test_cli_grammar.py` (TOP_LEVEL_GRAMMAR, `test_operational_mutates_guards`), `CHANGELOG.md`.

**Cambios previstos:** añadir `"review"` a la lista operational; añadir aserción de mutates según la rama que exista; una línea en Unreleased/Fixed.

**Dependencias:** existencia de `command_for_path(('review',))` o de subcomandos; valor `mutates` actual del registro.

**Validaciones futuras:** `pytest -q tests/test_cli_grammar.py`, `pytest -q tests/test_cli_help_examples.py`, `git diff --stat origin/main` acotado a los dos archivos.

No es agregado ni paquete: es una tarea ejecutable única.

## FUTURO

- El coordinador decide qué hacer si el registro contradice el comportamiento (hallazgo anotado).
- Un nodo ejecutor aplica los cambios y corre las validaciones.
- Un revisor humano valida el diff y el CHANGELOG.
