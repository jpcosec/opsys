# Deskops CLI — Cobertura de Stress-Testing

## Lo que se testeó (6 rondas, ~200 comandos)

| Área | Estado |
|---|---|
| **14 top-level commands** | Todos: show advance atoms faq repo desk bootstrap init graph add list about inbox |
| **15 add subcommands** | Todos: task, condition, operator, checklist, hook, edge, routine, pill, ritual, board, atom, repository, inbox-note, faq-doc, step |
| **15 list types** | Todos, incluyendo IDs válidos, inválidos, vacíos |
| **15 show types** | Todos, incluyendo IDs válidos, inválidos, vacíos, substring match |
| **15 --from-yaml paths** | Min YAML, full YAML, empty YAML, malformed, extra fields, mixed inline |
| **6 primitive types** | condition, operator, checklist, hook, edge, routine — creación, listado, show |
| **Cross-command workflows** | Pill lifecycle, board+task, ritual+step, FAQ, inbox, repo+atom, graph rebuild |
| **Edge cases** | Empty inputs, whitespace-only, emojis, very long (10K chars), newlines, HTML |
| **File system edge cases** | Nonexistent --root, read-only /etc, / (root), path traversal, symlinks, permissions |
| **Environment** | No HOME, no TMPDIR, non-repo directory, stdout vs stderr, signal handling |
| **Help system** | -h vs --help, bare command, all subcommand help pages |
| **Error messages** | Consistency across 15 types, Pydantic tracebacks, "Unexpected:" prefix, path leaks |
| **Exit codes** | All commands checked |
| **Python API** | 23 submodules, 17 Pydantic models, compiler, graph extractors, materializers, mermaid, workspace |
| **Test suite** | 14 files, 59/59 passing |
| **Graph resilience** | Corrupted kg.json → rebuild OK |
| **Install/bootstrap** | desk install, bootstrap vs init, repo register path validation |

## Lo que NO se testeó (no testear por ahora)

| Área | Razón |
|---|---|
| **Concurrencia** (dos deskops simultáneos) | Bajo impacto UX, difícil de testear confiablemente |
| **Rendimiento con miles de archivos** | Requiere generar datos de test masivos |
| **Cross-platform** (Windows, macOS) | Solo Linux disponible |
| **Memory profiling** | No hay señales de leaks |
| **Internationalization / locale** | Solo inglés |
| **sldb actualizaciones** | Dependencia externa, no se mockea |
| **Network / offline behavior** | Ya se verificó que bootstrap no requiere network si sldb presente |

## Hallazgos principales (top 10)

1. **CRITICAL**: advance task no funciona — sldb parser cross-wires campos markdown
2. **CRITICAL**: `show` glob `f"{id}*.md"` devuelve artifacts equivocados (suffix match)
3. **CRITICAL**: `list inbox-notes` ignora 11/13 notas (glob incompatible con date-prefix)
4. **CRITICAL**: 8 tipos con empty YAML `{}` crean artifacts basura (`*-none`, title `"None"`)
5. **CRITICAL**: `list tasks` crash total por un archivo inválido
6. **CRITICAL**: KG JSON edge serialization bug (68 edges con role/target null)
7. **HIGH**: 13/15 show types leakean paths absolutos con `Unexpected:`
8. **HIGH**: `_normalize_task_payload` splitea strings en caracteres (pills, references, etc.)
9. **HIGH**: `repo register` overwrites file antes de checkear duplicados
10. **HIGH**: `--from-yaml` no tiene rollback — huérfanos en disco tras fallo
