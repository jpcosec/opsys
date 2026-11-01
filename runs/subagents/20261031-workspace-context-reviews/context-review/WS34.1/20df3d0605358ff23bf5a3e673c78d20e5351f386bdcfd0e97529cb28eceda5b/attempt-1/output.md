REFORMULACION
Propósito: que deskops exponga un adaptador público restringido para dispatch a Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: capacidad de dispatch autorizado, sin shell arbitrario ni transporte duplicado, evidenciada por un dispatch aceptado y otro rechazado/vencido, correlacionados con el intento local WS32.1 y registros WS32.2. Repo dueño: deskops (`output_base: deskops:repository_root/`). Límites: solo dispatch; no fija umbral propio de timeout ni sustituye el contrato WS12; no ejecuta en planificación; los gates y el contrato pendientes condicionan el avance.

AMBIGUEDADES
Ninguna.

DRY-RUN
Lecturas: nodo y aristas en `dag.yaml`; brief, alcance y decisiones; `contratos/operaciones.md` de WS12, sección de dispatch/timeout; salidas WS33.1/WS33.2 y referencias WS32.1/WS32.2; `auditoria/scion-probe.md` de WS44; autorización G_EXEC.
Cambios previstos: módulo adaptador en `runtime/` o la API que fije WS12; comando en `cli/commands/runtime.py`; pruebas en `tests/`. El ejecutor validaría autoridad del coordinador, usaría/crearía el id de intento local, llamaría al transporte público existente, clasificaría aceptado/rechazado/vencido y solo marcaría `confirmed` con respuesta observada, sin umbral propio.
Dependencias: G_SCION, G_EXEC y G_WRITE_CONTRACT por delta; contrato WS12; identidad/registros WS32.
Validaciones futuras: agente real con dispatch aceptado y negativo; correlación con WS32.1/WS32.2; ausencia de shell y de transporte duplicado; prueba de timeout con la política de WS12.
Errores: si falta la política de timeout o un gate, detenerse y registrar el hueco; no inventar umbral ni convertir ausencia de confirmación en éxito o fallo remoto.

FUTURO
WS44 produce el probe y G_SCION; WS12 fija la política/umbral de timeout y el recibo G_WRITE_CONTRACT por delta; el humano/designee otorga G_EXEC; WS32.1/WS32.2 aportan identidad y registros; WS34.2 consume el dispatch para reply. Nada de esto es ambigüedad del nodo.
