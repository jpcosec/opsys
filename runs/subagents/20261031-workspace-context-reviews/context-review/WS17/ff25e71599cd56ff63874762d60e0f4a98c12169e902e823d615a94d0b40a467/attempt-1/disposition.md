# Disposición WS17, revisión 9

Borrador redactado por un agente Claude Sonnet y revisado por el coordinador.

**Fidelidad.** Fiel. Plantillas Markdown authored en ejemplo/nav/ (no genera corpus), repo deskops, depende de WS11 y WS40, WS16 no depende, WS30 integra y WS43 reutiliza: coincide.

**Ambigüedades.**

1. «cada plantilla resuelve el root/store… de los dos desks» frente a «conjunto de plantillas cubre ambos desks, no cada plantilla individual». Clase: `no es ambigüedad`. la última frase de la aceptación resuelve: la cobertura de ambos desks es del conjunto; cada plantilla solo debe resolver sus links contra los roots/aliases del manifiesto WS40.
2. umbral de «cubre ambos desks». Clase: `detalle de promoción`. caso de prueba: la aceptación pide «recorrer links Markdown sin UI» y resolver cada link contra el manifiesto; cuántos enlaces por desk lo fija el TaskDoc.
3. quién regenera el corpus con ejemplo/nav/. Clase: `futuro asignado`. productor WS40: «El generador de WS40 acepta estas fuentes y las materializa»; WS17 invoca ese comando (ver promotion-notes.md).
