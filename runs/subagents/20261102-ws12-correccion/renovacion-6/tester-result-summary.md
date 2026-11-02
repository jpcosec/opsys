No ejecuté pruebas ni comandos.

## Separación de fuentes

**LECTURA PROPIA** (archivos abiertos): `review-source-3.md`, ambos diffs, `operaciones.md`, `dag.yaml`, `closeout_gates.py`, `desk_paths.py`, `operations.py`, `cli/commands/operations.py`, `tests/test_cli.py`.

**DATO DEL SUPERVISOR** (`tester-d-facts.log`, no verificado por mí): `HEAD deskops: 66714cf1`; `sha256 operaciones.md: b96b909d…e93f`; `sha256 dag.yaml: 3e68ae20…0c5a`.

## Cotejo

| Objeto | Evidencia real | Veredicto |
|---|---|---|
| §4.4 dos recorridos; no rastreado sin HTTP ni «aplicado»; sin stale para CLI | `operaciones.md:298-312`; `dag.yaml:1814-1841` | PASS |
| W02 no queda como escritura de la UI | `operaciones.md:96` («No es un canal de escritura de la UI»), `operaciones.md:270` (handoff que la UI no ejecuta) | PASS |
| `closeout_evidence`: excepción solo drawer; W03 no completo; protegidos | `operaciones.md:222`, `operaciones.md:302`, `operaciones.md:308`, `operaciones.md:97` | PASS |
| `normalize_declared_evidence` existe y es de módulo | `deskops/services/closeout_gates.py:23`, `:54`, `:77`; sin `__all__`; sin uso en `tests/` | PASS |
| Pills: lista entera, conservación, validación, sin bind, sin merge | `operaciones.md:310`, `operaciones.md:225`, `dag.yaml:1814-1832` | PASS |
| `show task` solo busca en `desk/tasks` | `operations.py:412-419` → `:1073-1074` → `:1028-1032` → `:1125-1126` | PASS |
| Selector: nombre/prefijo, sin flag de ruta, comprobación previa, sin comando si falla | `desk_paths.py:26-62`; `operations.py:1138-1161`, `:1235-1245`; `cli/commands/operations.py:60-63`; `operaciones.md:306` | PASS |
| Prueba de selector idéntico y prefijo: exigida y no existente aún | `operaciones.md:306`; `tests/test_cli.py:1450-1460` solo cubre nombre idéntico | PASS |
| `G_PAYLOAD_PRECONDITION` en WS26 con razón; no a handoff/W01; WS47 en WS26.1; sin ciclo | `operaciones.md:54`, `:270-271`, `:636-638`; `dag.yaml:1766`, `:1808`, `:1814` | PASS |
| WS47: detecta, no detecta, deshabilitado; residuo no aprueba pérdida conocida | `operaciones.md:451-454`; `dag.yaml:3046-3064` | PASS |
| Gemelas sin «root debe decidir» ni «ambigüedad abierta»; creación/promoción en WS26.2 | `operaciones.md:537`, `:270-271`, `:363`, `:637-638`, `:697-698`, `:776`; búsqueda sin coincidencias en contrato/DAG | PASS |

## FAIL

Ninguno.

## Cobertura exacta

- `operaciones.md`: §1.5 (`:54`), W02 (`:96`), W03 (`:97`), filas `closeout_evidence`/`from_drawer`/campos/pills/PillDoc (`:222-230`), whitelist (`:250`), §4.2 filas preparar/crear (`:270-271`), §4.4 (`:298-312`), §5.7 (`:361-363`), §6.3 (`:408`), §6.2 WS47 (`:454`), §9.3 promoción (`:537`), §10.2 WS26/WS26.1/WS26.2 (`:636-638`), HO-01/HO-02 (`:697-698`), §13.3 (`:776`).
- `dag.yaml`: `revision_note` (`:3`), `requires` de WS26 (`:1766`), scope/acceptance de WS26.1 (`:1814-1841`), acceptance de WS47 (`:3046-3064`).
- Código abierto: `closeout_gates.py:23,54,77`; `desk_paths.py:26-62`; `operations.py:271-282,412-419,1028-1032,1073-1074,1118-1126,1138-1161,1235-1245`; `cli/commands/operations.py:60-63,126-133`; `tests/test_cli.py:1450-1460`.

RESULTADO: PASS
