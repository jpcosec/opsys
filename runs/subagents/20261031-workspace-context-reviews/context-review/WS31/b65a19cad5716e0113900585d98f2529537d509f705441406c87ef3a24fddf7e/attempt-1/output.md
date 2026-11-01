REFORMULACION
WS31 es un nodo de entrega documental en deskops: publicar el manual básico probado con navegación, edición, captura, trabajo manual y revisión demostradas, incorporando el índice de `borradores/manual.md`, capturas y limitaciones en `docs/workspace-user-manual.md`, con assets y átomos vinculados. Depende de WS30, WS10 y WS43; requiere G_HUMAN_MANUAL. Límites: Scion solo propuesto hasta WS38; personalización/impacto no bloquean el manual básico; no atomizar permisos ni aceptación técnica inexistente.

AMBIGUEDADES
1. «un átomo por cada decisión Pxx humana o técnica ya registrada y vigente en decisiones.md y por cada contrato en contratos/»: WS43, dependencia de WS31, ya produce «átomos de acuerdos durables»; no se dice si WS31 debe reutilizarlos o crear otros. Obliga a inventar regla antiduplicado.
2. «decisión Pxx humana o técnica ya registrada y vigente en decisiones.md»: ese archivo incluye T-P01…T-P09 y T-P03.1; no aclara si «Pxx» los abarca. Obliga a inventar el conjunto atomizable.
3. «incorporar el índice de borradores/manual.md, capturas y limitaciones a docs/workspace-user-manual.md»: no nombra productor de capturas ni acta de origen; WS31 no ejecuta UI. Obliga a inventar fuente/producción o a omitirlas.
4. «Tester independiente verifica esos criterios antes del cierre»: no identifica actor ni cómo se acredita independencia. Obliga a inventar quién valida.

DRY-RUN
Leería `dag.yaml` WS31, `borradores/manual.md`, `decisiones.md`, `cobertura.md`, acta WS30 y acta WS43, contratos de `contratos/`, átomos existentes y el manual destino. Escribiría el manual, assets y átomos; etiquetaría capítulos; mantendría Scion propuesto; añadiría limitaciones. Consumiría G_HUMAN_MANUAL (acta WS30), índice WS10 y acta WS43; contratos WS11/12. Si falta acta o contrato, pararía y registraría hueco; sin evidencia WS29 o G_HUMAN_MODEL, dejaría propuesto. Validaría links, etiquetas y atom→doc; después, Tester independiente. Sin ejecutar.

FUTURO
WS30 produce acta y G_HUMAN_MANUAL; WS43, acta de publicación y correspondencia; WS11/WS12, contratos e inventario; WS29 y WS39/G_HUMAN_MODEL, evidencia; WS37/WS38, capítulo Scion. Las decisiones humanas de producto ya registradas no se reabren aquí.
