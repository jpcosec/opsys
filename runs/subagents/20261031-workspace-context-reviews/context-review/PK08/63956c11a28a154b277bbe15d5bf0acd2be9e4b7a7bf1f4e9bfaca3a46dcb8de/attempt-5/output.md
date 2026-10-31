## REFORMULACION
Propósito: revisar PK08 como encargo de planificación, no como entrega de producto. Resultado esperado: determinar si la agrupación de revisión del ramal Scion está definida de forma comprobable. Repo: PK08 no declara `owner_repo`; su aceptación invoca un comando ejecutado «desde la raíz de deskops», por lo que el control se ejerce en deskops. Límites: no se revisan los bloques edge vecinos; no se ejecuta `context_review.py`; no se resuelven Pxx, gates ni méritos del producto; no se evalúan los hijos.

## AMBIGUEDADES
1. Contradicción sobre el efecto de un bloqueo explícito. Cita: «sin ambigüedad de encargo o bloqueo explícito con responsable». Cita: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera». Obliga a inventar si un hijo explícitamente `blocked`, con responsable y dependencia, permite que PK08 sea verdadera o, por el contrario, la impide.
2. Actor no identificado para registrar el bloqueo. Cita: «que el coordinador registra con responsable y dependencia en esa disposition.md». No se define quién es el coordinador ni en qué repo actúa; obliga a inventar la identidad o autoridad que validaría un `blocked`.

## DRY-RUN
Lecturas previstas: guía de revisión, brief, alcance, decisiones, cobertura, bloque PK08 y bloques edge de sus hijos como contratos de vecinos. Cambios previstos: ninguno; solo el informe de revisión. Dependencias: revisiones vigentes de WS32–WS38 y WS44, coincidencia de hashes de input y contrato, `disposition.md` guardada en cada intento, y el comando de estado desde la raíz de deskops. Validaciones futuras, sin ejecutar: correr `python desk/drawer/plans/workspace-documental/context_review.py status`; comprobar los ocho hijos directos; verificar hashes y disposiciones; comprobar que todo `blocked` tenga responsable y dependencia registrados.

## FUTURO
Cada context review hija produce su `disposition.md`; WS07 designa al operador Scion; WS05 produce el inventario; WS44 produce o no el recibo de G_SCION; el coordinador registra bloqueos; el humano resuelve las Pxx. Nada de eso se decide en PK08 ni se suple aquí.
