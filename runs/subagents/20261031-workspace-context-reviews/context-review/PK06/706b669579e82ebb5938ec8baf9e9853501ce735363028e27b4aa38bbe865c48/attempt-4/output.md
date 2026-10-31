## REFORMULACION

PK06 es una agrupación de revisión, no una tarea ejecutable ni una dependencia operativa. Su propósito es certificar que WS31 y WS43 tienen `context_review` vigente —hash de input y contrato actuales, con `disposition.md` guardada en su intento— o un bloqueo explícito con responsable. El resultado es el estado de PK06, comprobable con `context_review.py status`. No declara `owner_repo` propio; el comando se ejecuta desde la raíz de deskops. Límites: no revisa los bloques edge de sus vecinos, no ejecuta hijos, no valida calidad de producto y no resuelve propuestas Pxx.

## AMBIGUEDADES

1. **Contradicción sobre el efecto de un hijo bloqueado.** Cita: «Verdadera cuando cada hijo directo tiene revisión vigente sin ambigüedad de encargo o bloqueo explícito con responsable». Frente a: «Un hijo con ambigüedad sin resolver queda pending o blocked, y entonces esta aceptación no es verdadera». Obliga a decidir si un hijo `blocked` con responsable permite cumplir PK06 o si, por el contrario, lo impide; ambas frases admiten lecturas opuestas.

2. **Actor del registro de bloqueo no identificado.** Cita: «que el coordinador registra con responsable y dependencia en esa disposition.md». El input no nombra a ese coordinador ni indica cómo designarlo. Si aparece un bloqueo, el ejecutor tendría que inventar quién lo registra y con qué legitimidad, pese a que la aceptación depende de ese registro.

## DRY-RUN

Lecturas previstas: guía de revisión, brief, alcance, decisiones, cobertura, borrador de manual y definiciones de PK06, WS31 y WS43 en `dag.yaml`.

Cambios previstos: ninguno sobre el plan ni sobre los hijos; solo la revisión y, si procede, la disposición de PK06.

Dependencias: estado de revisión de WS31 y WS43, sus hashes vigentes y la existencia de `disposition.md` en el intento correspondiente; la comprobación usa `python desk/drawer/plans/workspace-documental/context_review.py status` desde la raíz de deskops.

Validaciones futuras: ejecutar ese comando, contrastar que los hashes coinciden, verificar disposiciones guardadas y comprobar si los bloqueos explícitos cumplen el criterio finalmente aplicado. No se ejecuta nada ahora.

## FUTURO

Un humano o el coordinador debe designar quién registra bloqueos y aclarar si un hijo bloqueado con responsable satisface PK06. `context_review.py` produce el estado y la vigencia de hashes. Los revisores de WS31 y WS43 generan sus disposiciones. Las decisiones Pxx y los gates de producto corresponden a otros nodos, no a esta revisión.
