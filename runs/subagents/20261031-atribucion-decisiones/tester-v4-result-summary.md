## 1. Registro (8 nodos)

| Nodo | dag.yaml evidence ≡ final-attempts.json | carpeta con output/disposition/receipt | technical_failure | ruta contiene input_sha256 | Veredicto |
|---|---|---|---|---|---|
| WS07 | sí (dag.yaml:557 vs final-attempts WS07) | sí | false (WS07/.../attempt-1/receipt.json:31) | sí, y = `input_sha256` dag.yaml:558 | PASS |
| WS12 | sí (dag.yaml:775) | sí | false (receipt.json:31) | sí, = dag.yaml:776 | PASS |
| WS33.2 | sí (dag.yaml:2374) | sí | false (receipt.json:31) | sí, = dag.yaml:2375 | PASS |
| PK02 | sí (dag.yaml:3079) | sí | false (receipt.json:31) | sí | PASS |
| WS19 | sí (dag.yaml:1288) | sí | false (receipt.json:31) | sí | PASS |
| WS37 | sí (dag.yaml:2586) | sí | false (receipt.json:31) | sí | PASS |
| WS13 | sí (dag.yaml:826) | sí | false (receipt.json:31) | sí | PASS |
| WS26 | sí (dag.yaml:1758) | sí | false (receipt.json:31) | sí | PASS |

Extra: `manifest.json` de WS07 usa `instruction_version: v2-ejecucion-hipotetica` y hashea `decisiones.md` = `f2d4b58f…` y `context-review-guide.md` = `dec1766a…`, iguales a `root-focal-approval-20261101.md`.

## 2. Falsa aceptación (8 elegidos: PK07, WS04, WS10, WS12, WS15.1, WS18, WS22, WS24)

| Objeto | Evidencia real | Veredicto |
|---|---|---|
| PK07 amb.1 `futuro asignado` | WS31 "Publicar manual documental básico probado" (dag.yaml:2095-2100); PK07 hijos WS29←WS15,WS24 (dag.yaml:2015-2017), WS39←WS12,WS13 (dag.yaml:2634-2636), sin arista entre sí | PASS (no fuerza invención) |
| WS10 amb.1 `detalle` | dag.yaml:646-680; "bloqueado" definido en scope | PASS |
| WS12 amb.1-2 `futuro asignado` | decisiones.md:45 (T-P03.1); dag.yaml:723-796 | PASS (el límite está declarado en el propio ledger) |
| WS15.1 amb.1 `detalle` / amb.2 `no es ambigüedad` | disposition WS15.1 líneas 9-10; dag.yaml:1052-1070 | PASS |
| WS18 amb.1 `no es ambigüedad` | disposition WS18 línea 9; dag.yaml:1216-1218 | PASS |
| WS22 amb.1-2 `detalle` | output WS22 líneas "AMBIGUEDADES 1-2"; dag.yaml:1501-1506 (estados desde deskops, campo de modelo TaskDoc auditado WS02) | PASS |
| WS24 amb.1-2 `detalle` | disposition WS24 líneas 9-10; dag.yaml:1565-1572 | PASS |
| WS04 amb.1-3 `detalle` | disposition WS04 líneas 9-11; justificación "Nodo ya ejecutado y **aprobado por root**" | FAIL de atribución (ver §5) |

Ninguna de las ambigüedades clasificadas obliga por sí sola a inventar un resultado: todas se resuelven leyendo deskops/WS02/WS09/WS11 o quedan como límite declarado.

## 3. Rechazos

| Nodo | Defecto attempt-1 | ¿Real? | ¿Desapareció? | Evidencia |
|---|---|---|---|---|
| PK02 | G_PRODUCT/G_WRITE_POLICY "pendientes" | sí, dag.yaml:26 y 115 = `satisfied` | sí (attempt-2: "verificados") | PK02/.../attempt-1/output.md FUTURO |
| PK07 | capítulo 15 a WS39 | sí, manual = WS31 (dag.yaml:2095) | sí | attempt-2 FUTURO |
| WS16 | G_UI_READ requerido con `requires: []` | sí (dag.yaml:1138) | sí, attempt-2 ya no lo afirma | attempt-2 DRY-RUN |
| WS19 | precondición solo en WS19.1 | sí, WS19.2 también requiere G_PAYLOAD_PRECONDITION (dag.yaml:1351-1355) | sí ("lo propio en relations/") | attempt-2 DRY-RUN |
| WS33.2 | acta P01 en delta deskops | sí, WS12: "en deltas de deskops no se crea recepción nueva" (dag.yaml:723-796) | **no del todo**: attempt-2 FUTURO repite "el receptor humano emite acta por delta"; declarado en disposition y ledger | disposition WS33.2 |
| WS37 | "WS44 designa operador" | sí, decisiones.md:15/25 ("Scion se designa…", P01); G_SCION "operador a designar" (dag.yaml:66) | sí | attempt-2 FUTURO |

