# Round 05 — Repo register edge cases

**Source:** round-05-subagent-01

## No path validation

`deskops repo register myrepo /nonexistent/path` → exit 0, registra un repo cuyo path no existe. Sin warning.

## No path scope validation

`deskops repo register myrepo-etc /etc` → exit 0. Acepta `/etc`, `/tmp`, cualquier path del sistema.

## Duplicate: file overwritten before store check

`deskops repo register myrepo .` repetido → exit 1, pero el archivo `.md` en `desk/registry/` ya fue sobrescrito. Inconsistencia: file on disk != store index.

## init + repo register gap

`deskops init /tmp/test && cd /tmp/test && deskops repo register local-test .` → `Error: RepositoryDoc model is not registered in the store.`

`init` no registra modelos en el local store. `bootstrap` sí, pero solo en global store (~/.sldb).

## Path sí existe como archivo

`deskops repo register test /tmp/test-file` (file, not dir) → exit 0, sin error. Path validation inexistente.

## Duplicate slug collision

`"my repo"` y `"My Repo"` slugifican a `my-repo`. El segundo overwrites silenciosamente.

## Empty name → Pydantic traceback

`deskops repo register "" /tmp` → `Unexpected: 1 validation error for RepositoryDoc ... Field required`

## --pythonpath aceptado pero no persistido

Flag aceptado, usado para runtime resolution pero no guardado en el archivo markdown.
