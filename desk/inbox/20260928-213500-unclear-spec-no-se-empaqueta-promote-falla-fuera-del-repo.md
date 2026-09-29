---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-09-28T21:35:00'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# spec/ no se empaqueta: promote falla con "Missing required field: artifact.task" fuera del repo

_Describe the incoming message with enough evidence to triage._

Reportado desde sldb. Dos hallazgos que bloquean `deskops promote` fuera del
repo de deskops.

## 1. El paquete instalado no incluye `spec/`

`operations.py:328` resuelve:

```python
self.spec_root = Path(__file__).resolve().parents[1] / "spec"
```

Eso funciona en el repo (`tools/deskops/spec/`), pero el paquete instalado en
site-packages NO trae ese directorio:

```
$ ls /home/jp/anaconda3/lib/python3.13/site-packages/spec/artifacts/
(no existe)

$ ls /home/jp/proyectos/hum-ecosystem/tools/deskops/spec/artifacts/
atom.yaml board.yaml faq.yaml inbox_note.yaml materialization.yaml
pill.yaml repository.yaml ritual.yaml step.yaml task.yaml
```

Sintoma: CUALQUIER `deskops promote drawer-task-to-active-task` desde otro repo
falla con

```
Missing required field: 'artifact.task'
```

El mensaje es enganoso: parece un payload incompleto del usuario, pero viene de
`specs/compiler.py:34` -> `registry.artifacts["artifact.task"]` levantando
KeyError sobre un registry vacio, capturado por el `except KeyError` generico de
`cli/main.py:379`.

Workaround aplicado en esta maquina (NO es fix):
```
ln -s /home/jp/proyectos/hum-ecosystem/tools/deskops/spec \
      /home/jp/anaconda3/lib/python3.13/site-packages/spec
```

Fix sugerido: empaquetar `spec/` como package data y resolver `spec_root`
relativo al paquete (`importlib.resources`), no a `parents[1]`. Secundario:
que un registry vacio de un error propio ("spec directory not found at X") en
vez de KeyError generico.

## 2. El repo tiene un CLI mas viejo que el instalado

Con `PYTHONPATH` apuntando al repo:

```
$ PYTHONPATH=tools/deskops python -m deskops.cli.main promote drawer-task-to-active-task ...
deskops promote: error: argument promote_command: invalid choice:
'drawer-task-to-active-task' (choose from inbox-to-drawer-task)
```

El instalado soporta ambos subcomandos; el repo solo `inbox-to-drawer-task`.
O el repo esta atrasado respecto a lo publicado, o se publico desde otra rama.
Vale la pena confirmar cual es la fuente de verdad.

## 3. Menor: `--from-yaml` de promote parece ignorarse

`deskops promote drawer-task-to-active-task <sel> --from-yaml payload.json`
creo el bundle pero con el contenido heredado del drawer, no con el payload
(probado con el payload plano y anidado bajo `task:`). `--title` si se aplico.
Los campos multilinea hubo que escribirlos aparte. Puede ser uso incorrecto de
mi lado; si es asi, un ejemplo en el help ayudaria.
