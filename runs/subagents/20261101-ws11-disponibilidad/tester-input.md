Eres un Tester independiente, en el directorio actual, raíz del repo deskops. Responde en español. Solo puedes leer. No ejecutaste nada: no lo afirmes ni declares haber probado comportamiento. No corrijas nada.

Separa LECTURA PROPIA de DATO DEL SUPERVISOR (runs/subagents/20261101-ws11-disponibilidad/tester-facts.log).

Lee runs/subagents/20261101-ws11-disponibilidad/review-source.md, runs/subagents/20261101-ws11-disponibilidad/patch.diff y en desk/drawer/plans/workspace-documental/contratos/navegacion.md las secciones 3.1, 3.2, 3.3, 5.2 (con su tabla), 5.3, 5.4, 8.2 a 8.6.

1. ¿El diff cambia una sola cadena de §3.2 Validación, con el texto exacto que root da?
2. Interacción §3.2/§8.5: ¿E-MD3 es alcanzable ahora? ¿Alias autorizado con recurso ausente da E-MD3 y no E-MD1? ¿Alias fuera del conjunto sigue dando E-MD1? ¿Se describe el mismo caso con dos errores? ¿La frase implica una comprobación de arranque permanente?
3. Sin creación, sin migración, sin fallback: ¿alguna frase de 3.1, 5.4, 8.3 u 8.4 contradice «antes de abrir el store»? Ojo con open_store (../sldb/src/sldb/api/stores/open_store.py:37-38): ¿el orden del contrato evita migrar en este caso?
4. No regresión de aliases: unicidad por (root.resolve(), store.resolve()), alias canónico, local reservado y fuera del conjunto, ausencia del parámetro, ?alias=local da E-MD1, sin configuración no hay lectura cruzada, clave de sesión. ¿Algo se contradice?

Informe: tabla con objeto, fuente, evidencia real archivo:línea, PASS o FAIL; qué no pudiste verificar. Última línea exacta `RESULTADO: PASS` o `RESULTADO: FAIL`.
