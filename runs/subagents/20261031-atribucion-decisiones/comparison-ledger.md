# Ledger de comparación — corrección de procedencia en decisiones.md

Fecha: 2026-10-31. Rol: Supervisor. Actor: Claude Opus 5.5, pane `w3Y:p1`. Revisores: `pi` por `context_review.py`, procesos aislados, instrucción `v2-ejecucion-hipotetica`.

## Qué se corrió

- Entrada: `decisiones.md` en `f76c2586`; cambia el bundle de los 73 nodos. Contratos sin cambio.
- `context_review.py run --stale --jobs 6`: 73 `ok`, `review-run.log`.
- Reintentos con `--new-attempt --reason`: WS12, WS13, WS42, `review-run-retries.log`. Mismo input.
- Vigentes: 70 `attempt-1` y 3 `attempt-2`, los 73 con recibo completo, manifest v2 e `input_sha256` igual al bundle. Lista: `final-attempts.json`.

## Qué leí exactamente

Leí `output.md` completo de los 73 y, para cada nodo: title, scope, acceptance, depends_on, requires, output_scope, output_base y children. Son 11 lotes y los tres reintentos.

No leí los bundles completos, `reconciliation`, `promotion`, ni los TaskDoc generados. Para WS19.1, WS12, WS08, WS09, WS13.2, WS13.3, WS11 y WS16 abrí además la ambigüedad y la disposición del intento anterior, recortadas a 700 y 600 caracteres. No hubo agente preparatorio: las 73 `disposition.md` las generó un script mío con las clases y notas que escribí tras leer.

Comprobado por programa: las cuatro secciones en cada output; y que cada ambigüedad numerada tiene una clase. Esa comprobación solo cuenta ítems: la clase es juicio mío.

## Resultado

| Dato | Valor |
|---|---|
| Ambigüedades listadas en intentos vigentes | 52 |
| `detalle de promoción` | 30 |
| `no es ambigüedad` | 17 |
| `futuro asignado` | 5 |
| Ambigüedades reales | 0 |
| Intentos rechazados por mí | 3 |

Rechazados:

- WS12 attempt-1: FUTURO «WS34.1/34.2 fijan su timeout», contra «no WS34» del contrato.
- WS13 attempt-1: transferencia WS13.2→WS13.3 sin arista.
- WS42 attempt-1: sin sección FUTURO. El helper no lo detectó, porque su recibo solo prueba la ejecución.

Ninguno de los 73 outputs menciona `T-Pxx`, «Procedencia técnica» ni «Técnica derivada». La separación no generó ambigüedad nueva, y eso también significa que los outputs no prueban que los revisores la hayan usado.

## Hallazgo que parecía regresión

WS19.1 levantó «modo manual exclusivo», sin antecedente en el intento previo. La frase está solo en la tabla inicial `35543965` y en `dag.yaml:1327`; ya faltaba en `decisiones.md` antes de esta corrección. No la causó el parche. Disposición: P03 más la «policy coordinador» de WS12.

## Límites

- Las clases son juicio del Supervisor; el Tester las revisa por muestra.
- Imprecisiones aceptadas sin intento nuevo, cada una en su disposición: WS24 y WS37 llaman «de planificación» al encargo; WS32.1 y WS33.2 mencionan recibos humanos en deltas deskops, donde WS12 fija que no hay recepción nueva; WS13.3 menciona a WS13.2 en FUTURO; WS15 dice no revisar hijos aunque recorre sus salidas.
- Citas a `dag.yaml` por número de línea en `decisiones.md`: siguen correctas tras registrar, pero se moverán con cualquier edición futura del DAG.

## Para la promoción

Sin cambio de contrato ahora:

- WS36: `output_scope` solo nombra la ruta a WS34; el scope pide también registrar con WS33.2.
- WS24: `output_scope` no nombra ruta backend si la API de grafo la requiere.
- WS22: selección y enlaces comunes pueden vivir fuera de `board/`.
- WS13.3: conducta al cerrar pestañas, activa o no, con historia.
- WS35: sigue vigente la clasificación del cierre anterior.