Attempt-1 no rechazados: WS13, WS15, WS25, WS27, PK04 no afirman transferencia entre hermanos sin arista (verificado contra dag.yaml:797-841, 1052-1093, 1652-1686, 1887-1928, 1212-1236/1488-1534/1565-1571).
Sí queda un defecto comparable **sin declarar**: WS26 (no está en esa lista, pero es agregado) dice "sus aristas WS12/WS22/**WS30**" (WS26/output.md DRY-RUN) cuando WS30 es dependiente (dag.yaml:2052-2064), no arista.

## 4. Aristas (comparación transferencia ↔ depends_on)

| Nodo | Transferencia afirmada | depends_on real | Veredicto |
|---|---|---|---|
| WS13 | 13.2 y 13.3 sin arista; ambos ←13.1 | dag.yaml:797-806, 892-895, 933-936 | PASS |
| WS15 | hijos ← WS13, sin arista entre sí | dag.yaml:1015-1021, 1052-1055, 1093-1096 | PASS |
| WS19 | ambos ← WS12; precondición también en 19.2 | dag.yaml:1258-1263, 1304-1307, 1348-1355 | PASS (attempt-2) |
| WS25 | hermanos sin arista, ambos ← WS12 | dag.yaml:1616-1622, 1652-1656, 1686-1690 | PASS |
| WS27 | 27.1 y 27.2 sin arista | dag.yaml:1852-1858, 1887-1891, 1928-1933 | PASS |
| WS26 | "sus aristas WS12/WS22/WS30"; 26.2 consume TaskDoc de 26.1 | dag.yaml:1728-1734; 26.2 ← WS12, WS22, WS26.1 (dag.yaml:1806-1812); **WS30 no es arista** | FAIL (frase falsa, no declarada) |

## 5. Atribución

Frases marcadas:
- `WS04/.../disposition.md:9-11` (y misma fórmula en WS01/WS02/WS03/WS06): "Nodo ya ejecutado y **aprobado por root**". La disposición declara haber leído solo id/rol/kind/repo/depends_on/requires/children + output.md; no hay artefacto que registre esa aprobación (auditoria/ui.md existe, aprobación de root no consta). Excede lo leído.
- `ws07-cobertura-efectiva.md`: "Respuestas literales 0-2 … Iguales a `owner-decisions.json`". `owner-decisions.json` no existe en el checkout (`find` vacío) → no verificable desde aquí.
- `comparison-ledger.md`: "`git diff 47b9e38b b2720ae2 -- dag.yaml` es vacío". No verificable; el `dag-diff.txt` local es otro par (post-registro) y solo cambia evidence/input_sha256.
- `ws07-cobertura-efectiva.md`: "dag.yaml solo cambia en evidencia" — coincide con `dag-diff.txt` (todos los hunks son `evidence`/`input_sha256`). PASS.
- Tabla de conteos: 24+10+7 = 41 (aritmética correcta); 73 entradas y 6 `attempt-2` en `final-attempts.json` (PK02, PK07, WS16, WS19, WS33.2, WS37) → 67+6 = 73. PASS en lo comprobable.
- "WS07 sin ambigüedad de actor": intento vigente dice "Ninguna" (output WS07 §AMBIGUEDADES). PASS.
- "WS33.2 repite … en FUTURO" y "PK02 dice WS09→WS12 con camino por WS11": ambas declaradas y correctas (WS11 depende de WS09 y WS08, dag.yaml:685-687).

## 6. Límites

- Visto: no hay activación de WS08-12 (todos `status: candidate`, `promotion: not_authorized`), ni UI, ni Scion, ni push en estos artefactos.
- **Sí hubo cambio de fuente desde la tanda anterior**: `decisiones.md` vigente tiene T-P03.1 y T-P01/T-P03 (decisiones.md:43-45); `decisiones-antes-7b045a6f.md` termina en línea 36. Líneas 1-22 idénticas byte a byte.
- Declarado: root exige "NO WS08–12/UI/Scion/push" (`root-decision-20261101.md`, punto final) y "sin cambio de contrato"; contratos/gates no cambian (dag.yaml:26/35/115 siguen `satisfied`).

## No pude verificar

- `owner-decisions.json` (ausente del checkout).
- Los 73 recibos: solo 8 revisados.
- Estado de git/HEAD, `context_review.py status`, builds y tests (solo declarados en `tester-v4-facts.log`).
- Conteo completo de clases 24/10/7 (las disposiciones de tandas 1 y 2 conviven en disco y no las filtré todas).

RESULTADO: FAIL
