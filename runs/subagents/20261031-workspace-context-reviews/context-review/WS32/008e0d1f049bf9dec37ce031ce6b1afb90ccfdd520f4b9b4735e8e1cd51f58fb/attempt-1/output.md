**REFORMULACION**
- **Propósito:** agrupar la unificación de identidad de intento y cierre Scion sin crear un segundo pipeline.
- **Resultado:** agregado de las salidas de WS32.1 y WS32.2; no ejecutable por sí mismo.
- **Repo dueño:** `deskops`.
- **Límites:** nodo `aggregate`; depende de WS05, WS12 y sus hijos; exige G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT; `promotion: not_authorized`; no autoriza ejecución ni modifica el pipeline Scion existente.

**AMBIGUEDADES**
Ninguna. La aceptación es comprobable por agregación: «se cumple cuando todos sus hijos cumplen su aceptación». El alcance y el resultado quedan delimitados por «Agregado: salidas de WS32.1, WS32.2» y por el carácter no ejecutable del nodo. Las referencias a gates pendientes son intencionales y no obligan a inventar.

**DRY-RUN**
- **Lecturas previstas:** definición de WS32, aceptación de WS32.1/WS32.2, estado de WS05/WS12 y gates G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.
- **Cambios previstos:** ninguno en WS32, por ser `aggregate` no ejecutable; sus hijos materializan los cambios.
- **Dependencias:** WS05 y WS12 como prerrequisitos; WS32.1 y WS32.2 como hijos que determinan el cierre del agregado.
- **Validaciones futuras:** aceptación individual de ambos hijos; contrato de operaciones de WS12; evidencia de closeout; probe público de Scion de WS44. Sin ejecutar nada.

**FUTURO**
WS32.1 y WS32.2 producen las salidas agregadas. WS05 aporta el inventario; WS12 produce G_WRITE_CONTRACT; WS44 produce G_SCION; el resolver externo aporta G_CLOSEOUT. Un humano designa el operador Scion en WS07 y decide cualquier promoción; este nodo no la autoriza.
