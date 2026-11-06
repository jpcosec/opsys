REFORMULACION
Propósito: sustituir las plantillas del desk que hoy son strings en deskops/workspace.py (config.json, Board, pills, rituales phase/execution/testing/closeout, drawer/README.md, tag-namespaces y runtime-pi-deepseek-flash) por archivos en deskops/data/templates/ y una declaración deskops/data/desk_declaration.yaml que deskops renderiza en proceso y pasa a sldb.api.scaffold_store; desk update usa includes declarados en vez de adivinar modelos.
Resultado: init y desk update --apply con el mismo árbol y sha256 que el golden; segunda corrida idempotente; borrados scaffold_desk, _write_if_missing, *_template y guess_model_for_path; default_ritual_text lee plantilla.
Repo: deskops, worktree por nodo en robocop2, sldb >=96d7b823.
Límites: no subir sldb ni el pin (solo package-data); no cambiar formato del desk ni gramática/goldens CLI; fuera CC31/32/34; inspect_desk, migrate_desk, classify_desk y _write_or_patch_config quedan; nada en desks reales.

AMBIGUEDADES
1. c3: «el worker elige uno y lo nombra en el informe» — fuerza elegir qué fixture de desk viejo usar (golden_desk u otro de migrate_desk/desk_sync).
2. SCOPE: «operations.py:231-241» frente a c2: «ensure_workspace vive en deskops/doc_access.py:146» — fuerza decidir qué módulo editar para las carpetas.
3. c5: «un solo placeholder del nombre» — no nombra el token; fuerza inventar su sintaxis y el mecanismo de sustitución.
4. c5: «includes declarados {model, glob}» — no dice dónde ni con qué esquema se declaran; fuerza inventar su ubicación y claves.
5. Título «faq como datos» frente a c5 «init no la escribe» y «deskops/data/faq.md el respaldo» — fuerza decidir si faq.md va a data/templates o queda en data/faq.md y si es semilla.

DRY-RUN
Lecturas: TaskDoc y c1-c8; workspace.py, doc_access.py, lifecycle.py, cli/commands/{core,desk,doctor}.py, bootstrap.py; firmas de scaffold_store y apply_includes; pyproject.toml; fixtures y tests citados.
Cambios: primer commit solo golden init/update y test_scaffold_golden; después data/templates/ y desk_declaration.yaml, workspace.py, cableado en doc_access/core/doctor/bootstrap, includes en desk.py, default_ritual_text, package-data, tests y CHANGELOG.
Dependencias: sldb >=96d7b823 (GD26), fixture de desk viejo, /dev/shm.
Validaciones futuras: pytest de los archivos listados, greps, segunda corrida, dry-run sobre copia, goldens de ayuda, wc -l.

FUTURO
El supervisor fija worktree, corre la suite completa sobre lo integrado y decide revisiones en frío; el worker elige y reporta el fixture y anota si _write_or_patch_config podría ser semilla sin cambiarlo; el coordinador decide cualquier subida de sldb (fuera de alcance); CC31/32/34 aportan las semillas managed.
