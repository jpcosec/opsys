## REFORMULACION
Propósito: inventariar las superficies y operaciones reales de Deskops para dejar una auditoría trazable. Resultado: `auditoria/deskops.md` con una fila por superficie (archivo, comando público o modelo registrado) y su operación expuesta, ubicación y estado comprobado. Repo dueño: `deskops`. Límites: solo las categorías enumeradas —modelos/Markdown no modelado; inbox/drawer/issues/FAQ/crossroads/pills/fases/rituales/registry/roles/runs; firmas públicas, efectos Git y cierre—; no inferir modelos por carpeta; lo no comprobado se marca con causa; no implementa ni modifica código. Depende de WS01.

## AMBIGUEDADES
Ninguna. La definición de superficie, las categorías, la aceptación comprobable y el repo están acotados; la falta de un contrato se rige por `alcance.md` y la promoción/TaskDoc queda fuera de este nodo.

## DRY-RUN
- Lecturas: `dag.yaml#node:WS02`, `brief.md` de WS01, código y comandos públicos de `deskops`; `sldb models list` y solo comandos de lectura.
- Cambios previstos: únicamente `auditoria/deskops.md` bajo `output_base`; una fila por superficie, sin tocar código.
- Dependencias: WS01; nodo `candidate`, sin ejecución autorizada (`promotion: not_authorized`).
- Validaciones futuras: comprobar cada fila con `archivo:línea` o salida de solo lectura; marcar «no comprobado» con causa; verificar que no se infiere modelo por carpeta.

## FUTURO
WS06 y WS10 consumirán la auditoría. WS07/WS11/WS12 designarán y aceptarán responsables por repo. La promoción humana producirá TaskDoc, preflight y evidencia; los gates y las propuestas Pxx no se resuelven aquí.
