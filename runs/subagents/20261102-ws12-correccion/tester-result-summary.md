## LECTURA PROPIA

| Objeto | Evidencia real archivo:línea | Veredicto |
|---|---|---|
| §4.4: una sola frase | patch-4.diff, hunk único @@ -297,7 +297,7 @@; solo cambia la línea «El caso se identifica…» (operaciones.md:300) | PASS |
| `local:` + ruta resuelve solo en ese store | doc_ref.py:33-35 (`name == LOCAL` → `(None, rest)`); doc_status.py:26-28 (`_lookup(store_path, …)`), :48-49 (solo `indexed_documents(store_path)`) | PASS |
| `matches_doc_ref` compara ruta relativa | doc_ref.py:45 (`ref in (name, path, f"{model}/{name}")`); path viene del índice guardado con `relative_to(root)` (ops.py:27, :74-76) | PASS |
| No contradice recorrido A ni B | operaciones.md:300 (fallo→no rastreado→B), :302 (rastreado→A); doc_status devuelve `missing`→interpretado como no rastreado | PASS |
| Efecto `open_store` declarado | open_store.py:37-38 (`migrate_store_layout`); operaciones.md:50 (MIG, cita `open_store.py:37-38`); §4.4 cita explícita «(1.4, MIG)» en :300 | PASS |

Observación: cita `doc_status.py:26-29` desplazada — `open_store` está en :25; el rango 26-29 cubre `split_doc_ref`/alias, no el open_store. Comportamiento descrito correcto.

## DATO DEL SUPERVISOR
- HEAD deskops `8c29b775`; sha256 operaciones.md `754546d6…ce9f39`.

RESULTADO: PASS
