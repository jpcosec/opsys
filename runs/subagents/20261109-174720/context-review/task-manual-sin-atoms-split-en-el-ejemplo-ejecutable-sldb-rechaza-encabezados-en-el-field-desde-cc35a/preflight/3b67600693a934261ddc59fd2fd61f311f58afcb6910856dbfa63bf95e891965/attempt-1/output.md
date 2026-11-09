## REFORMULACION
Propósito: corregir el ejemplo ejecutable del manual que usa `atoms split` con encabezados, rechazado por sldb desde CC35a. Resultado: `docs/operator-manual.md` deja de mostrar split como bloque ejecutable; la sección pasa a «Merge, delete, and validate»; el bloque crea dos átomos con answer plano, los fusiona y conserva delete/validate/list/show; una línea remite al drawer; `test_operator_manual` vuelve a verde sin tocar el test. Repo: `deskops-desk-cc`, superficie indicada sobre `origin/main 4699f912`. Límites: solo `docs/operator-manual.md` (sección alrededor de :661-695) y una línea en `CHANGELOG.md`; fuera el código de split, `tests/test_atoms_split.py`, `tests/test_operator_manual.py` y otros bloques del manual.

## AMBIGUEDADES
1. «con los ids que genera add atom (atom-<slug del título>)»: no define el algoritmo exacto del slug ni cómo capturarlo; obligaría a inventar la correspondencia título→id o el método de obtención.
2. «CHANGELOG.md (una línea en ## [Unreleased] / ### Changed)»: no da el texto de la línea; obligaría a inventar redacción y posición exacta.
3. «corre desde una copia del worktree en /dev/shm si lee mucho»: «lee mucho» carece de umbral; obligaría a inventar el criterio para copiar o no.
4. «SUPERFICIE (origin/main 4699f912)»: no indica el checkout/base de ejecución real; obligaría a inventar si se trabaja sobre esa referencia, otra rama o el worktree actual.

## DRY-RUN
Lecturas: sección «### Split, merge, delete, and validate» y bloque runnable de `docs/operator-manual.md`; `CHANGELOG.md`; `tests/test_operator_manual.py` para entender el orden, sin modificarlo. Cambios previstos: renombrar la sección; reescribir el párrafo inicial; sustituir el bloque por add de dos átomos con answer plano, merge, delete, validate, list y show; quitar la frase de `atoms split --section`; añadir una línea al CHANGELOG. Dependencias: CLI `deskops` y sandbox propio del manual; entorno de tests. Validaciones futuras: ejecutar de a uno `tests/test_operator_manual.py` y `test_cli_help_examples`; confirmar CHANGELOG. Sin ejecutar nada.

## FUTURO
La decisión de fondo sobre split (opciones a/b/c) queda en el drawer y no se promueve hasta cerrar la ola; el coordinador puede revisar la opción c. Otro nodo/humano decidirá promoción, commit/PR y validación CI.
