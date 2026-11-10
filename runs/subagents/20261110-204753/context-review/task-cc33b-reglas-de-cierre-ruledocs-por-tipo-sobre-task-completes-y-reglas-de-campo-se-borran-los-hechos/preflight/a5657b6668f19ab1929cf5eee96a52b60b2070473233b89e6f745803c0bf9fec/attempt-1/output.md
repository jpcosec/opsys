REFORMULACION
Encargo ejecutable (task.code, no agregado): en deskops, sustituir el cierre por hechos por reglas declarativas —RuleDoc semilla por tipo `on_transition` sobre `task_completes` (`where current_node = "ritual-testing"`) que exige los recibos evidence de CC33a; reglas de campo como RuleDoc alert; borrar `__closeout_evidence__`, `closeout_evidence_verified`, `pill_graduation_verified` y `_add_closeout_facts`; portar los chequeos CC38 borrando su función vieja—. Resultado: cierre bloqueado sin recibo commit accepted, grep vacío, tests/goldens/doctor, docs y CHANGELOG. Límites: no grafo (CC33c), selectores/escrituras ni tags por API sldb (DO7); nada a mano en `desk/`; no Python supliendo reglas; goldens intactos; tests de a uno.

AMBIGUEDADES
1. "los 9 chequeos de CC38" frente a b1: "8 filas: 3, 5, 13, 14, 15, 18, 24 y 25" y "no hay que buscar un noveno". Obliga a inventar un noveno o incumplir la aceptación.
2. "RuleDoc semilla on_transition sobre la arista task_completes (where current_node = "ritual-testing")": no fija campos, nombre ni cómo se liga al `task_type`. Obliga a inventar esquema y asociación.
3. "el tipo pasa a leer sus kinds de la RuleDoc o de una tabla de datos": alternativa sin criterio. Obliga a elegir e inventar tabla/mapeo.
4. "se borran los hechos y gates viejos" (título): no enumera gates; el cuerpo solo nombra hechos. Obliga a inventar cuáles gates.
5. "la regla de evidencia (DA5)": DA5 no se define. Obliga a inventar su contenido.
6. "goldens idénticos" frente a b8: "el worker para y avisa con el diff". Contradicción que obliga a decidir parar o ajustar.

DRY-RUN
Lecturas: contrato, a1-a8/b1-b9, informe CC38, `closure.py`, `task_types.py`, lifecycle, rules, goldens. Cambios previstos: semillas RuleDoc; quitar `has(closeout_evidence_verified)` de la arista; borrar hechos/código y añadir tests; portar los 8 checks (hipótesis para #3, #5, #13, #14, #18, #24; intentar #15/#25); docs/CHANGELOG/ritual. Dependencias: CC33a en main `6d133045`; CC33c sin integrar; lenguaje de reglas sldb; DO7/H1; review record goldens; comandos ~30 s. Validaciones futuras: grep vacío; `edges_blocked` con `fact = "commit"`; editar goal rebloquea; pytest por archivo; goldens; doctor en 6 desks; 4 pasos en clon limpio.

FUTURO
Deciden humano/coordinador: aceptar 8 y corregir el «9»; aprobar hipótesis y nota a sldb; aceptar o rechazar diff de golden; fijar la vía DO7/H1 para #5; correr suite completa y los 4 pasos; aceptar que #15/#25 queden como hipótesis si no se expresan.
