---
id: atom-todo-sustantivo-de-primer-nivel-del-cli-de-deskops-está-clasificado-una-sola-vez-en-su-gramática
title: Todo sustantivo de primer nivel del CLI de deskops está clasificado una sola
  vez en su gramática
five_wh_one_plus: what
tags:
- system:deskops
- topic:cli
---

# Todo sustantivo de primer nivel del CLI de deskops está clasificado una sola vez en su gramática

## Answer

Cada comando de primer nivel de deskops (cada sustantivo de command_registry) se clasifica exactamente una vez en TOP_LEVEL_GRAMMAR, que agrupa los comandos por su papel (por ejemplo operational para los que actúan sobre el ciclo de trabajo, como review), y las guardas de mutates de cada subcomando se leen del registro, no se repiten a mano. tests/test_cli_grammar.py lo hace cumplir: un comando nuevo que no se clasifica rompe el test, como pasó con review tras GC03. Al agregar un comando, se clasifica en la gramática en el mismo cambio.
