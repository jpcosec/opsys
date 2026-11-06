REFORMULACION

Nodo ejecutable hoja (`task.refactor`), no agregado. Propósito: sacar de `workspace.py` las plantillas del desk y convertirlas en datos del paquete (`deskops/data/templates/` + `desk_declaration.yaml`), que deskops renderiza en proceso y pasa a `sldb.api.scaffold_store`; `desk update` usará includes declarados en vez de adivinar modelos. Resultado: `init` y `desk update --apply` idénticos al golden, código viejo borrado, pruebas y CHANGELOG. Repo: deskops. Límites: no subir sldb ni el pin; no tocar semillas managed de CC31/CC32/CC34; conservar `inspect_desk`, `migrate_desk` y clasificación; no cambiar formato del desk ni gramática CLI; no escribir desks reales ni en sldb.

AMBIGUEDADES

1. Cita: «Se borran scaffold_desk, _write_if_missing y todos los *_template» junto a «Se quedan [...] _write_or_patch_config». Hoy esa función crea `config.json` con `_config_template`; no se dice qué fuente usa su rama de creación al borrar plantillas. Obligaría a inventar si lee la semilla, renderiza inline o conserva una plantilla.
2. Cita: «Se borran scaffold_desk» frente a «result = scaffold_desk(target_path)». `InitCLI`, `desk install` y `migrate_desk` consumen `created_paths`/`wrote_anything`; no se define la API sustituta ni cómo se preserva la salida «Wrote …». Obligaría a inventar el adaptador y su contrato de retorno.
3. Cita: «El Board va como semilla document» y «el perfil runtime-pi-deepseek-flash» entra como semilla `if_missing`. No se dice si el perfil runtime es texto estático o documento renderizado con `SYSTEM`. Obligaría a elegir representación.

DRY-RUN

Un ejecutor futuro leería TaskDoc, ritual, Board, archivos nombrados y APIs de sldb; no hay pills ni átomos ligados. Primero capturaría `tests/fixtures/golden/scaffold/{init,update}.json` y `test_scaffold_golden.py` con main. Luego crearía `data/templates/` y `desk_declaration.yaml`; sustituiría `{desk_name}` con `str.replace`; renderizaría el Board como `document`; añadiría `folders`, `seeds if_missing` e `include`; adaptaría `ensure_workspace` y `default_ritual_text`; borraría `scaffold_desk`, `_write_if_missing`, `guess_model_for_path` y `*_template`; ajustaría CLI, tests, package-data y CHANGELOG. Dependencia: sldb main ≥96d7b823 (G_GD26 satisfecho), sin cambiar pin. Validaría golden antes/después, grep vacío, segunda corrida idempotente, dry-run sobre copia en `/dev/shm`, tests listados, `wc -l` y CHANGELOG.

FUTURO

El coordinador fija worktree y acepta revisiones; el supervisor corre la suite completa sobre lo integrado; un tester independiente y el dueño deciden promoción/cierre. CC31/CC32/CC34 aportarán después las semillas managed. Nada de esto ejecuta el nodo.
