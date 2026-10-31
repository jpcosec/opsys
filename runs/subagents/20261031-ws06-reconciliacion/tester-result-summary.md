# Informe Tester WS06 — verificación de la corrección documental

Alcance: lectura estática. No se ejecutó hash, git ni validadores; el sha256 y los conteos del Supervisor se tratan como dato externo.

| Objeto | Evidencia real leída | Veredicto |
|---|---|---|
| 1. C-50 limitada a portabilidad, sin negar `POST /api/views/save`, remite a C-37 | `reconciliacion.md`, fila C-50: «El ViewDoc ya se crea y evalúa dentro de graph_ui (`views_routes.py:56-82`, `POST /api/views/save`; ver C-37)»; límites: «Limitada a portabilidad/independencia del host; no repite creación, evaluación local ni guardado de C-37». Código real: `views_routes.py` `def save_view(...)` y rama `POST /api/views/save` en `dispatch` | PASS |
| 2. C-64 nuevo delta, destino al candidato del drawer, conserva WS32/33, no exige WS05 | Fila C-64: clasificación «nuevo delta»; destino `desk/drawer/tasks/task-correlacionar-intentos-scion-con-rundoc-y-closeout.md`; «descomposición WS32/WS32.1/WS32.2 ya registrada»; «no se requiere WS05». El archivo destino existe y declara estado «candidato… No promovido». `dag.yaml` WS06 (líneas 482-483) repite «descomposición en WS32/33 sin requerir WS05». Hallazgo: WS32.1 y WS32.2 sí tienen `depends_on: WS05` (líneas 2063, 2107, 2156) | PASS con hallazgo |
| 3. C-28 declara en límites que doctor y drift amplían el ticket de Changes | Fila C-28, límites: «`doctor` y `drift check` amplían lo que nombra el ticket de Changes, que menciona `stores check` y el grafo». Ticket real: Scope dice «stores check + grafo de referencias»; `grep` de `doctor`/`drift` sin resultados en el ticket | PASS |
| 4. Ajuste 1 no niega que WS20 pida revisión; sitúa el vacío en el CAS de payload por campos | `canonical-adjustments.md` §1: «WS20 ya exige «revisión» y pruebas de conflicto, pero para raw-source (dag.yaml:1331-1339); el vacío es el CAS de guardado de payload por campos, no raw-source». `dag.yaml` WS20: scope «guarda por API pública con revisión»; acceptance «tests de roundtrip, conflicto, recuperación…» | PASS |
| 5. Conteo por clasificación y coherencia de cobertura/atomización | Conteo de filas leídas: ya cubierto 33 (graph_ui 11, sldb 8, spec2viz 2, deskops 12); nuevo delta 32 (graph_ui 23, sldb 2, spec2viz 1, deskops 6); extender ticket 2 (C-14, C-28); no adoptado 1 (C-29). Suma 68. Tabla de cobertura: WS18→C-37/48/49/50; WS29→C-06/28/29/46/61; WS32/32.1/32.2→C-64; 63 filas de nodo. Atomización: C-14 y C-28 como extensiones; C-50 en spec2viz reutilizando C-37/C-49; C-55 y C-64 en deskops | PASS |

## Hallazgos

- **C-41 (residual)**: la fila sigue diciendo «WS20 solo nombra raw-source», lo que contradice el Ajuste 1 corregido y el scope real de WS20 («con revisión»). No afecta al conteo, pero es texto desalineado en la matriz.
- **WS05**: C-64 afirma «no se requiere WS05», pero `dag.yaml` mantiene `WS05` en `depends_on` de WS32.1 y WS32.2. La afirmación vale para clasificar el delta, no para el camino de los nodos.
- **Sin hallazgos** en C-50, C-28 ni Ajuste 1 frente a su texto actual.

## No verificado

- sha256 `7a85a581…` del documento: **NO VERIFICADO** (no hay herramienta de hash en esta pasada).
- sha256 `125b862b…` del candidato C-64: **NO VERIFICADO**.
- Comportamiento runtime de rutas y comandos: no ejecutado.

RESULTADO: PASS
