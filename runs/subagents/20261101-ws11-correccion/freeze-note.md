# Parche congelado de la corrección de WS11, para revisión root

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Commit `b4968374`. Nada ejecutado en runtime. No es aprobación de nadie.

- `contratos/navegacion.md` sha256 `37b4edbda2d1a0e37421753daa3f5c8f96aacb58558ba4720eed57abb1d6801f`
- `borradores/vistas.md` sha256 `9772e00ea24602681e9e01fda4e05de61df63574ce0342cb8b822ffca099bc24` (solo F18a, campo Renderer, línea 367)
- `patch.diff` sha256 `e2a199a255418afafebe2a7d7ab448e1b6d21b093fdaec402f0071fbd1c9c715`, diff `65f76c46..b4968374` de esas dos rutas
- Detalle y tabla de las 16 filas C y 27 filas H: `result-summary.md`. Autor del cotejo: Executor Sonnet. Yo leí contrato y diff completos; de las filas solo reabrí las cadenas de `doc_status` y `doc_ref`.

Estado de checks: build verde. `validate` y `status` dan **solo** `WS09: input changed`, esperado por `vistas.md`. No renové ni registré nada. Log: `freeze-validation.log`.

## Resolución

| Punto | Dónde | Resolución |
|---|---|---|
| Decisión 1 | §6, §6.1, §6.2 | WS13.1 no se reduce; foco interno distinto de navegación; dominio con procedencia real |
| Decisión 2 | §5.2, §8.4, H-16 | Composición en graph_ui, WS41; sldb no se amplía |
| Decisión 3 | §9, §12.3 | WS18 detenida, opcional, sin pregunta nueva |
| Decisión 4 | §3.2, §8.6, H-10, H-11 | Contrato del input; WS41 consume; WS40 instancia; registry designable |
| A | §2.2, §4, §6, H-03 a H-05b, H-21 | C1-C3 navegación; C4 pasiva; C5b, C6, C7, C8/C9, C11, C12, C14 y H-05b separados; mismo origen por lectura o revisión; steps con orden sin StepDoc |
| B | §3.3, §5.2, H-06 | Guardias generales y específicas separadas; autorizar antes de leer; `recover_links` no es resolutor |
| C | §3.1, §5.4, §8.3, §8.4, H-14 | Retirado «doc_status no escribe»; obligación y criterio observable; dueños store propio y segundo desk |
| D | §7.3, §7.5, H-09 | Status conservado en el wrapper, WS15.1; E7 muestra causa recibida |
| E | §10 | Regla 5; SpecDoc y manifiesto WS40 derivados |
| F | `vistas.md:367` | Base existente; integración sigue candidatura |
| Clave de sesión | §5.3 | Alias más identidad local, sin sintaxis de cadena |

## Corregido por mí sobre lo que entregó el Executor

`doc_status` llama por dentro a `split_doc_ref` (`doc_status.py:26`), y el paso 6 de §5.2 habría seguido enlaces de store no autorizados con cualquier destino con dos puntos. Ahora exige `"local:" + resto`, por lectura de `doc_ref.py:38-39`, sin ejecutar.

## Corregido por el Executor fuera de lo pedido

H-23, H-21, C5b, §8.3 y §4 (`compose_document` sí devuelve texto expandido; el IR entrega `surface`), más citas. Lista en `result-summary.md`.

## Puntos que el parche redactó y root no decidió

1. Alias de operador distinto de los nombres de enlace de store de sldb. El contrato no exige que coincidan.
2. `local` tratado como alias reservado, por `doc_ref.py:18,38-39`.
3. Prefijo no autorizado en un enlace de texto: destino local y, si no resuelve, E5, no E-MD1.
4. H-11 no encaja en las cinco clases; la fila lo dice, sin clase nueva.
5. `vistas.md:375` (Evidencia de F18a) no lista las citas nuevas; no lo edité porque root pidió solo la celda necesaria.

## Pendiente tras tu revisión

Tester sobre los puntos corregidos completos, por lectura. Revisión fresca no ejecutora con WS13.1 o WS41 como consumidor. Renovar WS09 y su puntero en DAG. Closeout. No cerré fase, WS12, UI, Scion ni push.
