# WS12, resultado para checkpoint root

Claude Opus 5.5, pane `w3Y:p1`, 2026-11-01. Nada ejecutado en runtime. No es aprobación de nadie. `G_WRITE_CONTRACT` sigue pending. Contrato en estado borrador.

- `contratos/operaciones.md` sha256 `fa965612dae6d0d76c40c802fcace7b5ad46e472ddfa5bfd977d9206085ee085`
- Primer congelado `92ed7ed6`; correcciones `3dcefa4f` y `fa24ec7a`; `patch-correcciones.diff` sha256 `555eeebc5d96a15e11df3efa97f192df56cf9474a670a3bda048b22f816c6415`.

## Contenido

Matriz de 65 filas: COMP 38, LEC 13, NOAC 6, HUE 8. Las 96 hojas de `command_registry()` mapeadas en 2.7. Conteos del Executor, no recontados por mí.

Representación de precondición elegida: before-image por valor, `expected` y 409, en `changes[]` de `POST /save`. El token `version` se publica y ningún escritor lo consume; pron tiene su guarda `hash_c`, interna. Sin precondición compartida: P03 no cambia.

«Modo manual exclusivo», §5: afirmación del responsable fuera de la petición y ausencia de evidencia contraria en cada escritura. Sin evidencia, lectura y handoff. Mecanismo: HO-03, sin productor.

## Evidencia y sus bytes

| Revisión | Bytes | Resultado |
|---|---|---|
| Tres Testers completos, sin solape, secciones 1-13 | `f91227ec` | FAIL los tres, `renovacion-1/` |
| Los mismos, repetidos | `6a58a2f2` | B (§5-§9) PASS; A y C FAIL, `renovacion-2/` |
| Tester focal de lo corregido y de 10.2 | final | PASS |

**A (§1-§4) y C (§10-§13) no tienen un PASS completo sobre bytes finales**: tienen su ronda completa con FAIL acotados y el focal que los resuelve. El focal no reabrió el resto de la sección 2. Tester deepseek-flash sin shell ni git.

**Mi lectura:** §1 y §5-§7 completas, y comprobaciones directas de `expected`, `version`, `workers`, `Origin`, `.deskops.log`, `serve.py`. **No leí completas §2-§4 ni §8-§13.** El Executor dijo haber corregido «único timeout» y seguía en §4.1: lo encontró el Tester.

**No hice revisión fresca de consumidor de este contrato.** Tu orden no la pide para WS12 y los consumidores deben traerlo enlazado.

`status` da todas vigentes y no hubo staleness: el contrato no es fuente de bundles y `dag.yaml` no cambió. Eso no certifica el contrato.

## Para root

Decisiones técnicas sin productor, asignadas como huecos:

1. HO-05: baja de RelationDoc; sldb borra el archivo y graph_ui local solo destrackea.
2. HO-07: ningún canal reúne precondición y guarda contra borrar contenido no declarado.
3. HO-11: la captura a drawer no cumple con prueba real en ninguna de las cinco opciones; por defecto, no disponible. Falta el productor Deskops explícito antes de WS25.2 que prevé el DAG.

También sin productor: HO-03, HO-04, HO-06, HO-09, HO-10, HO-11b, HO-12, HO-15, HO-18. HO-19 lo fija una corrección documental al preparar WS34.1 y WS34.2. HO-17 depende del inventario WS05, ausente.

Hallazgos de código, sin tocar: guarda de `Origin` solo si llega el header, y ausente en la rama remota de `/api/save` (HO-15); `atoms validate` con `mutates=False` escribe andamiaje; `show task` y `advance task` pueden migrar el store; `.deskops.log` versionado en sldb y spec2viz.

Sin productor no se habilita nada. Código UI, SLDB y ramal Scion esperan tu revisión.
