## REFORMULACION
Propósito: inventariar, sin mutar nada, las superficies y operaciones de Deskops: archivos de las categorías enumeradas, comandos CLI públicos, métodos de `DeskopsOperations` y modelos registrados, distinguiendo modelado de Markdown no modelado.

Resultado: `auditoria/deskops.md`, con una fila por superficie, ubicación, operación expuesta y estado comprobado.

Repo dueño: `deskops`.

Límites: solo lectura; no inferir modelo por carpeta; marcar «no comprobado» con causa; no implementar ni corregir. `WS01` es dependencia declarada; su contrato no se revisa aquí.

## AMBIGUEDADES
1. «una fila por superficie» / «la operación expuesta (comando o método que la lee o muta, o «dato pasivo»)». Una misma superficie puede ser leída y mutada por varios comandos o métodos. El ejecutor debe inventar si agrupa varias operaciones en una fila, duplica filas —contradiciendo «una fila por superficie»— o elige una.
2. «cada archivo, comando público o modelo registrado concreto de las categorías enumeradas». No queda claro si «de las categorías enumeradas» limita solo a los archivos o también a comandos y modelos, ni si «cada archivo» abarca todo el repo `deskops` o solo esas categorías. Obliga a inventar el universo inventariable y, con ello, la completitud.
3. «estado comprobado = lectura citada con archivo:línea o salida de comando de solo lectura». Para directorios, binarios, modelos del store o datos pasivos, «archivo:línea» no aplica; no define si la evidencia es existencia, contenido, hash o permisos. El ejecutor debe inventar el criterio.
4. «Modelado = tiene modelo registrado en el store (`sldb models list`)». No identifica store, desk ni ruta. El ejecutor debe inventar contra qué store ejecutar o cómo decidir «modelado».

## DRY-RUN
Lecturas previstas: brief, alcance, decisiones, cobertura; repo `deskops`; ayuda CLI; código de `DeskopsOperations`; `sldb models list`. Cambios previstos: solo `auditoria/deskops.md`. Dependencias: `WS01`, store SLDB accesible, repo `deskops`. Validaciones futuras: cada fila con ubicación, operación y estado; ausencia de inferencia por carpeta; «no comprobado» con causa; que no haya mutaciones ni salida de alcance.

## FUTURO
`WS06` y `WS10` consumen la auditoría; `WS10` la recibe también de forma transitiva. La promoción fijará columnas, archivos exactos y TaskDoc. Un humano o receptor valida la aceptación; si falta el store, se registra el hueco y no se crea sustituto.
