---
kind: suggestion
sender_project: gemini_test
created_at: 2026-08-25T02:01:03
status: open
---

# Ritual: Zero-context subagent stress test

Es vital estandarizar un 'Test de Estrés de Arquitectura de Cero Contexto' usando un subagente (context: fresh) para revisar la carpeta desk/ antes de empezar a programar. En nuestro proyecto de Agente Conversacional, este test detectó instantáneamente 9 vacíos graves (timeouts de state machine, esquemas de payload no definidos, colisiones de CRON vs User). Propongo agregarlo como un paso oficial en el ritual de 'design' o 'preparation'.
