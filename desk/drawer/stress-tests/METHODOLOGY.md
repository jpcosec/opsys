# UX stress-test methodology

## Qué es

Un UX stress-test es una exploración sistemática de la interfaz CLI desde la perspectiva de un usuario. No busca "encuentra bugs en el código" sino "encuentra dónde la experiencia se rompe, confunde o contradice el modelo mental que el usuario construyó".

## Principios

1. **Read-only.** No se edita ningún archivo. No se modifica el sistema bajo test. Solo se ejecutan comandos y se observa.
2. **El usuario no sabe lo que sabe el desarrollador.** El test asume que el usuario no leyó el código fuente. Solo conoce `--help`, la documentación superficial, y su intuición.
3. **Modelo mental primero.** Cada test se basa en una `use-case` narrativa (UC-XX) que describe qué quiere lograr el usuario. El test verifica si el sistema lo deja lograr eso sin fricción.
4. **Anchor en atoms.** Si un atom dice "el CLI es thin sobre primitives y sldb", el test verifica: ¿el CLI es thin? ¿O tiene lógica duplicada? ¿O faltan comandos que el atom sugiere?
5. **Fricción es el hallazgo.** Un error con traceback es un hallazgo. Un comando que existe pero se comporta distinto a lo esperado es un hallazgo. Un output silencioso donde debería haber feedback es un hallazgo. Una inconsistencia entre tipos de artifact es un hallazgo.

## Estructura de un test

Cada test vive en `desk/drawer/stress-tests/st-XX-nombre.md` y contiene:

```markdown
# ST-XX: Nombre

**Basado en:** UC-XX

## Script

Secuencia de comandos CLI que el usuario ejecuta. Textual, uno por línea.
Incluye casos felices, casos borde, y casos de error.

## Puntos de estrés

Tabla: por cada paso del script, qué observar.
No es "funciona o no funciona". Es "el output es claro?",
"el error sugiere qué hacer?", "el usuario queda en un estado conocido?".

## Modos de fracaso

Lista de formas en que la experiencia se rompe.
Esto alimenta directamente los archivos de hallazgos.
```

## Cómo se ejecuta

1. Elegir un ST basado en un UC, o elegir una superficie no cubierta
2. Preparar setup si hace falta (estado inicial específico)
3. Ejecutar el script manualmente o mediante subagente
4. **Observar**, no juzgar. Anotar outputs textuales, exit codes, comportamientos sorprendentes
5. Escribir hallazgos en `findings/round-NN-descripcion.md`

## Qué observar en cada comando

| Dimensión | Preguntas |
|---|---|
| **Discoverability** | ¿El comando aparece en `--help`? ¿Su nombre es obvio? ¿Hay un subcomando donde el usuario esperaría uno distinto? |
| **Error messages** | ¿El error es para un humano o para un desarrollador? ¿Muestra traceback interno o mensaje semántico? ¿Sugiere qué hacer? |
| **Exit codes** | ¿0 para éxito, 1 para error manejado, 2 para argparse? ¿O hay casos donde un error devuelve 0? |
| **Silent failures** | ¿Hay comandos que devuelven 0 sin output y sin error cuando deberían haber fallado? |
| **Consistency** | ¿Tipos de artifact similares se comportan igual? ¿O task valida campos y ritual no? |
| **Naming** | ¿Los nombres de subcomandos son consistentes (singular/plural)? ¿Los flags siguen un patrón? |
| **State** | ¿El comando deja al usuario en un estado conocido? ¿Puede ver qué pasó? |
| **Output** | ¿El output es scrolleable? ¿Tiene estructura (tablas, columnas)? ¿O es texto plano sin formato? |
| **Edge cases** | ¿IDs vacíos, paths con espacios, strings muy largos, caracteres UTF-8? |
| **CI readiness** | ¿Se puede pipear? ¿Hay `--format json`? ¿Hay `--ci`? ¿Hay colores ANSI que rompen logs? |

## Pipeline de findings

```
UC-XX (narrativa)
  └→ ST-XX (script de comandos)
       └→ Observaciones (outputs textuales, anotaciones)
            └→ findings/round-NN-area.md (hallazgos consolidados)
                 └→ Priorización (qué arreglar, qué investigar, qué rediseñar)
```

## Cobertura esperada

Cada superficie del CLI debe tener al menos un ST. Las superficies se definen por comando top-level y por tipo de artifact:

| Superficie | ST asociado |
|---|---|
| about, faq | ST-01 |
| inbox | ST-02 |
| graph build/neighbors/missing | ST-03, ST-04 |
| list/show/add (todos los tipos) | ST-05, ST-11 |
| advance task | ST-05 |
| init, bootstrap | ST-init |
| repo register | ST-13 |
| atoms add-namespace | ST-14 |
| spec (infraestructura sin CLI) | ST-06 |
| drift, materialize, closeout (no existen) | ST-07 |
| edge cases, --root, errores | ST-12, ST-show-nonexistent |
| modelos, sldb state | ST-models |
| FAQ content | ST-faq |

## Lo que NO es un UX stress-test

- No es un test unitario (no prueba funciones aisladas)
- No es un test de integración (no verifica que módulos conecten)
- No es un test de regresión (no verifica que bugs anteriores no hayan vuelto)
- No es una auditoría de seguridad
- No es una revisión de código

Es una exploración de la experiencia del usuario. El entregable son hallazgos de fricción, no bugs etiquetados.
