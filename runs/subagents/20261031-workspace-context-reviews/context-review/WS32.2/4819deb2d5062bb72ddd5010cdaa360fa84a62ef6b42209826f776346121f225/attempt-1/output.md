REFORMULACION
Propósito: hacer idempotentes manifiesto, RunDoc y cierre sobre el intento correcto, identificado por id de intento, no por agente ni slug. Resultado: registros canónicos consistentes que no duplican identidad ni evidencia al repetir una finalización. Repo dueño: deskops. Límites: solo `deskops/runtime/scion.py`, `models/run.py`, `services/closure.py` y `tests/`; sin segundo pipeline ni sustituir la API pública de Scion. Depende de WS05, WS12, WS32.1 y de G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT.

AMBIGUEDADES
1. «Una finalización repetida sobre el mismo id de intento conserva identidad y evidencia sin crear registros nuevos»: no define qué hacer si la repetición trae hash de sesión o evidencia distintos. Obliga a inventar si se rechaza, se conserva el primer registro o se actualiza.
2. «hash de sesión»: no indica qué sesión, quién lo produce ni cómo se verifica; la aceptación exige que manifiesto, RunDoc y cierre coincidan en él. Obliga a inventar fuente y cálculo.
3. «según el ticket de external_references.scion»: el contenido del ticket no se suministra y solo se listan campos mínimos. Si el ticket exige más campos o reglas, el ejecutor debe inventarlos; no se nombra quién lo produce ni qué hacer si falta.

DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodo y gates en `dag.yaml`; ticket `external_references.scion`; `auditoria/scion.md` (WS05); `contratos/operaciones.md` (WS12); salidas de WS32.1; plantilla RunDoc y código actual de deskops.
Cambios previstos: solo los archivos de `output_scope`.
Dependencias: WS05 aporta inventario; WS12 contrato de escritura; WS32.1 separa intento/dispatch. Gates pendientes son intencionales.
Validaciones futuras: pruebas de finalización repetida, dos intentos del mismo agente, dispatch fallido, coincidencia manifiesto/RunDoc/cierre y ausencia de registros nuevos; preflight y TaskDoc de promoción quedan fuera de este nodo.

FUTURO
WS07 designa operador Scion; WS44 produce G_SCION; WS12 produce G_WRITE_CONTRACT; un resolver externo estabiliza G_CLOSEOUT; WS32.1 fija identidad de intento; WS32 agrega el cierre de sus hijos. El TaskDoc de promoción fijará archivos, pruebas y textos; el humano resolverá Pxx y la aceptación de graph_ui.
